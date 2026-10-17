# CR-AR-FMWK-04: Information Systems Entity Allocation and Relationship Integration

| Field | Value |
|-------|-------|
| **CR** | CR-AR-FMWK-04 |
| **Title** | Information Systems Entity Allocation and Relationship Integration (post-CR-022 closure) |
| **Status** | Proposed (this PR) |
| **Layer** | OpenDEAM (T0 root-model) |
| **Programme** | Information Systems Semantic Architecture |
| **Architectural parent** | CR-AR-FMWK-03 (entity-system cross-reference; merged 2026-10-15+); CR-AR-FMWK-02 (authorship cardinal rule R1, R2; merged 2026-10-15+) |
| **Companion to** | CR-017 (dea-metamodel foundation, merged 2026-10-16); CR-018 (ISF, merged); CR-019 (ISC, merged); CR-020 (ISS, merged); CR-021 (II, merged); CR-022 (metamodel closure, merged 2026-10-16) |
| **Depends on** | CR-AR-FMWK-03; CR-AR-FMWK-02; CR-017; CR-018; CR-019; CR-020; CR-021; CR-022 (all merged); `CR-012 (dea-governance)` + DEA-ID-000 (when accepted) |
| **Enables** | CR-IS-CAT-01..04 (catalog renames + new catalogs); `CR-013 (dea-governance)` portfolio adoption (closure gate) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-16 |

## 1. Executive Summary

This CR extends the OpenDEAM root model with the four new Digital Profile entities introduced in the IS Semantic Architecture programme (CR-017..CR-022) and the new `dea:specifies` relationship introduced in CR-021. It is the first cross-repo CR in Path Y, landing in `technehub-labs/dea-architecture-framework` after the metamodel-side slice of Path Y is closed on `main`.

The OpenDEAM model is bumped from v0.6.0 to v0.7.0. The four new entities are allocated to L5 with appropriate building blocks (L5-systems for ISC and ISF; L5-integration for ISS and II). The new `contract` rel_type is added to the controlled vocabulary, mirroring the new `contract` category (category M) in the metamodel CATEGORIES set. Two other rel_types are added: `execution` (ISC executes ISF) and `serving` (ISC provides ISS; ISS exposed via IF). The OpenDEAM-to-metamodel identifier map is consumed from the dea-metamodel closure document and reproduced in the OpenDEAM-side closure document at `docs/is-semantic-architecture/opendeam-identifier-map.yaml`.

The migration path is recorded: `dea:entity-system-function` (legacy SF) is retained in OpenDEAM for EGV-004 identity continuity; the new `dea:entity-information-system-function` (ISF) supersedes it. The class alias `II` (Investment Initiative) is preserved; the new `dea:entity-integration-interface` is allocated the alias `IF` to avoid collision.

## 2. Scope

### 2.1 In scope

1. The four new entity allocations in `model/opendeam-model.yaml`:
   - `dea:entity-information-system-function` (ISF; L5/L5-systems; supersedes `dea:entity-system-function`).
   - `dea:entity-information-system-component` (ISC; L5/L5-systems; abstract; specialises SC).
   - `dea:entity-information-system-service` (ISS; L5/L5-integration).
   - `dea:entity-integration-interface` (IF; L5/L5-integration; class alias `IF` to avoid `II` collision with Investment Initiative).
2. Eight new relationships in the OpenDEAM architectural graph:
   - `ISF` → `ISC` (executed by; realization)
   - `ISC` → `ISF` (executes; execution)
   - `ISC` → `ISC` (composed of; composition)
   - `ISC` → `ISS` (provides; serving)
   - `ISS` → `IF` (exposed via; serving)
   - `API` → `IF` (specifies; contract, the new `dea:specifies` relationship from CR-021)
   - `ISS` → `PS` (specializes conditional per D-3; realization)
   - `ISC` → `APC` (specializes; realization)
   - `ISC` → `IGC` (specializes; realization)
3. Three new `rel_type` controlled vocabulary values: `execution`, `serving`, `contract`.
4. The OpenDEAM-to-metamodel identifier map at `docs/is-semantic-architecture/opendeam-identifier-map.yaml` (10 mappings + 6 notes; the canonical map for the IS programme).
5. The OpenDEAM model version bump from v0.6.0 to v0.7.0; the `VERSION` file updated to `0.7.0`.
6. The `schemas/opendeam-model.schema.json` rel_type enum extended with the three new values.
7. The CR-AR-FMWK-04 doc (this file).
8. `change-requests/README.md` row for CR-AR-FMWK-04.

