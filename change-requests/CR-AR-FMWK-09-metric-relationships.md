# CR-AR-FMWK-09: Metric Programme Relationships (root-model slice)

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-09 |
| **Title** | Metric Programme Relationships: the intra-capability edges for the twelve Metric dimension entities |
| **Status** | Proposed (this PR) |
| **Type** | Relationship allocation (additive); no entity change |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Predecessor** | CR-AR-FMWK-05 (Metric entity allocation, PR #18): "Relationship allocation is deliberately deferred to a follow-on CR so that this one stays reviewable and reversible" — this is that follow-on |
| **Authority** | `dea-metamodel` docs/metric-capability-map.md §4 — the canonical 23-relationship metric capability; this CR is the root-model translation, not a re-authoring |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. Change Request

Add **24 relationships** to `model/opendeam-model.yaml` under
`relationships:` — the intra-capability edges connecting the twelve
Metric dimension entities (allocated by CR-AR-FMWK-05) to each other
and to `MTR` (Performance Metric). No entity entry changes; no
existing relationship changes.

## 2. Translation rule

The metamodel defines 23 canonical relationships touching the
capability, but OpenDEAM's `rel_type` vocabulary is closed (10 values:
realization, composition, aggregation, dependency, flow, governance,
association, execution, serving, contract — CR-AR-FMWK-04 precedent).
This CR does **not** extend the vocabulary. Each metamodel edge is
mapped to the closest existing `rel_type` by function:

| Metamodel function | OpenDEAM rel_type |
|---|---|
| produces, derives-from, analyses-metric | `dependency` |
| applies-metric, applies-subject, measures-subject, measured-by | `governance` |
| has-provenance, has-designation, references, specifies-target, has-target, applies-period, constrains, informs-decision | `governance` |
| corrects, supersedes | `dependency` |
| correlates, tests-hypothesis | `association` |
| interprets | `dependency` |
| benchmarked-against | `association` |
| specializes (ReportingPeriod → TemporalInterval) | **out of scope** — no `TIV` entity in OpenDEAM |

Two metamodel edges land on the same OpenDEAM edge (the 3-subject /
16-target design-vs-runtime pattern collapses to one `applies`
governance edge), producing 24 OpenDEAM edges from 23 metamodel
relationships; the `specializes` edge is out of scope because OpenDEAM
does not allocate Core metamodel entities (CR-AR-FMWK-04 D-3
precedent).

## 3. The 24 edges

| # | from | to | label | rel_type | cardinality | Source (metamodel) |
|---|---|---|---|---|---|---|
| 1 | MTR | MMT | applies metric | governance | 0..1:0..N | applies-metric |
| 2 | MMT | MOBS | produces | dependency | 1:0..N | produces |
| 3 | MMT | PRV | has provenance | governance | 1:0..1 | has-provenance |
| 4 | MOBS | PRV | has provenance | governance | 1:0..1 | has-provenance |
| 5 | MTR | PRV | has provenance | governance | 0..1:0..1 | has-provenance |
| 6 | MOBS | MOBS | corrects | dependency | 0..N:0..N | corrects |
| 7 | MTR | SO | applies to | governance | 0..1:0..N | applies-subject |
| 8 | MMT | SO | measures subject | governance | 1:0..N | measures-subject |
| 9 | MTR | BSL | references baseline | governance | 0..N:0..N | references |
| 10 | MTR | PTG | specifies target | governance | 0..1:0..N | specifies-target |
| 11 | SO | PTG | has target | governance | 0..N:0..N | has-target |
| 12 | MMT | RPT | applies period | governance | 1:0..N | applies-period |
| 13 | MOBS | RPT | applies period | governance | 1:0..N | applies-period |
| 14 | BSL | RPT | applies period | governance | 1:0..N | applies-period |
| 15 | PTG | RPT | applies period | governance | 1:0..N | applies-period |
| 16 | THR | RPT | applies period | governance | 1:0..N | applies-period |
| 17 | PIT | RPT | applies period | governance | 1:0..N | applies-period |
| 18 | IDS | RPT | applies period | governance | 1:0..N | applies-period |
| 19 | PIT | MOBS | interprets | dependency | 0..N:0..N | interprets |
| 20 | THR | MTR | constrains | governance | 0..N:0..N | constrains |
| 21 | MTR | IDS | has designation | governance | 0..1:0..N | has-designation |
| 22 | ANR | MTR | analyses metric | dependency | 0..N:0..N | analyses-metric |
| 23 | COR | CSH | tests hypothesis | association | 0..N:0..N | tests-hypothesis |
| 24 | COR | MTR | correlates with | association | 0..N:0..N | correlates |

