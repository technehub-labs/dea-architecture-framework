# CR-AR-FMWK-06: Role (ROL) Status Promotion — proposed → planned

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-06 |
| **Title** | Role (ROL) Status Promotion: proposed → planned |
| **Status** | Proposed (this PR) |
| **Type** | Lifecycle status transition (forward); additive metadata change |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Entity** | `dea:entity-role` (class_alias `ROL`, L3, `L3-people-skills-culture`) |
| **Governing rule** | `terminology.lifecycle.states_ordered` + `forward_transition` (model/opendeam-model.yaml): a forward transition requires a PR and a patch version bump; no ADR is required |
| **Predecessor** | ADR-0003 (v0.3.0 rollout that scaffolded `dea-catalog-roles`); STRUCT-07c smoke test (CR-CATALOG-STRUCT-07c) that defined the status↔catalog-content contract |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. Change Request

Update `model/opendeam-model.yaml` `allocation.entities`, entry
`dea:entity-role`:

```yaml
- entity_id: dea:entity-role
  class_alias: ROL
  display_name: Role
  layer: L3
  building_block: L3-people-skills-culture
  status: proposed      # → planned
  catalog_repo: dea-catalog-roles
```

Change exactly one field: `status: proposed` → `status: planned`.

Bump the version from v0.7.1 to v0.7.2 in **both** `VERSION` and
`model.version` (the integrity gate in `validate_model.py` fails on a
mismatch — the CR-AR-FMWK-05 rollout hit exactly this and the gate caught
it).

## 2. Why `planned` is the correct state

The lifecycle meaning of the two states, per the status↔catalog-content
contract that `scripts/check_catalog_index_matches_model.py`
(STRUCT-07c) encodes:

- **`proposed`** — out of scope for catalogs; no catalog content is
  expected. The entity is a candidate; nothing is committed.
- **`planned`** — a catalog is expected; `counts.canonical >= 1` is the
  target (0 is a warning, not a failure). The entity is committed, its
  owning repo is named, content is intended but not yet canonical.

`dea-catalog-roles` exists and carries the foundation-first pattern
(README entity detail, LICENSE, NOTICE, `metamodel-pointer.yaml`), but
has no `CATALOG.yaml` and no canonical Role entries. That is precisely
`planned`: the repo is real and committed, the content is not.

Promoting past `planned` (to `scaffold` or `existing`) would be wrong:
the smoke test would warn — correctly — that the model claims content
the catalog does not have.

## 3. What does NOT change

- `entity_id`, `class_alias`, `display_name`, `layer`,
  `building_block`, `catalog_repo`, `description` — all unchanged.
- Both ROL relationships: `SKL → ROL` (required by, dependency,
  0..N:0..N) and `ROL → AC` (fulfilled by, realization, 1:0..N).
- No other entity entry, no layer or building_block reorganisation, no
  schema change, no controlled-vocabulary change, no consumer
  contract change (`validate-against-model.yml` keys on identity and
  allocation, not lifecycle status).

## 4. Version impact

Per `terminology.lifecycle.forward_transition` this is a forward
transition within the ordered states — a **PR + patch bump**:
v0.7.1 → v0.7.2. No ADR, no minor bump. This follows the established
precedent of the `dea:entity-business-process` scaffold→existing
upgrade (commit 2e43369), which was also a single-line status flip
with a patch-bump delivery.

## 5. Downstream effects

- **`dea-catalog-roles/metamodel-pointer.yaml`** currently records
  `catalog.status: proposed` and pins `v0.3.0`. It is auto-generated
  ("do not edit manually") and regenerates from this repo's fan-out at
  the next root-model release — this CR is that release for ROL.
- **STRUCT-07c smoke test** — `dea-catalog-roles` is not yet in
  `KNOWN_ADOPTERS`, so the status flip has no immediate CI effect. When
  the repo adopts the catalog-repository pattern and joins the known
  adopters, the `planned` status will generate the expected (advisory)
  zero-content warning until the first canonical Role entries land.
  That is the intended signal, not a regression.
- **Viewer/metamodel consumers** key on `class_alias` and identity;
  lifecycle status is documentation, not allocation — no consumer
  regeneration is strictly required, but the standard post-release
  fan-out (`fan-out.yml` → `opendeam-sync` → viewers) applies.

## 6. Definition of done

- [ ] `dea:entity-role` `status: planned` in
      `model/opendeam-model.yaml` (one line)
- [ ] `VERSION` → `0.7.2`
- [ ] `model.version` → `0.7.2`
- [ ] `scripts/validate_model.py` PASS
- [ ] `scripts/check_authorship.py` PASS (AUT-001/002/003 = 0)
- [ ] `model-ci.yml` green (includes STRUCT-07c smoke test,
      `--skip-unreachable`)
- [ ] This CR registered in `change-requests/README.md`

## 7. Out of scope

- Any promotion of sibling L3-people-skills-culture entities (SKL,
  CHI) — each needs its own evidence check and should be batched in a
  follow-on audit CR, not smuggled into this one.
- Any content contribution to `dea-catalog-roles` (first canonical Role
  entries are the trigger for the next promotion, planned → scaffold).
- Regenerating consumer pointers by hand (fan-out handles it).

## 8. Cross-references

- `terminology.lifecycle` in `model/opendeam-model.yaml` (states + bump rules)
- `scripts/check_catalog_index_matches_model.py` (status↔content contract)
- Commit 2e43369 — precedent status flip (scaffold → existing)
- ADR-0003 Phase 3 (foundation-first scaffold of `dea-catalog-roles`)
- `change-requests/CR-CATALOG-STRUCT-07c.md` (smoke-test CR)
- Roadmap: T2 pin-drift note (pointers regenerate at the next root-model release)
