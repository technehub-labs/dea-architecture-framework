# CR-CATALOG-STRUCT-07c: AF Smoke Test for Catalog/Model Drift

**Status**: Proposed
**Layer**: L0 (Architecture Framework; tooling)
**Owner**: TechNeHub Labs
**Depends on**: CR-CATALOG-STRUCT-07a (consumer module in `dea-metaframework`), CR-CATALOG-STRUCT-02..05 (four conformant adopters)
**Companion to**: CR-CATALOG-STRUCT-07 (the full STRUCT-07 slice); 07a (consumer module) and 07b (viewer integration) merged; this PR lands 07c (the architecture-framework smoke test).

## What this CR is

Third and final PR of the three-PR STRUCT-07 stack. Adds a smoke test to `dea-architecture-framework` that closes the consumer contract: walks the OpenDEAM root model, finds every entity whose `catalog_repo` matches a known conformant adopter, fetches each adopter's `CATALOG.yaml`, and verifies the catalog content is consistent with the model's status declaration.

The smoke test is the third leg of the consumer triangle:

1. **`validate_model.py`** (existing): validates the model itself (entity shapes, layer assignments, completeness).
2. **`validate_consumer.py`** (existing): validates each catalog's `metamodel-pointer.yaml` against the pinned model (allocation drift).
3. **`check_catalog_index_matches_model.py`** (NEW, this PR): validates that each catalog's actual content matches the model's `status` declaration.

Where (2) checks "the catalog claims the right allocation" and (1) checks "the model is internally consistent", (3) checks "the catalog has content where the model says it should".

## Decisions locked during planning

- **Q1 (severity)**: `existing + 0 canonical` is a **fail** (catastrophic drift; the model says the entity exists and the catalog says it's empty). `scaffold + >0 canonical` is a **warning** (model status is stale; promotion is a model-update concern, not a contract violation). `planned + 0 canonical` is a **warning** (same as scaffold+0). `proposed` and `retired` skip the content check (no backing expected).
- **Q2 (scope)**: only known conformant adopters are smoke-tested. The other 45 model entries that reference not-yet-adopters (`dea-catalog-ecosystem-platforms`, etc.) are ignored: they would always fail under the existing regime (catalog doesn't exist yet), and we don't want to litter CI with phantom failures.
- **Q3 (CI)**: the smoke test does NOT block CI on warnings. Hard failures (model missing, fetch failed, schema broken) exit non-zero. Soft warnings (status drift) print to stderr; the consumer operator triages them.

## What changes

### Files added

- `scripts/cross_repo_consumer/__init__.py` (vendored)
- `scripts/cross_repo_consumer/fetch.py` (vendored)
- `scripts/cross_repo_consumer/cli.py` (vendored)
- `scripts/check_catalog_index_matches_model.py` (~280 lines)
- `tests/__init__.py` (test package marker)
- `tests/test_check_catalog_index_matches_model.py` (~290 lines; 17 tests)
- `change-requests/CR-CATALOG-STRUCT-07c.md` (this file)

### Files changed

None. The smoke test is a new script + tests; it does not modify the existing `validate_model.py` or `validate_consumer.py`. A follow-up PR can wire the smoke test into `model-ci.yml` if desired.

## Smoke test output (live run against HEAD model + cached adopters)

```
INFO: 54 model entities; 4 reference known adopters (['dea-catalog-business-capabilities', 'dea-catalog-digital-business-service-factory', 'dea-catalog-processes', 'dea-catalog-stakeholders'])
  dea:entity-business-process (dea-catalog-processes): WARN: status=scaffold but catalog has 2 canonical entities (model status is stale; promote to 'existing' or 'planned')

result: 0 failure(s), 1 warning(s)
```

The warning is **real drift**: the model has `dea:entity-business-process` with `status: scaffold`, yet the process catalog actually has 2 canonical `Process` entries (`dea:process-manage-customer-relationship`, `dea:process-onboard-supplier`). The smoke test surfaces this as a warning; promotion to `status: existing` is the model's job, not the smoke test's.

## Severity matrix

| Model status | Catalog canonical count | Severity |
|---|---|---|
| existing | 0 | **FAIL** |
| existing | >=1 | pass |
| planned | 0 | WARN (model content lagging catalog) |
| planned | >=1 | pass |
| scaffold | 0 | pass (expected scaffold state) |
| scaffold | >=1 | WARN (model status is stale) |
| proposed / retired | any | skip (no catalog expected) |

## Verification

- `PYTHONPATH=scripts python -m pytest tests/test_check_catalog_index_matches_model.py` returns `17 passed`.
- Live smoke against the real model + cached adopters returns `0 failures, 1 warning` (the documented `dea:entity-business-process` status-drift case).
- All 30 metaframework consumer tests still pass (no regression in the upstream module).
- Dash sweep on new prose: clean.
- Secret scan: 0.
- `git diff --check`: clean.

## Sequencing

| Slice | Status |
|---|---|
| STRUCT-01 | Merged |
| STRUCT-06a + 06b | Merged |
| STRUCT-02..05 (four adopters) | Merged |
| STRUCT-07a (consumer module, `dea-metaframework`) | Merged (PR #19) |
| STRUCT-07b (viewer integration) | Merged (PR #164 + #22) |
| STRUCT-07c (AF smoke test) | **This PR** |

After this merges, **STRUCT-07 is complete** and the cross-repo consumer pattern is fully wired: catalog repos produce `CATALOG.yaml`; the consumer reads them; the viewer surfaces them; the architecture framework validates them.