### 2.2 Out of scope

1. The new catalog repositories (`dea-catalog-information-system-functions`, `dea-catalog-information-system-components`, `dea-catalog-information-system-services`, `dea-catalog-information-system-integration-interfaces`). Owned by `CR-IS-CAT-01..04` after CR-AR-FMWK-04 lands.
2. The governance portfolio registration. Owned by `CR-013 (dea-governance)`.
3. The TTL/SQLite/Pydantic/TypeScript artefacts for the new OpenDEAM relationships. OpenDEAM does not generate these; the metamodel is the source of truth and the metamodel already has them (per CR-022).
4. The OpenDEAM architecture viewer regeneration. Owned by the viewer project; CR-AR-FMWK-04 records the changes; the viewer team is informed via the kanban surface.

## 3. Entity Allocations

The four new entities are allocated to L5 with the following layer/building-block assignments:

| Entity | Layer | Building Block | Class Alias | Specialises | Catalog |
|---|---|---|---|---|---|
| `dea:entity-information-system-function` | L5 | L5-systems | ISF | (Core `dea:Behavior`) | dea-catalog-information-system-functions |
| `dea:entity-information-system-component` | L5 | L5-systems | ISC | (SC) | dea-catalog-information-system-components |
| `dea:entity-information-system-service` | L5 | L5-integration | ISS | (Core `dea:entity-service`) | dea-catalog-information-system-services |
| `dea:entity-integration-interface` | L5 | L5-integration | IF | (none) | dea-catalog-information-system-integration-interfaces |

The `specialises` field is recorded where applicable. For `ISF` and `ISS`, the parent is a Core entity (not allocated to OpenDEAM); the specialisation is recorded in the metamodel only. For `ISC`, the parent is `SC` (allocated to L3); the specialisation is recorded in the OpenDEAM allocation block. For `IF`, no specialisation; the entity is a first-class L5 entity.

The class alias `IF` is chosen to avoid the collision with the existing `II` (Investment Initiative) alias. The metamodel's class alias `II` for `dea:IntegrationInterface` is preserved; the OpenDEAM alias is the MECE-distinct local alias.

## 4. Relationship Architecture

The eight new relationships added to the OpenDEAM architectural graph:

| From | To | Label | rel_type | Cardinality | CR |
|---|---|---|---|---|---|
| ISF | ISC | executed by | realization | 0..N:1..N | CR-019 |
| ISC | ISF | executes | execution | 1:0..N | CR-019 |
| ISC | ISC | composed of | composition | 1:0..N | CR-019 |
| ISC | ISS | provides | serving | 1:0..N | CR-020 |
| ISS | IF | exposed via | serving | 1:0..N | CR-021 |
| API | IF | specifies | contract | 0..N:0..N | CR-021 (D-4) |
| ISS | PS | specializes (conditional per D-3) | realization | 0..N:0..N | CR-020 (D-3) |
| ISC | APC | specializes | realization | 0..N:0..N | CR-019 |
| ISC | IGC | specializes | realization | 0..N:0..N | CR-019 |

The new `contract` rel_type mirrors the new `contract` category (category M) in the metamodel CATEGORIES set (introduced in CR-021). The new `execution` and `serving` rel_types are OpenDEAM-side rel_type values that mirror the metamodel's `dea:executes`, `dea:provides`, `dea:exposes`, and `dea:uses` relationship categories.

The eight new relationships are recorded in the OpenDEAM `relationships:` block at the end of the model file. Each relationship uses the compact one-liner format `{from: ALIAS, to: ALIAS, label: LABEL, rel_type: TYPE, cardinality: "X..Y:Z..W"}` to match the existing pattern.

## 5. OpenDEAM-to-Metamodel Identifier Map

The canonical identifier map is at `docs/is-semantic-architecture/opendeam-identifier-map.yaml`. It contains 10 mappings:

- 4 mappings for the four new Digital Profile entities (ISF, ISC, ISS, IF).
- 5 mappings for the reconciled entities (SystemFunction, SolutionComponent, ApplicationComponent, IntegrationComponent, InfrastructureComponent, PlatformService, API) : note that the count is higher than 4 because some entities map to multiple canonical ids (e.g., ApplicationComponent maps to APC in OpenDEAM and to dea:ApplicationComponent in the metamodel).
- 3 mappings for OpenDEAM-only entities (BusinessService, Technology, BusinessProcess) that have no IS programme mapping.

