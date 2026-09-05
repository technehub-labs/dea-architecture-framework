"""Tests for check_catalog_index_matches_model (CR-CATALOG-STRUCT-07c).

Offline-only: tests exercise the model parser + status/content checks
against a fixture model + cached catalogs. No network round-trips in CI.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import check_catalog_index_matches_model as smoke


# Fixture model: a minimal OpenDEAM root model with three entities.
# Tests assert that the smoke test detects each scenario correctly.
FIXTURE_MODEL_YAML = """\
allocation:
  entities:
    - entity_id: dea:entity-stakeholder
      class_alias: SH
      display_name: Stakeholder
      layer: L1
      status: scaffold
      catalog_repo: dea-catalog-stakeholders
    - entity_id: dea:entity-business-process
      class_alias: BP
      display_name: Business Process
      layer: L2
      status: existing
      catalog_repo: dea-catalog-processes
    - entity_id: dea:entity-capability
      class_alias: CAP
      display_name: Capability
      layer: L2
      status: planned
      catalog_repo: dea-catalog-business-capabilities
    - entity_id: dea:entity-ecosystem-platform
      class_alias: EP
      display_name: Ecosystem Platform
      layer: L1
      status: planned
      catalog_repo: dea-catalog-ecosystem-platforms
    - entity_id: dea:entity-unrelated
      class_alias: UR
      display_name: Unrelated
      layer: L5
      status: planned
      catalog_repo: null
