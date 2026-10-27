# CR-AR-FMWK-11: Metric Dimension-Entity Lifecycle Promotion (proposed → planned)

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-11 |
| **Title** | Metric Dimension-Entity Lifecycle Promotion: the twelve Metric dimension entities, proposed → planned |
| **Status** | Proposed (this PR) |
| **Type** | Lifecycle status transition (forward) + documented governance convention for dimension entities |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Predecessor** | CR-AR-FMWK-08 §8 (deferred the dimension-entity lifecycle question); CR-AR-FMWK-05 (allocated the twelve with `catalog_repo: null` by design); CR-AR-FMWK-09 (wired 24 edges) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. The governance question CR-AR-FMWK-08 deferred

Do dimension entities follow the catalog-content status↔content
contract at all? The STRUCT-07c smoke test keys on `catalog_repo`,
and dimension entities deliberately carry `catalog_repo: null`
(CR-AR-FMWK-05 §3: instances of these types live in the metrics
catalog governed by `MTR`'s schema, not in per-entity repositories).

**Answer, recorded here as the governing convention:**

> Dimension entities follow the same ordered lifecycle states as
> layer-allocated entities, but their status expresses **programme
> commitment**, not catalog-content backing. A dimension entity is
> `proposed` when it is a candidate; `planned` when it is admitted,
> allocated, and wired into the model (committed, no per-entity
> catalog by design); `scaffold`/`existing` never apply to a
> `catalog_repo: null` dimension entity unless a per-entity catalog
> is later chartered — the catalog-content contract activates only
> when a `catalog_repo` exists.

The rationale: the validator already enforces the boundary
structurally (rule 5: `existing`/`scaffold` require `catalog_repo`;
dimension entities with `catalog_repo: null` can only occupy
`proposed` or `planned`). This CR documents that as intent rather
than leaving it as an implicit validator side-effect.

No new validator rule is needed. Rule 5 already enforces exactly
this convention; a `planned` dimension entity without a
`catalog_repo` passes, and any future attempt to promote one to
`scaffold`/`existing` without chartering a catalog will fail the
gate. The convention is self-enforcing.

## 2. Change Request

Update `model/opendeam-model.yaml` `allocation.entities`: flip
`status: proposed` → `status: planned` on the twelve Metric
dimension entities allocated by CR-AR-FMWK-05:

| Entity | Alias |
|---|---|
| `dea:entity-measurement` | MMT |
| `dea:entity-measurement-observation` | MOBS |
| `dea:entity-indicator-designation` | IDS |
| `dea:entity-baseline` | BSL |
| `dea:entity-performance-target` | PTG |
| `dea:entity-threshold` | THR |
| `dea:entity-performance-interpretation` | PIT |
| `dea:entity-reporting-period` | RPT |
| `dea:entity-provenance` | PRV |
| `dea:entity-analytical-result` | ANR |
| `dea:entity-correlation` | COR |
| `dea:entity-causal-hypothesis` | CSH |

Exactly one field per entry; nothing else changes.

## 3. Why `planned` is the correct state

The evidence class differs from CR-AR-FMWK-06/07/08 (no catalog
repo to check) but the signal is stronger, not weaker:

- **Admitted**: each entity was admitted by its own metamodel CR
  (CR-MET-001..012, all merged 2026-10-16) against six validation
  gates (schema, measurement conformance, MECE coverage, evidence
  anchors, threshold semantics, dual-anchor model).
- **Allocated**: all twelve are in the root model with
  `scope_layers` (CR-AR-FMWK-05, PR #18) and render 13/13 via the
  consumer generator.
- **Wired**: 24 intra-capability edges connect them
  (CR-AR-FMWK-09, PR #24); the integration surface reaches 9
  further entities (CR-AR-FMWK-10, PR #26).

`proposed` ("out of scope for catalogs; a candidate; nothing
committed") understates entities that are admitted, allocated, and
structurally wired. `planned` ("committed, content intended")
matches their actual state under the dimension convention in §1.

## 4. What does NOT change

- `MTR` (Performance Metric) — `status: existing`,
  `catalog_repo: dea-catalog-metrics`; it has real catalog content
  and is correct as-is. Not a dimension promotion candidate.
- `CON` (Concept) — a dimension entity whose named repo
  (`dea-catalog-concepts`) does not exist; stays `proposed` under
  create-on-content. Its status question is independent of this CR.
- All twelve entities' other fields, all 24 CR-AR-FMWK-09 edges,
  all CR-AR-FMWK-10 fields/edges, `scope_layers`, and every
  layer-allocated entity.
- Validator and schema: no change (rule 5 already enforces the
  convention; see §1).

## 5. Version impact

Forward transitions = **PR + patch bump**: v0.7.6 → v0.7.7. No ADR:
the lifecycle machinery, states, and bump rules are unchanged; this
CR records a convention within the existing `terminology.lifecycle`
framework. (If the convention is later found to need a validator
rule of its own or a terminology entry, that would be the
ADR-gated follow-up.)

## 6. Downstream effects

- **STRUCT-07c smoke test**: none. Dimension entities without
  `catalog_repo` are not in `KNOWN_ADOPTERS` scope; the status flip
  does not alter the status↔content checks, which key on
  `catalog_repo`.
- **Viewers/consumers**: lifecycle status is documentation, not
  allocation; the standard sync chain applies, no regeneration
  required.
- **`dea-metamodel`**: no counterpart change; the canonical
  statuses there are unchanged.

## 7. Definition of done

- [ ] Twelve dimension entities flipped to `status: planned`
- [ ] `VERSION` → `0.7.7`
- [ ] `model.version` → `0.7.7`
- [ ] `scripts/validate_model.py` PASS
- [ ] `scripts/check_authorship.py` PASS (AUT-001/002/003 = 0)
- [ ] `model-ci.yml` green
- [ ] This CR registered in `change-requests/README.md`

## 8. Out of scope

- CON's status (independent create-on-content question)
- Any chartering of per-entity catalogs for dimension entities
- The org-wide `supersedes` vocabulary question (still deferred
  from CR-AR-FMWK-09 §4)
- Any validator or schema change

## 9. Cross-references

- CR-AR-FMWK-05 (allocation, `catalog_repo: null` by design), §3
- CR-AR-FMWK-08 §8 (the deferral this CR closes)
- CR-AR-FMWK-09 (24 edges), CR-AR-FMWK-10 (integration surface)
- `dea-metamodel` CR-MET-001..012 (admission), docs/metric-capability-map.md §6 (six admission gates)
- Validator rule 5 (`scripts/validate_model.py`: hosted statuses require catalog_repo)
- `terminology.lifecycle` in `model/opendeam-model.yaml`
