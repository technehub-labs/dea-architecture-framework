# CR-AR-FMWK-14: Concept (CON) Status Promotion + CR-AR-FMWK-08 Record Correction

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-14 |
| **Title** | Concept (CON) Status Promotion (proposed → planned) and CR-AR-FMWK-08 §4 record correction |
| **Status** | Proposed (this PR) |
| **Type** | Lifecycle status transition (forward) + factual record correction |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Entity** | `dea:entity-concept` (class_alias `CON`, semantic-dimension; no layer) |
| **Governing rule** | `terminology.lifecycle.forward_transition` (PR + patch bump); the dimension-lifecycle convention (CR-AR-FMWK-11 §1) applies — but CON's promotion does not need it, because CON has a named `catalog_repo`, so the ordinary STRUCT-07c evidence class governs |
| **Predecessor** | CR-AR-FMWK-08 (whose §4 table this CR corrects); CR-AR-FMWK-06/07 (the promotion precedent) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. The factual correction

CR-AR-FMWK-08 §4 recorded CON as a non-promotion on the claim "repo
`dea-catalog-concepts` does not exist." **That claim was wrong** — the
product of a transient GitHub API failure during the audit's batched
repo checks (the same loop verified 13 other repos correctly, so the
error escaped notice).

Re-verified live on 2026-10-27 (post-#31 merge):

- `dea-catalog-concepts` **exists** — created 2026-07-21, public,
  not archived. The documented rename from `dea-catalog-glossary`
  redirects to it (GitHub rename, history preserved; it also absorbed
  `dea-catalog-taxonomy`), exactly as ADR-0004 D2 and the roadmap's
  v0.4.0 rollout record state.
- Commit history is continuous across the org's governance arc:
  v0.2.1 pointer era (Aug 13), v0.4.0 ADR-0004 adoption + rename
  (Aug 14), README foundation (Aug 16), CR-CON-01 authorship gate
  (Oct 14), CR-CON-02 entity-system slice (Oct 16).
- Foundation is **fuller than the CR-06/07 promotion precedent**: not
  just README/LICENSE/NOTICE/pointer, but also `change-requests/`,
  `reconciliation/`, `scripts/`, `tests/` — a governed catalog repo.
- `metamodel-pointer.yaml` declares `catalog.status: proposed` and
  pins v0.4.0 (stale pin, auto-generated; regenerates via fan-out).
- **No `CATALOG.yaml`; zero canonical entries.**

This CR corrects the record rather than leaving the audit's error
standing: the CR-08 §4 row for CON is superseded by this CR's §1.

## 2. Why `planned` is the correct state

This is the ordinary STRUCT-07c evidence class (CR-AR-FMWK-06/07), not
the dimension-lifecycle convention: CON has a named, existing
`catalog_repo` (`dea-catalog-concepts`), so the status↔content
contract applies directly.

- **`proposed`** says "no catalog expected" — false; the repo exists
  and is committed.
- **`planned`** says "catalog expected, content intended but not yet
  canonical" — exactly the verified state (no `CATALOG.yaml`, zero
  canonical Concept entries).
- Promoting past `planned` would be wrong: the smoke test would warn,
  correctly, that the model claims content the catalog lacks.

The roadmap's CON disposition also updates: the legacy-catalog table
listed `dea-catalog-glossary` as "candidate (a): map to a model
entity" — that mapping has in fact been complete since v0.4.0 (the
repo was renamed and now carries the CON pointer). The disposition is
resolved, not pending.

## 3. Change Request

Two parts:

1. **Model**: one line in `model/opendeam-model.yaml`
   `allocation.entities` — `dea:entity-concept`:
   `status: proposed` → `status: planned`. No other field changes
   (entity_id, class_alias, display_name, catalog_repo, scope_layers
   all unchanged).
2. **Docs**: a correction note in `docs/roadmap.md` marking the CON
   disposition resolved (the glossary→concepts rename completed the
   mapping in v0.4.0), and this CR registered in
   `change-requests/README.md`.

## 4. What does NOT change

- Any other entity (FR, PHR, INR, IA, KA remain `proposed` — their
  repos are genuinely absent, re-verified in the same check that
  caught the CON error).
- CON's dimension semantics (semantic-dimension allocator,
  `scope_layers`, `defined_by` machinery — all unchanged).
- No relationships, no schema, no validator rules (rule 10's
  supersedes check and rule 3's dimension checks are untouched).
- CR-AR-FMWK-08's promotions themselves (the nine remain correct;
  only the CON non-promotion row was wrong).

## 5. Version impact

Forward transition = **PR + patch bump**: v0.8.1 → v0.8.2. No ADR.

## 6. Definition of done

- [ ] `dea:entity-concept` `status: planned` (one line)
- [ ] `VERSION` and `model.version` → `0.8.2`
- [ ] Roadmap CON-disposition correction note
- [ ] This CR registered in `change-requests/README.md`
- [ ] `validate_model.py` PASS; `check_authorship.py` PASS;
      `model-ci.yml` green

## 7. Out of scope

- FR/PHR/INR/IA/KA (repos genuinely absent; create-on-content)
- Any content contribution to `dea-catalog-concepts` (first
  canonical Concept entries trigger planned → scaffold)
- The dimension-lifecycle convention's application to other dimension
  entities (governed by CR-AR-FMWK-11)
- Amending CR-AR-FMWK-08's document text itself (historical CRs are
  immutable; this CR carries the correction forward)

## 8. Cross-references

- CR-AR-FMWK-08 §4 (the corrected record)
- CR-AR-FMWK-06 / CR-AR-FMWK-07 (the promotion precedent and evidence
  class)
- ADR-0004 D2 (the glossary+taxonomy → Concept merge and rename)
- `scripts/check_catalog_index_matches_model.py` (status↔content
  contract)
- `dea-catalog-concepts` commit history (v0.2.1 → v0.4.0 →
  CR-CON-01/02; the live evidence)
