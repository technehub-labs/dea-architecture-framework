#!/usr/bin/env python3
"""Validate a consumer repo's allocation declaration against the OpenDEAM model.

Used by the reusable workflow validate-against-model.yml: consumer repos
(e.g. dea-catalog-*) declare their entity allocation in metamodel-pointer.yaml;
this script checks that declaration against the pinned model.

v0.2.0 (ADR-0002): dimension entities (no home layer, e.g. Performance Metric)
declare `metamodel.dimension: <allocator-id>` instead of `metamodel.layer`.

v0.6.0 (CR-AR-FMWK-01): abstract kernels (e.g. dea:entity-process) declared
in the root model with `abstract: true` are realized by their specializations
(e.g. dea:entity-business-process). The pointer may declare the kernel id
standalone (in a multi-entity `entities:` list) without declaring a layer or
dimension; the class_alias and discriminator checks still apply.

Usage:
  python3 validate_consumer.py --model model/opendeam-model.yaml \
      --pointer path/to/metamodel-pointer.yaml

Checks:
  1. pointer.metamodel.entity_id exists in the model.
  2. Layer-allocated entities: pointer.metamodel.layer matches the model.
     Dimension entities: pointer.metamodel.dimension names an orthogonal
     allocator declared by the model.
     Abstract kernels: pointer must NOT declare layer or dimension.
  3. pointer.metamodel.class_alias matches the model.
  4. pointer.metamodel.version is a well-formed pin (vX.Y.Z[-tag]).
  5. Discriminator (ADR-0002 D6): shared catalog_repo entities must declare
     the discriminator in the pointer.

Exit: 0 = consistent, 1 = drift detected (messages on stdout).
"""
import argparse
import re
import sys
from pathlib import Path

import yaml


def check_one(mm: dict, by_id: dict, allocator_ids: set, label: str, errors: list[str]) -> None:
    """Validate one metamodel declaration (single-entity `metamodel:` block or
    one entry of a multi-entity `entities:` list) against the model."""
    entity_id = mm.get("entity_id")
    if not entity_id:
        errors.append(f"{label}: missing entity_id")
        return
    if entity_id not in by_id:
        errors.append(f"drift: {label} entity_id {entity_id} not in OpenDEAM model")
        return
    canon = by_id[entity_id]
    if canon.get("abstract"):
        # Abstract kernel (CR-AR-FMWK-01; mirrors ADR-0005 D3 Resource template).
        # An abstract kernel is layer-allocated in the model (Resource kernel
        # precedent) but its concrete instances (specializations) carry the
        # context. The pointer declares the kernel id (typically in a
        # multi-entity `entities:` list) without claiming a layer or dimension
        # of its own; the consumer must NOT declare a layer or dimension for
        # the kernel itself (the kernel's purpose is to be realized by
        # specializations, not allocated to a layer directly).
        if mm.get("layer"):
            errors.append(
                f"drift: {entity_id} is an abstract kernel in the model; "
                f"{label} should not declare layer={mm.get('layer')} "
                f"(the kernel is realized by its specializations)"
            )
        if mm.get("dimension"):
            errors.append(
                f"drift: {entity_id} is an abstract kernel in the model; "
                f"{label} should not declare dimension={mm.get('dimension')}"
            )
    elif "layer" in canon:
        if mm.get("layer") != canon["layer"]:
            errors.append(
                f"drift: {entity_id} layer={mm.get('layer')} in {label}, "
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
                f"{label} must declare dimension (e.g. measurement-dimension), not layer"
            )
        elif dim not in allocator_ids:
            errors.append(
                f"drift: {entity_id} dimension={dim} in {label}, "
                f"model declares orthogonal_allocators {sorted(allocator_ids)}"
            )
        if mm.get("layer"):
            errors.append(f"drift: {entity_id} declares layer={mm.get('layer')} but model treats it as a dimension entity")
    if mm.get("class_alias") != canon["class_alias"]:
        errors.append(
            f"drift: {entity_id} class_alias={mm.get('class_alias')} in {label}, "
            f"model says {canon['class_alias']}"
        )
    # Shared catalog_repo (ADR-0002 D6): if the entity declares a discriminator
    # in the model, the pointer should declare it too.
    if canon.get("discriminator") and not mm.get("discriminator"):
        errors.append(
            f"drift: {entity_id} model requires discriminator '{canon['discriminator']}' "
            f"(shared catalog_repo); {label} does not declare it"
        )


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

    # Multi-entity pointers (shared catalog_repo per ADR-0002 D6):
    # an optional top-level `entities:` list validates each entry; the
    # primary `metamodel:` block is validated as before.
    extra = pointer.get("entities") or []
    for i, entry in enumerate(extra):
        check_one(entry, by_id, allocator_ids, f"entities[{i}]", errors)

    if not entity_id and not extra:
        errors.append("pointer: missing metamodel.entity_id")
    elif entity_id:
        check_one(mm, by_id, allocator_ids, "pointer metamodel", errors)

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
