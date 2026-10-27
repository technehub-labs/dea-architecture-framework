# CR-AR-FMWK-07: Skill (SKL) & Change Initiative (CHI) Status Promotion — proposed → planned

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-07 |
| **Title** | Skill (SKL) & Change Initiative (CHI) Status Promotion: proposed → planned |
| **Status** | Proposed (this PR) |
| **Type** | Lifecycle status transition (forward); additive metadata change |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Entities** | `dea:entity-skill` (class_alias `SKL`) and `dea:entity-change-initiative` (class_alias `CHI`), both L3, `L3-people-skills-culture` |
| **Governing rule** | `terminology.lifecycle.states_ordered` + `forward_transition` (model/opendeam-model.yaml): a forward transition requires a PR and a patch version bump; no ADR is required |
| **Predecessor** | CR-AR-FMWK-06 (ROL promotion, PR #19) — same evidence class, same one-line-per-entity shape; ADR-0003 Phase 3 (foundation-first scaffold of both catalogs); STRUCT-07c status↔content contract |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. Change Request

Update `model/opendeam-model.yaml` `allocation.entities`:

```yaml
- entity_id: dea:entity-skill            # status: proposed → planned
- entity_id: dea:entity-change-initiative # status: proposed → planned
```

Change exactly one field on each of the two entries:
`status: proposed` → `status: planned`.

Bump the version from v0.7.2 to v0.7.3 in **both** `VERSION` and
`model.version`.

## 2. Why `planned` is the correct state

The evidence class is identical to CR-AR-FMWK-06 (ROL), verified
live against GitHub on 2026-10-27:

| Entity | Catalog repo | Foundation scaffold | `CATALOG.yaml` | Canonical entries |
|---|---|---|---|---|
| SKL | `dea-catalog-skills` | README, LICENSE, NOTICE, `metamodel-pointer.yaml`, `.github`, `.gitignore` | absent | 0 |
| CHI | `dea-catalog-change-initiatives` | README, LICENSE, NOTICE, `metamodel-pointer.yaml`, `.github`, `.gitignore` | absent | 0 |

Per the STRUCT-07c status↔content contract
(`scripts/check_catalog_index_matches_model.py`):

- **`proposed`** — out of scope for catalogs; no catalog content is
  expected. Neither entity is a mere candidate anymore: both have a
  committed owning repo.
- **`planned`** — a catalog is expected; `counts.canonical >= 1` is
  the target (0 is a warning, not a failure). Both repos are real and
  committed; content is intended but not yet canonical.

That is exactly `planned`. Promoting further (scaffold/existing) would
be wrong and would generate the smoke test's stale-status warning.

## 3. What does NOT change

- `entity_id`, `class_alias`, `display_name`, `layer`,
  `building_block`, `catalog_repo`, `description` — all unchanged on
  both entries.
- All three relationships touching these entities:
  `SKL → ROL` (required by, dependency, 0..N:0..N),
  `ROL → AC` (untouched by this CR), and
  `CHI → OU` (targets, dependency, 0..N:0..N).
- No other entity entry, no layer or building_block reorganisation, no
  schema change, no controlled-vocabulary change, no consumer contract
  change.

## 4. Version impact

Forward transition = **PR + patch bump**: v0.7.2 → v0.7.3. No ADR, no
minor bump. Follows CR-AR-FMWK-06 and the 2e43369 precedent
(single-line status flips, patch-bump delivery).

This CR is based on the CR-AR-FMWK-06 branch (PR #19) and must merge
after it; the version chain v0.7.1 → v0.7.2 (ROL) → v0.7.3 (SKL+CHI)
is linear.

## 5. Downstream effects

- **`dea-catalog-skills` / `dea-catalog-change-initiatives`
  `metamodel-pointer.yaml`** — both auto-generated, currently pinning
  v0.3.0 and recording `catalog.status: proposed`; both regenerate
  from this repo's fan-out at the next root-model release.
- **STRUCT-07c smoke test** — neither repo is in `KNOWN_ADOPTERS`,
  so no immediate CI effect. On adoption, `planned` will produce the
  expected advisory zero-content warning until first canonical entries
  land. Intended signal, not a regression.
- **Viewer/metamodel consumers** key on identity and allocation;
  lifecycle status is documentation — no regeneration strictly
  required; standard post-release fan-out applies.

## 6. Definition of done

- [ ] `dea:entity-skill` `status: planned` in
      `model/opendeam-model.yaml` (one line)
- [ ] `dea:entity-change-initiative` `status: planned` in
      `model/opendeam-model.yaml` (one line)
- [ ] `VERSION` → `0.7.3`
- [ ] `model.version` → `0.7.3`
- [ ] `scripts/validate_model.py` PASS
- [ ] `scripts/check_authorship.py` PASS (AUT-001/002/003 = 0)
- [ ] `model-ci.yml` green (includes STRUCT-07c smoke test)
- [ ] This CR registered in `change-requests/README.md`
- [ ] PR #19 (CR-AR-FMWK-06) merged first

## 7. Out of scope

- Any other `proposed` entity (remaining candidates: see the audit
  note in §8) — each needs its own evidence check.
- Any content contribution to either catalog repo (first canonical
  entries trigger planned → scaffold).
- Regenerating consumer pointers by hand (fan-out handles it).
- ROL (delivered by CR-AR-FMWK-06).

## 8. Audit note (completes the L3-people-skills-culture block)

With this CR the entire `L3-people-skills-culture` building block is
promoted out of `proposed`: ROL (CR-AR-FMWK-06), SKL and CHI (this
CR). This closes the sibling audit identified in CR-AR-FMWK-06 §7.
Remaining `proposed` entities elsewhere in the model remain candidates
for a future org-wide audit CR; the same evidence rule applies — check
the catalog repo's actual state before flipping.

## 9. Cross-references

- `terminology.lifecycle` in `model/opendeam-model.yaml` (states + bump rules)
- `scripts/check_catalog_index_matches_model.py` (status↔content contract)
- CR-AR-FMWK-06 (`change-requests/CR-AR-FMWK-06-role-status-promotion.md`, PR #19)
- Commit 2e43369 — precedent status flip (scaffold → existing)
- ADR-0003 Phase 3 (foundation-first scaffold of both catalog repos)
- `change-requests/CR-CATALOG-STRUCT-07c.md` (smoke-test CR)
