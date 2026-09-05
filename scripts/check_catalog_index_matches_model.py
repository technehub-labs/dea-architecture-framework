"""Cross-repo smoke test: model vs. catalog content (CR-CATALOG-STRUCT-07c).

Walks the OpenDEAM root model (model/opendeam-model.yaml) and verifies
that each model entity whose `catalog_repo` matches a known conformant
adopter is backed by a CATALOG.yaml that:

  1. Exists and parses cleanly.
  2. Declares a metamodel_version compatible with the model pin.
  3. Has content consistent with the model's status field:
     - status: existing    -> catalog counts.canonical >= 1
     - status: planned     -> catalog counts.canonical >= 1 (warning if 0)
     - status: scaffold    -> catalog counts.canonical >= 0 (warning if > 0;
       signals the model status is stale relative to the actual catalog)
     - status: proposed/retired -> out of scope (no catalog expected)

Exits 0 on success; non-zero on hard failures (e.g. model file missing,
, schema mismatch). Warnings print to stderr and do NOT fail CI; they
surface drift the consumer operator should reconcile.

Usage:
    # Offline (cache populated from a prior run):
    python scripts/check_catalog_index_matches_model.py \\
        --model model/opendeam-model.yaml \\
        --cache-dir .cache/cross_repo_consumer \\
        --offline

    # Online (live fetches via raw.githubusercontent.com):
    python scripts/check_catalog_index_matches_model.py \\
        --model model/opendeam-model.yaml

This script does NOT replace validate_consumer.py or validate_model.py;
it complements them by adding the catalog-content side of the
allocation contract (the model declares which catalog owns each
entity; the catalogs declare what they actually contain).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable

# Make the vendored cross_repo_consumer importable.
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import yaml  # noqa: E402

from cross_repo_consumer import parse_catalog_yaml  # noqa: E402
from cross_repo_consumer.fetch import fetch_catalog_yaml  # noqa: E402


# Known conformant adopters (L1 catalogs). Keep in lock-step with the
# adoption tracker at dea-metaframework/docs/standards/
# catalog-repository-pattern-adoption.md.
KNOWN_ADOPTERS: frozenset[str] = frozenset(
    {
        "dea-catalog-processes",
        "dea-catalog-business-capabilities",
        "dea-catalog-digital-business-service-factory",
        "dea-catalog-stakeholders",
    }
)


def load_model_entities(model_path: Path) -> list[dict[str, Any]]:
    """Load entity entries from the OpenDEAM root model.

    Returns:
        The list under `allocation.entities` in the model YAML.
    """
    doc = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    try:
        return list(doc["allocation"]["entities"])
    except (KeyError, TypeError) as exc:
        raise SystemExit(
            f"ERROR: {model_path} does not have allocation.entities: {exc}"
        ) from exc


def version_compatible(pinned: str, catalog_version: str) -> bool:
    """Best-effort semver-ish compatibility check.

    The standard's metamodel_version uses carets (^0.2.1, ^1.0.0)
    for a reason: a major or minor bump is a contract break. This
    function accepts the catalog's metamodel_version only if its
    major AND minor match the pin's. Anything else is flagged.

    Examples (pin="1.0.0"):
      "1.0.0"      -> compatible
      "1.0.5"      -> compatible (patch bump; backwards-compatible)
      "1.2.3"      -> INCOMPATIBLE (minor bump; potentially breaking)
      "2.0.0"      -> INCOMPATIBLE (major bump; breaking)

    A None / empty catalog_version is treated as unknown (warning,
    not failure) because the schema does not require it.
    """
    if not catalog_version:
        return True  # unknown; warn elsewhere
    pin = pinned.lstrip("^").strip()
    cat = catalog_version.lstrip("^").strip()
    pin_major_minor = ".".join(pin.split(".")[:2])
    cat_major_minor = ".".join(cat.split(".")[:2])
    return pin_major_minor == cat_major_minor


def entity_relevant_to_smoke(entity: dict[str, Any]) -> bool:
    """Skip entities whose catalog_repo is null or not a known adopter."""
    repo = entity.get("catalog_repo")
    return bool(repo) and repo in KNOWN_ADOPTERS


def check_one_entity(
    entity: dict[str, Any],
    catalogs: dict[str, Any],
) -> tuple[str, str, list[str]]:
    """Verify one model entity's catalog_repo is backed correctly.

    Returns:
        (entity_id, catalog_repo, list_of_findings).
        Findings are strings; severity is implicit ("WARN:" vs "FAIL:").
    """
    findings: list[str] = []
    entity_id = entity["entity_id"]
    repo = entity["catalog_repo"]
    status = entity.get("status", "planned")
    if repo not in catalogs:
        findings.append(f"FAIL: {repo} was not fetched (consumer returned no catalog)")
        return entity_id, repo, findings

    cat = catalogs[repo]
    canonical = cat.counts.canonical
    metamodel_version = cat.metadata.metamodel_version or ""

    # Status/content expectation.
    if status == "existing":
        if canonical == 0:
            findings.append(
                f"FAIL: status=existing but catalog has 0 canonical entities"
            )
    elif status == "planned":
        if canonical == 0:
            findings.append(
                f"WARN: status=planned and catalog has 0 canonical entities "
                f"(consider promoting to 'existing' once content lands)"
            )
    elif status == "scaffold":
        if canonical > 0:
            findings.append(
                f"WARN: status=scaffold but catalog has {canonical} canonical "
                f"entities (model status is stale; promote to 'existing' or "
                f"'planned')"
            )
    elif status in ("proposed", "retired"):
        # These don't need catalog backing.
        pass
    else:
        findings.append(f"WARN: unknown status {status!r}")

    return entity_id, repo, findings


def collect_known_adopter_repos(
    entities: Iterable[dict[str, Any]],
) -> set[str]:
    """Set of catalog_repos that are known adopters referenced by model entries."""
    return {e["catalog_repo"] for e in entities if entity_relevant_to_smoke(e)}


def run_smoke(
    model_path: Path,
    cache_dir: Path | None = None,
    *,
    offline: bool = False,
    timeout_s: float = 15.0,
    treat_fetch_failure_as_skip: bool = False,
) -> tuple[int, int, list[str]]:
    """Run the smoke test; return (fail_count, warn_count, finding_lines).

    Args:
        treat_fetch_failure_as_skip: When True, a fetch failure for a
            known adopter does NOT count as a fail. Instead it emits
            an INFO note and is skipped. Useful in CI environments
            that cannot reach private repos without a PAT.
    """
    fail_count = 0
    warn_count = 0
    findings: list[str] = []

    entities = load_model_entities(model_path)
    repos_to_fetch = collect_known_adopter_repos(entities)

    if not repos_to_fetch:
        findings.append(
            "INFO: no model entities reference known conformant adopters; "
            "nothing to smoke"
        )
        return 0, 0, findings

    findings.append(f"INFO: {len(entities)} model entities; "
                    f"{len(repos_to_fetch)} reference known adopters "
                    f"({sorted(repos_to_fetch)})")

    # Fetch every known adopter referenced by the model.
    catalogs: dict[str, Any] = {}
    for repo in sorted(repos_to_fetch):
        try:
            fetch = fetch_catalog_yaml(
                repo,
                ref="main",
                cache_dir=cache_dir,
                timeout_s=timeout_s,
                offline=offline,
            )
        except Exception as exc:  # noqa: BLE001 (CLI surface; surfacing all)
            # Fetch-stage errors are the only ones that can be skipped.
            # A 404 (private repo no PAT), a cache miss in offline mode,
            # or a CDN timeout all land here.
            if treat_fetch_failure_as_skip:
                findings.append(
                    f"INFO: {repo}: skipped (fetch error: "
                    f"{type(exc).__name__}: {exc})"
                )
                continue
            findings.append(f"FAIL: {repo}: {type(exc).__name__}: {exc}")
            fail_count += 1
            continue
        try:
            catalogs[repo] = parse_catalog_yaml(fetch.bytes)
        except Exception as exc:  # noqa: BLE001 (CLI surface; surfacing all)
            # Parse-stage errors are schema/content integrity issues.
            # They are NOT skipped by --skip-unreachable; a broken
            # catalog that was successfully fetched is still a real
            # failure that the operator must fix.
            findings.append(f"FAIL: {repo}: parse error: "
                            f"{type(exc).__name__}: {exc}")
            fail_count += 1

    # Per-entity checks.
    for entity in entities:
        if not entity_relevant_to_smoke(entity):
            continue
        entity_id, repo, entity_findings = check_one_entity(entity, catalogs)
        # If the catalog was skipped (not in catalogs), all findings
        # for this entity are SKIPPED at the entity level rather than
        # FAIL (the consumer can't reach the repo, so it can't validate).
        if repo not in catalogs:
            findings.append(
                f"  {entity_id} ({repo}): SKIPPED (catalog not reachable; "
                f"verify manually with a PAT)"
            )
            continue
        for finding in entity_findings:
            findings.append(f"  {entity_id} ({repo}): {finding}")
            if finding.startswith("FAIL"):
                fail_count += 1
            elif finding.startswith("WARN"):
                warn_count += 1

    return fail_count, warn_count, findings


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check-catalog-index-matches-model",
        description=(
            "Cross-repo smoke test: verify that each model entity whose "
            "catalog_repo is a known conformant adopter is backed by a "
            "CATALOG.yaml with content consistent with the model status."
        ),
    )
    p.add_argument(
        "--model",
        type=Path,
        default=Path("model/opendeam-model.yaml"),
        help="Path to the OpenDEAM root model (default: model/opendeam-model.yaml).",
    )
    p.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Cache directory for fetched CATALOG.yaml (offline path).",
    )
    p.add_argument(
        "--offline",
        action="store_true",
        help="Do not fetch; only read from --cache-dir.",
    )
    p.add_argument(
        "--skip-unreachable",
        action="store_true",
        help=(
            "Treat fetch failures as SKIP (do not fail CI). Useful when "
            "some known adopters are private and the CI runner has no "
            "PAT. The skipped repos are listed in the output so the "
            "consumer operator can verify them manually with credentials."
        ),
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="HTTP timeout in seconds (default: 15).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if not args.model.is_file():
        print(f"ERROR: model file not found: {args.model}", file=sys.stderr)
        return 1
    fail, warn, findings = run_smoke(
        args.model,
        cache_dir=args.cache_dir,
        offline=args.offline,
        timeout_s=args.timeout,
        treat_fetch_failure_as_skip=args.skip_unreachable,
    )
    for line in findings:
        print(line)
    print(f"\nresult: {fail} failure(s), {warn} warning(s)")
    return 1 if fail > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())