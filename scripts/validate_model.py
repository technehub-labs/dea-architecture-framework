#!/usr/bin/env python3
"""Validate model/opendeam-model.yaml — schema + referential integrity.

Checks beyond JSON Schema:
  1. Layer IDs are unique and sequential (L1..Ln).
  2. class_alias and entity_id are globally unique.
  3. Every entity's layer exists; every entity's building_block exists
     INSIDE that layer (not just anywhere).
  4. Every relationship endpoint resolves to a declared class_alias.
  5. Entities with status 'existing'/'scaffold' must declare a catalog_repo.
  6. VERSION file matches model.version.

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

    # 3. Entity layer + building_block (must live INSIDE the entity's layer)
    for e in entities:
        if e["layer"] not in bb_by_layer:
            errors.append(f"integrity: {e['class_alias']} references unknown layer {e['layer']}")
        elif e["building_block"] not in bb_by_layer[e["layer"]]:
            errors.append(
                f"integrity: {e['class_alias']} building_block {e['building_block']} "
                f"is not inside layer {e['layer']}"
            )

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

    # 6. VERSION matches model.version
    if VERSION.exists() and VERSION.read_text().strip() != model["model"]["version"]:
        errors.append(
            f"integrity: VERSION file ({VERSION.read_text().strip()}) "
            f"!= model.version ({model['model']['version']})"
        )

    if errors:
        print("OpenDEAM model validation FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(
        f"OpenDEAM model OK — {len(layers)} layers, "
        f"{sum(len(l['building_blocks']) for l in layers)} building blocks, "
        f"{len(entities)} entities, {len(rels)} relationships "
        f"(v{model['model']['version']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
