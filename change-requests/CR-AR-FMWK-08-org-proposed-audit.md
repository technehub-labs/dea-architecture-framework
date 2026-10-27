# CR-AR-FMWK-08: Org-Wide `proposed`-Status Audit — 9 Promotions

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-08 |
| **Title** | Org-Wide `proposed`-Status Audit: 9 promotions proposed → planned |
| **Status** | Proposed (this PR) |
| **Type** | Lifecycle status transitions (forward); additive metadata change |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Entities** | 9 entities across L1, L2, L3, L4 (see §3 table) |
| **Governing rule** | `terminology.lifecycle.states_ordered` + `forward_transition` (model/opendeam-model.yaml): a forward transition requires a PR and a patch version bump; no ADR is required |
| **Predecessor** | CR-AR-FMWK-06 (ROL, PR #19) and CR-AR-FMWK-07 (SKL+CHI, PR #20) — same evidence class, same one-line-per-entity shape; STRUCT-07c status↔content contract |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. Purpose

This is the org-wide audit deferred by CR-AR-FMWK-06 §7 and scoped by
CR-AR-FMWK-07 §8. Every entity currently at `status: proposed` was
enumerated from the model and each one's `catalog_repo` was checked
live against GitHub (2026-10-27). The outcome:

- **9 promotions** — catalog repo exists with the foundation-first
  scaffold but no `CATALOG.yaml`; `proposed` understates the committed
  state. Promoted to `planned`.
- **19 remain `proposed`** — either the named catalog repo does not
  exist yet, or the entity is an abstract kernel / dimension entity
  with no catalog expectation. `proposed` is honest for these.

## 2. Method

Per-entity `catalog_repo` resolved via the GitHub API. A repo counts
as foundation-first scaffold when it carries README, LICENSE, NOTICE,
`metamodel-pointer.yaml`, `.github`, `.gitignore` and **no**
`CATALOG.yaml` and no canonical entries — identical to the evidence
class accepted in CR-AR-FMWK-06 and CR-AR-FMWK-07.

Entities with no `catalog_repo` expectation are excluded from the
audit by design:

- Abstract kernels (`PRC`, `RES`) — structural anchors, no catalog.
- Dimension entities (`MMT`, `MOBS`, `IDS`, `BSL`, `PTG`, `THR`,
  `PIT`, `RPT`, `PRV`, `ANR`, `COR`, `CSH`) — the STRUCT-07c contract
  treats dimension entities as out of catalog-content scope; lifecycle
  promotion for these is a governance-semantics question deferred to
  the metric-programme follow-on.

## 3. Promotions

All nine have existing foundation-first catalog repos, verified live:

| Entity | Alias | Building block | Catalog repo (exists, no `CATALOG.yaml`) |
|---|---|---|---|
| `dea:entity-ecosystem-platform` | EP | L1-ecosystem-platforms | `dea-catalog-ecosystem-platforms` |
| `dea:entity-risk` | RSK | L2-risk-compliance | `dea-catalog-risk-register` |
| `dea:entity-control` | CTL | L2-risk-compliance | `dea-catalog-controls` |
| `dea:entity-regulation` | REG | L2-risk-compliance | `dea-catalog-regulations` |
| `dea:entity-signal` | SIG | L2-innovation-foresight | `dea-catalog-signals` |
| `dea:entity-experiment` | EXP | L2-innovation-foresight | `dea-catalog-experiments` |
| `dea:entity-technology-radar-entry` | TRE | L2-innovation-foresight | `dea-catalog-technology-radar` |
| `dea:entity-model-deployment` | MDP | L4-model-operations | `dea-catalog-model-deployments` |
| `dea:entity-model-feedback-signal` | MFS | L4-model-operations | `dea-catalog-model-deployments` |

Change exactly one field on each: `status: proposed` → `status: planned`.

## 4. Non-promotions (documented for the record)

| Entity | Alias | State | Why it stays `proposed` |
|---|---|---|---|
| `dea:entity-concept` | CON | repo `dea-catalog-concepts` does not exist | No committed owner yet; create-on-content applies |
| `dea:entity-financial-resource` | FR | repo `dea-catalog-financial-resources` does not exist | Named by v0.5.0 earmark; create-on-content applies |
| `dea:entity-physical-resource` | PHR | repo `dea-catalog-physical-resources` does not exist | Same |
| `dea:entity-intangible-resource` | INR | repo `dea-catalog-intangible-resources` does not exist | Same |
| `dea:entity-information-asset` | IA | repo `dea-catalog-information-assets` does not exist | Same |
| `dea:entity-knowledge-asset` | KA | repo `dea-catalog-knowledge-assets` does not exist | Same |
| `dea:entity-process`, `dea:entity-resource` | PRC, RES | abstract kernels, `catalog_repo: null` | No catalog expectation |
| 12 metric-programme dimension entities | MMT..CSH | no layer, no catalog_repo | Dimension scope; deferred to the metric follow-on CR |

## 5. Version impact

Forward transitions = **PR + patch bump**: v0.7.3 → v0.7.4. No ADR, no
minor bump. The version chain stays linear: v0.7.1 → v0.7.2 (#19) →
v0.7.3 (#20) → v0.7.4 (this CR).

This CR is based on the CR-AR-FMWK-07 branch (PR #20) and must merge
after it.

## 6. Downstream effects

- **`metamodel-pointer.yaml` in the 9 catalog repos** — all
  auto-generated, regenerating from this repo's fan-out at the next
  root-model release; no hand edits.
- **STRUCT-07c smoke test** — none of the 9 repos are in
  `KNOWN_ADOPTERS`, so no immediate CI effect. On adoption, `planned`
  produces the expected advisory zero-content warning until first
  canonical entries land. Intended signal.
- **MDP + MFS share `dea-catalog-model-deployments`** — the repo
  already exists foundation-first; this CR promotes both entities.
  The pre-existing non-blocking "shares catalog_repo without
  discriminator" convention warning is unchanged by a status flip.

## 7. Definition of done

- [ ] 9 entities flipped to `status: planned` in
      `model/opendeam-model.yaml`
- [ ] `VERSION` → `0.7.4`
- [ ] `model.version` → `0.7.4`
- [ ] `scripts/validate_model.py` PASS
- [ ] `scripts/check_authorship.py` PASS (AUT-001/002/003 = 0)
- [ ] `model-ci.yml` green (includes STRUCT-07c smoke test)
- [ ] This CR registered in `change-requests/README.md`
- [ ] PR #19 and PR #20 merged first

## 8. Out of scope

- Creating any of the 6 named-but-nonexistent catalog repos
  (create-on-content per the roadmap earmark).
- Any content contribution to the 9 catalog repos (first canonical
  entries trigger planned → scaffold).
- Metric-programme dimension-entity lifecycle semantics (follow-on CR).
- Regenerating consumer pointers by hand (fan-out handles it).

## 9. Cross-references

- `terminology.lifecycle` in `model/opendeam-model.yaml` (states + bump rules)
- `scripts/check_catalog_index_matches_model.py` (status↔content contract)
- CR-AR-FMWK-06 (`change-requests/CR-AR-FMWK-06-role-status-promotion.md`, PR #19)
- CR-AR-FMWK-07 (`change-requests/CR-AR-FMWK-07-skl-chi-status-promotion.md`, PR #20)
- Commit 2e43369 — precedent status flip (scaffold → existing)
- `change-requests/CR-CATALOG-STRUCT-07c.md` (smoke-test CR)
- `docs/roadmap.md` — "New catalog repos named by v0.5.0" earmark (create-on-content)