"""


@pytest.fixture
def fixture_model(tmp_path: Path) -> Path:
    p = tmp_path / "model.yaml"
    p.write_text(FIXTURE_MODEL_YAML)
    return p


@pytest.fixture
def adopter_cache(tmp_path: Path) -> Path:
    """Cache with three of the four known adopters (BC + processes +
    stakeholders); DBSF intentionally omitted to test the missing-repo
    case."""
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "dea-catalog-stakeholders@main.yaml").write_text(
        "catalog:\n  id: dea:catalog-stakeholders\n  name: Stakeholders\n"
        "  abbreviation: SH\n  metamodel_version: '^0.2.1'\n  counts:\n"
        "    entities: 0\n    canonical: 0\n    candidates: 0\n"
        "    retired: 0\n    research_files: 0\n    open_change_requests: 0\n"
        "  entities: []\n"
    )
    (cache / "dea-catalog-processes@main.yaml").write_text(
        "catalog:\n  id: dea:catalog-processes\n  name: Processes\n"
        "  abbreviation: BP\n  metamodel_version: '1.0.0'\n  counts:\n"
        "    entities: 2\n    canonical: 2\n    candidates: 0\n"
        "    retired: 0\n    research_files: 3\n    open_change_requests: 0\n"
        "  entities:\n"
        "    - id: dea:process-x\n      type: Process\n      state: canonical\n"
        "      path: entities/v1-alpha/x/x.yaml\n      lifecycle_status: active\n"
        "      version: '1.0.0'\n      last_modified: '2026-09-05'\n"
        "      research_count: 0\n      candidate_count: 0\n"
        "      canonical_count: 1\n      retired_count: 0\n"
        "    - id: dea:process-y\n      type: Process\n      state: canonical\n"
        "      path: entities/v1-alpha/y/y.yaml\n      lifecycle_status: active\n"
        "      version: '1.0.0'\n      last_modified: '2026-09-05'\n"
        "      research_count: 0\n      candidate_count: 0\n"
        "      canonical_count: 1\n      retired_count: 0\n"
    )
    (cache / "dea-catalog-business-capabilities@main.yaml").write_text(
        "catalog:\n  id: dea:catalog-business-capabilities\n  name: BC\n"
        "  abbreviation: BC\n  metamodel_version: '1.0.0'\n  counts:\n"
        "    entities: 26\n    canonical: 26\n    candidates: 0\n"
        "    retired: 0\n    research_files: 0\n    open_change_requests: 0\n"
        "  entities:\n"
        "    - id: dea:capability-z\n      type: BusinessCapability\n"
        "      state: canonical\n      path: entities/v1-alpha/z/z.yaml\n"
        "      lifecycle_status: active\n      version: '1.0.0'\n"
        "      last_modified: '2026-09-05'\n      research_count: 0\n"
        "      candidate_count: 0\n      canonical_count: 1\n"
        "      retired_count: 0\n"
    )
    return cache


# ---------------------------------------------------------------------------
# Pure-function tests
# ---------------------------------------------------------------------------


class TestVersionCompatible:
    """The semver-ish compat check."""

    def test_equal(self) -> None:
        assert smoke.version_compatible("1.0.0", "1.0.0") is True

    def test_patch_bump_compatible(self) -> None:
        assert smoke.version_compatible("1.0.0", "1.0.5") is True

    def test_minor_bump_incompatible(self) -> None:
        # The standard's pin scheme treats minor bumps as a contract break
        # (e.g., a new dimension or removed entity); we flag any catalog
        # whose minor does not match.
        assert smoke.version_compatible("1.0.0", "1.2.3") is False

    def test_major_bump_incompatible(self) -> None:
        assert smoke.version_compatible("1.0.0", "2.0.0") is False

    def test_minor_bump_incompatible(self) -> None:
        # The standard's pin scheme treats major.minor as a contract; we
        # flag any catalog whose major.minor does not match.
        assert smoke.version_compatible("1.0.0", "1.5.0") is False

    def test_empty_catalog_version_is_unknown(self) -> None:
        assert smoke.version_compatible("1.0.0", "") is True
        assert smoke.version_compatible("1.0.0", None) is True  # type: ignore[arg-type]

    def test_caret_stripped(self) -> None:
        assert smoke.version_compatible("^0.2.1", "0.2.5") is True
        assert smoke.version_compatible("0.2.1", "^0.2.5") is True


class TestEntityRelevantToSmoke:
    def test_known_adopter_is_relevant(self) -> None:
        e = {"catalog_repo": "dea-catalog-processes"}
        assert smoke.entity_relevant_to_smoke(e) is True

    def test_unknown_catalog_not_relevant(self) -> None:
        e = {"catalog_repo": "dea-catalog-ecosystem-platforms"}
        assert smoke.entity_relevant_to_smoke(e) is False

    def test_null_repo_not_relevant(self) -> None:
        assert smoke.entity_relevant_to_smoke({"catalog_repo": None}) is False
        assert smoke.entity_relevant_to_smoke({}) is False


class TestCollectKnownAdopterRepos:
    def test_collects_only_known_adopters(self) -> None:
        entities = [
            {"catalog_repo": "dea-catalog-processes"},
            {"catalog_repo": "dea-catalog-ecosystem-platforms"},
            {"catalog_repo": "dea-catalog-stakeholders"},
            {"catalog_repo": None},
        ]
        assert smoke.collect_known_adopter_repos(entities) == {
            "dea-catalog-processes",
            "dea-catalog-stakeholders",
        }


# ---------------------------------------------------------------------------
# Smoke-run tests
# ---------------------------------------------------------------------------


class TestRunSmoke:
    def test_existing_with_content_passes(
        self, fixture_model: Path, adopter_cache: Path
    ) -> None:
        """Existing+has-canonical: no warning, no failure."""
        fail, warn, findings = smoke.run_smoke(
            fixture_model, cache_dir=adopter_cache, offline=True
        )
        assert fail == 0
        assert warn == 0
        assert any("INFO: 5 model entities" in f for f in findings)

    def test_scaffold_with_zero_content_passes(
        self, fixture_model: Path, adopter_cache: Path
    ) -> None:
        """Stakeholders is scaffold with 0 canonical entities: correct state."""
        fail, warn, findings = smoke.run_smoke(
            fixture_model, cache_dir=adopter_cache, offline=True
        )
        # The scaffold+0 case is the EXPECTED state for stakeholders.
        stakeholder_findings = [
            f for f in findings if "dea:entity-stakeholder" in f
        ]
        assert all("WARN" not in f for f in stakeholder_findings)
        assert fail == 0

    def test_planned_with_content_passes(
        self, fixture_model: Path, adopter_cache: Path
    ) -> None:
        """Capability is planned with 26 canonical entities: no warning
        (planned+has-content is the natural progression; promotion to
        'existing' is a model-update concern)."""
        fail, warn, findings = smoke.run_smoke(
            fixture_model, cache_dir=adopter_cache, offline=True
        )
        capability_findings = [
            f for f in findings if "dea:entity-capability" in f
        ]
        assert all("WARN" not in f for f in capability_findings)
        assert fail == 0

    def test_missing_adopter_catalog_fails(
        self, fixture_model: Path, tmp_path: Path
    ) -> None:
        """An adopter that's NOT in the cache surfaces as FAIL."""
        cache = tmp_path / "empty"
        cache.mkdir()
        fail, warn, findings = smoke.run_smoke(
            fixture_model, cache_dir=cache, offline=True
        )
        assert fail > 0
        assert any(
            "dea-catalog-processes" in f and "FAIL" in f for f in findings
        )

    def test_model_with_no_known_adopters_returns_clean(
        self, tmp_path: Path
    ) -> None:
        """A model whose entities only reference non-adopter repos
        returns 0 failures and 0 warnings with an INFO note."""
        model = tmp_path / "minimal.yaml"
        model.write_text(
            "allocation:\n  entities:\n"
            "    - entity_id: dea:entity-x\n      catalog_repo: null\n"
            "      status: planned\n"
        )
        cache = tmp_path / "cache"
        cache.mkdir()
        fail, warn, findings = smoke.run_smoke(
            model, cache_dir=cache, offline=True
        )
        assert fail == 0
        assert warn == 0
        assert any("nothing to smoke" in f for f in findings)

    def test_skip_unreachable_treats_fetch_failures_as_skip(
        self, tmp_path: Path
    ) -> None:
        """With treat_fetch_failure_as_skip=True, a missing catalog
        file is logged as INFO rather than FAIL."""
        model = tmp_path / "model.yaml"
        model.write_text(
            "allocation:\n  entities:\n"
            "    - entity_id: dea:entity-x\n"
            "      catalog_repo: dea-catalog-processes\n"
            "      status: existing\n"
        )
        # Cache is empty: processes the catalog will not be found.
        cache = tmp_path / "empty"
        cache.mkdir()
        fail, warn, findings = smoke.run_smoke(
            model,
            cache_dir=cache,
            offline=True,
            treat_fetch_failure_as_skip=True,
        )
        assert fail == 0
        assert warn == 0
        assert any(
            "INFO: dea-catalog-processes: skipped" in f for f in findings
        )
        assert any(
            "dea:entity-x" in f and "SKIPPED" in f for f in findings
        )

    def test_skip_unreachable_does_not_mask_schema_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A schema parse error (catalog exists but is broken YAML)
        is still a FAIL even with treat_fetch_failure_as_skip=True.
        Only fetch failures are skipped; parse errors propagate."""
        model = tmp_path / "model.yaml"
        model.write_text(
            "allocation:\n  entities:\n"
            "    - entity_id: dea:entity-x\n"
            "      catalog_repo: dea-catalog-processes\n"
            "      status: existing\n"
        )
        cache = tmp_path / "cache"
        cache.mkdir()
        # A valid YAML document, but with the WRONG shape: parse_catalog_yaml
        # will reject this. This proves fetch-skip does not mask parse failures.
        (cache / "dea-catalog-processes@main.yaml").write_text(
            "not_a_catalog_root: true\n"
        )
        fail, _, findings = smoke.run_smoke(
            model,
            cache_dir=cache,
            offline=True,
            treat_fetch_failure_as_skip=True,
        )
        assert fail > 0
        assert any("FAIL" in f for f in findings)


class TestStatusContentMismatch:
    """The status/content drift checks (the smoke test's primary value)."""

    def test_existing_with_zero_canonical_fails(self, tmp_path: Path) -> None:
        """Status=existing but catalog has 0 canonical: FAIL."""
        model = tmp_path / "model.yaml"
        model.write_text(
            "allocation:\n  entities:\n"
            "    - entity_id: dea:entity-x\n      catalog_repo: dea-catalog-processes\n"
            "      status: existing\n"
        )
        cache = tmp_path / "cache"
        cache.mkdir()
        (cache / "dea-catalog-processes@main.yaml").write_text(
            "catalog:\n  id: x\n  name: X\n  abbreviation: X\n"
            "  metamodel_version: '1.0.0'\n  counts:\n"
            "    entities: 0\n    canonical: 0\n    candidates: 0\n"
            "    retired: 0\n    research_files: 0\n    open_change_requests: 0\n"
            "  entities: []\n"
        )
        fail, warn, findings = smoke.run_smoke(
            model, cache_dir=cache, offline=True
        )
        assert fail == 1
        assert any("FAIL" in f and "0 canonical" in f for f in findings)

    def test_scaffold_with_canonical_warns(self, tmp_path: Path) -> None:
        """Status=scaffold but catalog has canonical entities: WARN
        (model is stale relative to the actual catalog)."""
        model = tmp_path / "model.yaml"
        model.write_text(
            "allocation:\n  entities:\n"
            "    - entity_id: dea:entity-x\n      catalog_repo: dea-catalog-processes\n"
            "      status: scaffold\n"
        )
        cache = tmp_path / "cache"
        cache.mkdir()
        (cache / "dea-catalog-processes@main.yaml").write_text(
            "catalog:\n  id: x\n  name: X\n  abbreviation: X\n"
            "  metamodel_version: '1.0.0'\n  counts:\n"
            "    entities: 1\n    canonical: 1\n    candidates: 0\n"
            "    retired: 0\n    research_files: 0\n    open_change_requests: 0\n"
            "  entities:\n"
            "    - id: dea:x\n      type: Process\n      state: canonical\n"
            "      path: x\n      lifecycle_status: active\n"
            "      version: '1.0.0'\n      last_modified: '2026-09-05'\n"
            "      research_count: 0\n      candidate_count: 0\n"
            "      canonical_count: 1\n      retired_count: 0\n"
        )
        fail, warn, findings = smoke.run_smoke(
            model, cache_dir=cache, offline=True
        )
        assert fail == 0
        assert warn == 1
        assert any(
            "WARN" in f and "stale" in f and "scaffold" in f for f in findings
        )