The map is consumed by `CR-IS-CAT-01..04` and the `CR-013 (dea-governance)` portfolio adoption.

## 6. Controlled Vocabulary Expansion

The rel_type controlled vocabulary in the OpenDEAM model is extended with three new values:

| rel_type | Definition | Source |
|---|---|---|
| `execution` | The source executes the target (e.g., ISC executes ISF). Mirrors the metamodel's `dea:executes` relationship. | CR-019 (D-2) |
| `serving` | The source makes the target available to consumers (e.g., ISC provides ISS; ISS exposed via IF). Mirrors the metamodel's `dea:provides` and `dea:exposes` relationships. | CR-020 (D-3) + CR-021 (D-4) |
| `contract` | The source is a contract that specifies the target (e.g., API specifies IF). Mirrors the metamodel's new `dea:specifies` relationship and the new `contract` category (M). | CR-021 (D-4) |

The schema at `schemas/opendeam-model.schema.json` is updated to permit the three new rel_types in the enum.

## 7. Migration and Compatibility

This is a **minor** version impact: the model is bumped from v0.6.0 to v0.7.0. The four new entity allocations are additive. The legacy `dea:entity-system-function` (class alias SF) is retained for EGV-004 identity continuity; new models should use `dea:entity-information-system-function` (class alias ISF).

The class alias `IF` for `dea:entity-integration-interface` is the OpenDEAM-side alias; the metamodel-side alias remains `II`. Viewers that use the class_alias as a key should be aware of the local mapping.

## 8. Validation

Local CI verification:

- `python3 scripts/validate_model.py` PASS (warnings only; no errors; "5 layers, 27 building blocks, 58 entities (2 dimension), 79 relationships (v0.7.0)").
- `python3 scripts/check_authorship.py` PASS (AUT-001/002/003 = 0).
- `python3 -m pytest tests/test_check_authorship.py` PASS (21/21).
- `python3 -m pytest tests/test_check_catalog_index_matches_model.py` SKIP (pre-existing PyYAML install issue in the local environment; not introduced by CR-AR-FMWK-04).

## 9. Cross-Repository Impact

| Repository | Required alignment |
|---|---|
| `technehub-labs/dea-metamodel` | No action; CR-022 has already closed the metamodel side. |
| `technehub-labs/dea-governance` | `CR-013 (dea-governance)` registers the four new entities in the portfolio. |
| `technehub-labs/dea-catalog-system-functions` → `dea-catalog-information-system-functions` | `CR-IS-CAT-01` renames the existing catalog. |
| `technehub-labs/dea-catalog-application-components` → `dea-catalog-information-system-components` | `CR-IS-CAT-02` renames the existing catalog. |
| `technehub-labs/dea-catalog-platform-services` + new `dea-catalog-information-system-services` | `CR-IS-CAT-03` establishes the new catalog. |
| `technehub-labs/dea-catalog-api-contracts` + new `dea-catalog-information-system-integration-interfaces` | `CR-IS-CAT-04` extends the existing catalog and establishes the new interface catalog. |

## 10. Acceptance Criteria

- [ ] Four new entity allocations in `model/opendeam-model.yaml`.
- [ ] Eight new relationships in the OpenDEAM `relationships:` block.
- [ ] Three new rel_type controlled vocabulary values in `schemas/opendeam-model.schema.json`.
- [ ] OpenDEAM model version bumped from v0.6.0 to v0.7.0.
- [ ] `VERSION` file updated to `0.7.0`.
- [ ] OpenDEAM-to-metamodel identifier map at `docs/is-semantic-architecture/opendeam-identifier-map.yaml`.
- [ ] `scripts/validate_model.py` PASS.
- [ ] `scripts/check_authorship.py` PASS (AUT-001/002/003 = 0).
- [ ] Cardinal author rule satisfied: `Author: Emmanuel A. Otchere` per CR-AR-FMWK-02.
- [ ] D-004 / D-005 / Standardization-body embargo clean.