Edge 6 (`MOBS → MOBS corrects`) is a self-edge — a correction restates
a prior observation of the same type. The validator has no
self-edge prohibition (checked); `cardinality 0..N:0..N` reflects
that any observation may correct or be corrected.

## 4. Out-of-scope metamodel edges (documented for the record)

| Metamodel edge | Why not in this CR |
|---|---|
| `measured-by` / `assessed-by` extensions (16 source types) | These are integration-surface extensions on pre-existing OpenDEAM entities (e.g. `measured_by` field on AIM, BC); the OpenDEAM-side wire already exists via `measured_by` fields and the `SO/CAP/SF → MTR` edges. Extending to all 16 types belongs to a follow-on CR touching entity entries, not relationships. |
| `constrains` on Requirement/Guardrail/Regulation/Constraint | Pre-existing governance edges outside the metric capability. |
| `benchmarked-against` peer metrics | No benchmark-peer entity in OpenDEAM; would require `AssessmentResult`/`Technology` endpoints that are not OpenDEAM entities. |
| `informs-decision` → `dea:Decision` | No Decision entity in OpenDEAM (Core metamodel entity; OpenDEAM does not allocate Core entities — CR-AR-FMWK-04 D-3). |
| `derives-from` evidence chain | Runtime instance-level fact (observation provenance chain), already represented structurally by edges 3-5 and 19. |
| `supersedes` (10-type) | Cross-cutting lifecycle relation, not metric-specific; an OpenDEAM-wide `supersedes` vocabulary question deferred to its own CR. |
| `specializes` (ReportingPeriod → TemporalInterval) | No `TIV` in OpenDEAM (Core entity). |

## 5. Version impact

**Additive relationship allocation** — same class as
CR-AR-FMWK-04's edge work: **PR + patch bump**: v0.7.4 → v0.7.5. No
ADR, no minor bump. No rel_type vocabulary change.

This CR is based on the v0.7.4 stack tip (`vibe/skl-chi-status-promotion-cr`,
carrying the merged #20/#21 stack; landing on main via PR #23). Merge
#23 first; this PR bases against main after that and the version chain
v0.7.2 → v0.7.3 → v0.7.4 → v0.7.5 stays linear.

## 6. Consumer-side prerequisite

Same as CR-AR-FMWK-05 §6: the viewer generator resolves a dimension
entity's allocator through `DIMENSION_ALLOCATOR` in `dea-metamodel`
(PR #196, merged). Edges among dimension entities render once both
endpoints render; no new consumer change is required for these edges.

## 7. Definition of done

- [ ] 24 edges added to `relationships:` in `model/opendeam-model.yaml`
- [ ] Zero entity entries changed; zero pre-existing edges changed
- [ ] `rel_type` vocabulary unchanged (10 values)
- [ ] `VERSION` → `0.7.5`
- [ ] `model.version` → `0.7.5`
- [ ] `scripts/validate_model.py` PASS (expect 103 relationships)
- [ ] `scripts/check_authorship.py` PASS (AUT-001/002/003 = 0)
- [ ] `model-ci.yml` green
- [ ] This CR registered in `change-requests/README.md`
- [ ] PR #23 (stack reconciliation) merged first

## 8. Out of scope

- Any change to the twelve Metric entity entries or to `MTR`
- The 16-type `measured-by`/`assessed-by` integration surface (follow-on CR)
- An OpenDEAM-wide `supersedes` relationship vocabulary question
- Any rel_type vocabulary expansion
- Metric entity lifecycle promotions (dimension semantics deferred, per CR-AR-FMWK-08 §8)

## 9. Cross-references

- `dea-metamodel` docs/metric-capability-map.md §4 (canonical authority, 23 relationships)
- CR-AR-FMWK-05 (`change-requests/CR-AR-FMWK-05-metric-entity-allocation.md`, PR #18) — entity allocation this CR wires
- `dea-metamodel` viewer/entity-graph.json (binding of record)
- PR #23 (stack reconciliation, lands v0.7.4 on main)
- ADR-0002 D1 (measurement is a dimension, not a layer)
