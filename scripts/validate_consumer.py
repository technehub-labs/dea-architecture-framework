#!/usr/bin/env python3
"""Validate a consumer repo's allocation declaration against the OpenDEAM model.

Used by the reusable workflow validate-against-model.yml: consumer repos
(e.g. dea-catalog-*) declare their entity allocation in metamodel-pointer.yaml;
this script checks that declaration against the pinned model.

v0.2.0 (ADR-0002): dimension entities (no home layer, e.g. Performance Metric)
declare `metamodel.dimension: <allocator-id>` instead of `metamodel.layer`.

Usage:
  python3 validate_consumer.py --model model/opendeam-model.yaml \
      --pointer path/to/metamodel-pointer.yaml

Checks:
  1. pointer.metamodel.entity_id exists in the model.
  2. Layer-allocated entities: pointer.metamodel.layer matches the model.
     Dimension entities: pointer.metamodel.dimension names an orthogonal
     allocator declared by the model.
  3. pointer.metamodel.class_alias matches the model.
  4. pointer.metamodel.version is a well-formed pin (vX.Y.Z[-tag]).

Exit: 0 = consistent, 1 = drift detected (messages on stdout).
"""
import argparse
import re
import sys
from pathlib import Path

import yaml


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, type=Path)
    ap.add_argument("--pointer", required=True, type=Path)
    args = ap.parse_args()

    model = yaml.safe_load(args.model.read_text())
    pointer = yaml.safe_load(args.pointer.read_text())

    errors: list[str] = []
    by_id = {e["entity_id"]: e for e in model["allocation"]["entities"]}
    allocator_ids = {a["id"] for a in model["architecture"].get("orthogonal_allocators", [])}

    mm = pointer.get("metamodel", {})
    entity_id = mm.get("entity_id")
    if not entity_id:
        errors.append("pointer: missing metamodel.entity_id")
    elif entity_id not in by_id:
        errors.append(f"drift: entity_id {entity_id} not in OpenDEAM model")
    else:
        canon = by_id[entity_id]
        if "layer" in canon:
            if mm.get("layer") != canon["layer"]:
                errors.append(
                    f"drift: {entity_id} layer={mm.get('layer')} in pointer, "
                    f"model says {canon['layer']} ({canon['display_name']})"
                )
            if mm.get("dimension"):
                errors.append(f"drift: {entity_id} declares dimension but model allocates it to layer {canon['layer']}")
        else:
            # Dimension entity (ADR-0002 D1)
            dim = mm.get("dimension")
            if not dim:
                errors.append(
                    f"drift: {entity_id} is a dimension entity in the model; "
                    f"pointer must declare metamodel.dimension (e.g. measurement-dimension), not layer"
                )
            elif dim not in allocator_ids:
                errors.append(
                    f"drift: {entity_id} dimension={dim} in pointer, "
                    f"model declares orthogonal_allocators {sorted(allocator_ids)}"
                )
            if mm.get("layer"):
                errors.append(f"drift: {entity_id} declares layer={mm.get('layer')} but model treats it as a dimension entity")
        if mm.get("class_alias") != canon["class_alias"]:
            errors.append(
                f"drift: {entity_id} class_alias={mm.get('class_alias')} in pointer, "
                f"model says {canon['class_alias']}"
            )

    version = str(mm.get("version", ""))
    if not re.fullmatch(r"v\d+\.\d+\.\d+(-[a-z0-9.]+)?", version):
        errors.append(f"pointer: metamodel.version '{version}' is not a well-formed pin (vX.Y.Z[-tag])")

    name = pointer.get("catalog", {}).get("name", args.pointer)
    if errors:
        print(f"Consumer validation FAILED for {name}:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(f"Consumer {name} consistent with OpenDEAM v{model['model']['version']} ({entity_id})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
