# CR-AR-FMWK-16: Stakeholder Status Promotion (SH)

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-16 |
| **Title** | Stakeholder status promotion: scaffold → existing (first canonical tranche landed) |
| **Status** | Proposed (this PR) |
| **Layer** | OpenDEAM (T0 root-model) |
| **Depends on** | CR-AR-FMWK-14 (promotion precedent); `dea-catalog-stakeholders` CR-CATALOG-STRUCT-12/13/14 (foundation modernization + population contract + first canonical tranche, PRs #15/#16/#17); companion metamodel promotion CR-MET-021 |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-08 |
| **Version bump** | PATCH (0.9.0 → 0.9.1) — one-line status promotion (CR-AR-FMWK-14 precedent) |

## 1. Executive summary

Promotes `dea:entity-stakeholder` (SH) `status: scaffold` → `status: existing`. The Stakeholders catalog landed its first canonical tranche on 2026-11-08: 11 canonical records — 3 organisation/governance/community capacities (the platform supplier, the OSS community, the owner's governing-board capacity) + 8 regulators one-to-one with the regulations catalog's eight active `dea:regulation-*` records (7 `enforces` + 1 `publishes`), all gates green, five workflows passing on the tranche PR. ADR-0002 D5 ladder: forward transition (`scaffold → existing`), PR-only — no ADR required.

This also resolves the drift the `check_catalog_index_matches_model` gate warns on: `scaffold` with `counts.canonical > 0` "signals the model status is stale relative to the actual catalog". The catalog side now truthfully reads `canonical: 11` under its re-vendored, hyphen-form-correct regenerator (its CR-CATALOG-STRUCT-12 foundation pass fixed the same vendored-regenerator defect family that miscounted the capabilities catalog).

## 2. Scope

### In scope

1. `model/opendeam-model.yaml`: the `dea:entity-stakeholder` allocation entry's `status` value (one line).
2. `VERSION` + `model.version` PATCH bump (0.9.0 → 0.9.1; CR-AR-FMWK-14 one-line-promotion precedent).

### Out of scope

1. The metamodel-side lifecycle mirror (`metamodel/registry/entities.yaml` et al.) — companion CR-MET-021 in `technehub-labs/dea-metamodel`.
2. Any allocation change (entity_id, alias, layer, building block are untouched — the catalog's CR-CATALOG-STRUCT-12 re-pin moved to v0.9.0 against the identical allocation).
3. Any other entity's status.

## 3. NOT-List

1. No backward transition — no ADR needed (ADR-0002 D5: forward transitions are PR-only).
2. No schema, relationship, or vocabulary change.
3. No new entity — the promotion is a one-value governance metadata change.

## 4. Acceptance criteria

- AC-01 `scripts/validate_model.py` passes (VERSION file matches `model.version`; all integrity checks green).
- AC-02 `grep -A6 "entity_id: dea:entity-stakeholder" model/opendeam-model.yaml` shows `status: existing`.
- AC-03 The repo's test suite passes (no test pins the stakeholders scaffold state on the live model — the `check_catalog_index_matches_model` tests use inline fixtures).
- AC-04 CHANGELOG entry + index row.

## 5. Promotion chain

`dea-catalog-stakeholders` CR-CATALOG-STRUCT-14 (first tranche, PR #17) → this CR (root-model status) → CR-MET-021 (metamodel lifecycle mirrors).
