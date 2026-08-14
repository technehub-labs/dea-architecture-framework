#!/usr/bin/env python3
"""Validate model/opendeam-model.yaml — schema + referential integrity.

v0.2.0 (ADR-0002): measurement is an orthogonal dimension, not a layer.
Entities without a `layer` are dimension entities (e.g. MTR) and are checked
against scope_layers rules instead of layer/building_block containment.

Checks beyond JSON Schema:
  1. Layer IDs are unique and sequential (L1..Ln).
  2. class_alias and entity_id are globally unique.
  3. Non-dimension entities: layer exists; building_block exists INSIDE that
     layer. Dimension entities (no layer): must declare scope_layers (valid
     layer IDs) and must NOT declare building_block.
  4. Every relationship endpoint resolves to a declared class_alias.
  5. Entities with status 'existing'/'scaffold' must declare a catalog_repo.
  6. measured_by targets exist and are dimension entities; the measured
     entity's layer must be within the metric's scope_layers.
  6b. governed_by targets exist and are L2-risk-compliance entities
     (ADR-0003 D6).
  6c. defined_by / parent_concept targets exist and are dimension entities
     covering the source entity's layer; no Concept self-parenting
     (ADR-0004 D2). `enforcement` is enum-constrained by the schema
     (ADR-0004 D4).
  7. specializes targets exist and are abstract:true; the parent's
     realized_in_layers must include the subclass's layer. abstract:true
     entities must declare realized_in_layers.
  8. A catalog_repo shared by multiple entities requires every sharer to
     declare a discriminator (ADR-0002 D6) — non-blocking warning as of v0.3.0.
  9. VERSION file matches model.version.

Run: python3 scripts/validate_model.py
Exit: 0 = clean, 1 = violations found.
"""
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