## 11. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Class alias collision (II for both Investment Initiative and IntegrationInterface) | CR-AR-FMWK-04 uses `IF` for the OpenDEAM alias; the metamodel's `II` alias is preserved. The class_alias mapping is documented in the OpenDEAM-to-metamodel identifier map. |
| OpenDEAM viewer regeneration | The viewer team is informed via the kanban surface; CR-AR-FMWK-04 records the changes; the viewer is regenerated as part of the cross-repo consumer workflow. |
| Cross-repo coupling | The OpenDEAM-to-metamodel identifier map is the bridge; both repos carry the map. The dea-metamodel stub is consumed by CR-AR-FMWK-04 and the catalog CRs. |
| New rel_type vocabulary expansion | The expansion is documented in §6; the schema is updated; the controlled vocabulary remains closed (three new values added in a controlled manner). |
| Generated artifact drift | The OpenDEAM model is the source of truth; the schema and validators are updated in this PR. |
| Author confusion (CR-AR-FMWK-02 R1) | The authorship header is preserved (Emmanuel A. Otchere, emmanuel@otchere.com); `check_authorship.py` enforces. |

## 12. Completion Definition

CR-AR-FMWK-04 is complete when:

1. The four new entity allocations are present in `model/opendeam-model.yaml`.
2. The eight new relationships are present in the OpenDEAM `relationships:` block.
3. The three new rel_type values are in `schemas/opendeam-model.schema.json`.
4. The OpenDEAM model version is v0.7.0; `VERSION` is `0.7.0`.
5. The OpenDEAM-to-metamodel identifier map is at `docs/is-semantic-architecture/opendeam-identifier-map.yaml`.
6. Local CI checks pass (`validate_model.py`, `check_authorship.py`, `test_check_authorship.py`).
7. PR opens against `origin/main`; CI on GitHub Actions shows green before user review.

## 13. Path Y Completion (after this PR merges)

After CR-AR-FMWK-04 lands, the remaining Path Y work is the catalog cascade:

1. `CR-IS-CAT-01` (rename `dea-catalog-system-functions` to `dea-catalog-information-system-functions`; extend).
2. `CR-IS-CAT-02` (rename `dea-catalog-application-components` to `dea-catalog-information-system-components`; extend).
3. `CR-IS-CAT-03` (establish new `dea-catalog-information-system-services`).
4. `CR-IS-CAT-04` (establish new `dea-catalog-information-system-integration-interfaces`; extend `dea-catalog-api-contracts`).
5. `CR-013 (dea-governance)` portfolio adoption as the closure gate.

## 14. References

### 14.1 Inputs and authorities

- `technehub-labs/dea-architecture-framework/change-requests/CR-AR-FMWK-03.md` (entity-system cross-reference; merged 2026-10-15+)
- `technehub-labs/dea-architecture-framework/change-requests/CR-AR-FMWK-02.md` (authorship cardinal rule R1, R2; merged 2026-10-15+)
- `technehub-labs/dea-metamodel/change-requests/CR-017-information-systems-domain-semantic-integration.md` (foundation; merged 2026-10-16)
- `technehub-labs/dea-metamodel/change-requests/CR-018-information-system-function.md` (ISF; merged)
- `technehub-labs/dea-metamodel/change-requests/CR-019-information-system-component.md` (ISC; merged)
- `technehub-labs/dea-metamodel/change-requests/CR-020-information-system-service.md` (ISS; merged)
- `technehub-labs/dea-metamodel/change-requests/CR-021-integration-interface.md` (II; merged)
- `technehub-labs/dea-metamodel/change-requests/CR-022-metamodel-artifact-and-conformance-closure.md` (closure; merged 2026-10-16)
- `technehub-labs/dea-metamodel/docs/is-semantic-architecture/opendeam-identifier-map.yaml` (the consumed stub; the canonical map is in this repo)

### 14.2 Companion Kanban surface

- Project 23 (DEAMMISE) at `/board/23`: card #392 (CR-AR-FMWK-04), In Progress during authoring
- Companion umbrella carrier #384
- DRIFT-4 card #419 (InfrastructureComponent placement; recorded in CR-019)
- DRIFT-5 (TypeScript RelationshipType union) and DRIFT-6 (TTL generator) recorded in CR-022; cards pending
- Per-channel skill at `~/.hermes/profiles/coder/skills/dea-is-semantic-arch-kanban-discipline/SKILL.md`
- Snapshot doc at `~/.hermes/profiles/coder/kanban/dea-metamodel-is-snapshot-2026-10-16.md`

---

End of CR-AR-FMWK-04.