BASE = Path(__file__).parent.parent
MODEL = BASE / "model" / "opendeam-model.yaml"
SCHEMA = BASE / "schemas" / "opendeam-model.schema.json"
VERSION = BASE / "VERSION"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    model = yaml.safe_load(MODEL.read_text())
    schema = yaml.safe_load(SCHEMA.read_text())

    # 0. JSON Schema
    for e in Draft7Validator(schema).iter_errors(model):
        errors.append(f"schema: {'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}")

    layers = model["architecture"]["layers"]
    entities = model["allocation"]["entities"]
    rels = model["relationships"]

    layer_ids = [l["id"] for l in layers]
    bb_by_layer = {l["id"]: {bb["id"] for bb in l["building_blocks"]} for l in layers}

    # 1. Layer IDs unique + sequential
    if len(layer_ids) != len(set(layer_ids)):
        errors.append("integrity: duplicate layer IDs")
    expected = [f"L{i+1}" for i in range(len(layer_ids))]
    if layer_ids != expected:
        errors.append(f"integrity: layer IDs must be sequential {expected}, got {layer_ids}")

    # 2. Alias / entity_id uniqueness
    aliases = [e["class_alias"] for e in entities]
    ids = [e["entity_id"] for e in entities]
    for dup in {a for a in aliases if aliases.count(a) > 1}:
        errors.append(f"integrity: duplicate class_alias {dup}")
    for dup in {i for i in ids if ids.count(i) > 1}:
        errors.append(f"integrity: duplicate entity_id {dup}")
    by_alias = {e["class_alias"]: e for e in entities}

    # 3. Entity layer + building_block (dimension entities exempt)
    for e in entities:
        if "layer" not in e:
            # Dimension entity (ADR-0002 D1 — e.g. Performance Metric)
            if "building_block" in e:
                errors.append(f"integrity: {e['class_alias']} is a dimension entity but declares building_block")
            if not e.get("scope_layers"):
                errors.append(f"integrity: {e['class_alias']} is a dimension entity and must declare scope_layers")
            else:
                for sl in e["scope_layers"]:
                    if sl not in layer_ids:
                        errors.append(f"integrity: {e['class_alias']} scope_layers references unknown layer {sl}")
            continue
        if e["layer"] not in bb_by_layer:
            errors.append(f"integrity: {e['class_alias']} references unknown layer {e['layer']}")
        elif "building_block" not in e:
            errors.append(f"integrity: {e['class_alias']} has layer {e['layer']} but no building_block")
        elif e["building_block"] not in bb_by_layer[e["layer"]]:
            errors.append(
                f"integrity: {e['class_alias']} building_block {e['building_block']} "
                f"is not inside layer {e['layer']}"
            )
        if e.get("scope_layers"):
            errors.append(f"integrity: {e['class_alias']} declares scope_layers but is layer-allocated (dimension-only field)")

    # 4. Relationship endpoints
    valid = set(aliases)
    for r in rels:
        for ep in ("from", "to"):
            if r[ep] not in valid:
                errors.append(f"integrity: relationship {r['from']}->{r['to']} unknown alias {r[ep]}")

    # 5. Catalog repo required for hosted statuses
    for e in entities:
        if e["status"] in ("existing", "scaffold") and not e.get("catalog_repo"):
            errors.append(f"integrity: {e['class_alias']} status={e['status']} requires catalog_repo")

    # 6. measured_by -> dimension entity; measured layer within metric scope
    for e in entities:
        for target in e.get("measured_by", []):
            t = by_alias.get(target)
            if not t:
                errors.append(f"integrity: {e['class_alias']} measured_by unknown alias {target}")
                continue
            if "layer" in t:
                errors.append(f"integrity: {e['class_alias']} measured_by {target} but {target} is not a dimension entity")
            elif "layer" in e and t.get("scope_layers") and e["layer"] not in t["scope_layers"]:
                errors.append(
                    f"integrity: {e['class_alias']} (layer {e['layer']}) measured_by {target} "
                    f"whose scope_layers {t['scope_layers']} exclude it"
                )

    # 6b. governed_by (ADR-0003 D6) -> targets must exist and must be
    # Risk/Control/Regulation-class entities (L2-risk-compliance block).
    GOVERNANCE_BB = "L2-risk-compliance"
    for e in entities:
        for target in e.get("governed_by", []):
            t = by_alias.get(target)
            if not t:
                errors.append(f"integrity: {e['class_alias']} governed_by unknown alias {target}")
            elif t.get("building_block") != GOVERNANCE_BB:
                errors.append(
                    f"integrity: {e['class_alias']} governed_by {target} — "
                    f"governed_by must reference Risk/Control/Regulation entities ({GOVERNANCE_BB})"
                )

    # 6c. defined_by / parent_concept (ADR-0004 D2, semantic-dimension) ->
    # targets must exist and be dimension entities whose scope_layers cover
    # the source entity's layer; a Concept may not be its own parent.
    # NOTE: with >1 dimension entity (MTR, CON) the model does not declare
    # which dimension entity backs which allocator, so these checks accept
    # any dimension entity as target — same looseness as check 6.
    for e in entities:
        for field in ("defined_by",):
            for target in e.get(field, []):
                t = by_alias.get(target)
                if not t:
                    errors.append(f"integrity: {e['class_alias']} {field} unknown alias {target}")
                elif "layer" in t:
                    errors.append(f"integrity: {e['class_alias']} {field} {target} but {target} is not a dimension entity")
                elif "layer" in e and t.get("scope_layers") and e["layer"] not in t["scope_layers"]:
                    errors.append(
                        f"integrity: {e['class_alias']} (layer {e['layer']}) {field} {target} "
                        f"whose scope_layers {t['scope_layers']} exclude it"
                    )
        parent_concept = e.get("parent_concept")
        if parent_concept:
            t = by_alias.get(parent_concept)
            if not t:
                errors.append(f"integrity: {e['class_alias']} parent_concept unknown alias {parent_concept}")
            elif "layer" in t:
                errors.append(f"integrity: {e['class_alias']} parent_concept {parent_concept} but {parent_concept} is not a dimension entity")
            if parent_concept == e["class_alias"]:
                errors.append(f"integrity: {e['class_alias']} parent_concept references itself")

    # 7. specializes / abstract / realized_in_layers
    for e in entities:
        if e.get("abstract") and not e.get("realized_in_layers"):
            errors.append(f"integrity: {e['class_alias']} is abstract but declares no realized_in_layers")
        for rl in e.get("realized_in_layers", []):
            if rl not in layer_ids:
                errors.append(f"integrity: {e['class_alias']} realized_in_layers references unknown layer {rl}")
        parent_ref = e.get("specializes")
        if parent_ref:
            parent = by_alias.get(parent_ref)
            if not parent:
                errors.append(f"integrity: {e['class_alias']} specializes unknown alias {parent_ref}")
            else:
                if not parent.get("abstract"):
                    errors.append(f"integrity: {e['class_alias']} specializes {parent_ref} which is not abstract:true")
                elif "layer" in e and parent.get("realized_in_layers") and e["layer"] not in parent["realized_in_layers"]:
                    errors.append(
                        f"integrity: {e['class_alias']} (layer {e['layer']}) specializes {parent_ref} "
                        f"whose realized_in_layers {parent['realized_in_layers']} exclude it"
                    )

    # 8. Shared catalog_repo without discriminator (D6) — WARNING as of
    # v0.3.0 (user decision: models land as authored; the convention is
    # advisory until a shared repo gains real multi-entity content).
    repo_users: dict[str, list[str]] = {}
    for e in entities:
        if e.get("catalog_repo"):
            repo_users.setdefault(e["catalog_repo"], []).append(e["class_alias"])
    for repo, users in repo_users.items():
        if len(users) > 1:
            for e in entities:
                if e.get("catalog_repo") == repo and not e.get("discriminator"):
                    warnings.append(
                        f"convention: {e['class_alias']} shares catalog_repo {repo} with "
                        f"{[u for u in users if u != e['class_alias']]} but declares no discriminator (ADR-0002 D6)"
                    )

    # 9. VERSION matches model.version
    if VERSION.exists() and VERSION.read_text().strip() != model["model"]["version"]:
        errors.append(
            f"integrity: VERSION file ({VERSION.read_text().strip()}) "
            f"!= model.version ({model['model']['version']})"
        )

    n_bbs = sum(len(l["building_blocks"]) for l in layers)
    n_dims = sum(1 for e in entities if "layer" not in e)
    if errors:
        print("OpenDEAM model validation FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    if warnings:
        print("OpenDEAM model warnings (non-blocking):")
        for w in warnings:
            print(f"  ⚠ {w}")
    print(
        f"OpenDEAM model OK — {len(layers)} layers, {n_bbs} building blocks, "
        f"{len(entities)} entities ({n_dims} dimension), {len(rels)} relationships "
        f"(v{model['model']['version']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
