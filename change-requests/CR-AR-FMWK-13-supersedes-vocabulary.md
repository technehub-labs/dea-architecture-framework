# CR-AR-FMWK-13: Supersedes/Replaces Vocabulary Resolution + Schema Hygiene

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-13 |
| **Title** | Supersedes/Replaces vocabulary resolution: a `supersedes` terminology entry, entity-field declarations, and one validator rule |
| **Status** | Proposed (this PR) |
| **Type** | Terminology convention + schema declaration + validator rule (no entity or relationship content changes) |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model, schema, validator) |
| **Predecessor** | CR-AR-FMWK-09 §4 (deferred the org-wide `supersedes` question); CR-AR-FMWK-04 (introduced the entity-level `supersedes` field on ISF) |
| **Authority** | `dea-metamodel` CR-004 §19 (Core grammar: `dea:replaces`, `dea:transitions-to`) + the metric programme's `dea:supersedes` (docs/metric-capability-map.md §4) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. The deferred question

CR-AR-FMWK-09 §4 left `supersedes` out of the metric edges because "an
OpenDEAM-wide `supersedes` vocabulary question" deserved its own CR.
The question: does OpenDEAM need a lifecycle supersession relation,
and how does it relate to the Core grammar's `dea:replaces`?

## 2. Resolution (the convention this CR records)

OpenDEAM distinguishes **three** temporal relations, matching the
metamodel's separation:

| Relation | Where it lives | Meaning | Authority |
|---|---|---|---|
| **Entity identity supersession** — `supersedes` entity field | `allocation.entities[].supersedes` (entity entry) | A root-model entity has taken over the architectural role of a predecessor entity **at the model level** (ISF supersedes SF's role). One-directional; the predecessor keeps its identity for continuity (EGV-004). | OpenDEAM `terminology` (this CR) |
| **Instance supersession** — `supersedes` relationship edge | `relationships[]` (deferred to the metric follow-on) | A newer authoritative **instance/value** exists for the same period (metric programme: 10-type, both endpoints). Distinct from `corrects` (asserts the original was wrong). | `dea-metamodel` metric capability; not yet in OpenDEAM — see §6 |
| **Replacement/retirement** — Core `dea:replaces` | Core grammar (metamodel) | The source takes over the function of the target, **which is retired**. | Core relationship grammar; OpenDEAM's `lifecycle.states_ordered` already covers retirement via `deprecated`/`retired` statuses |

**Ruling:** OpenDEAM does **not** add a `supersedes` rel_type value in
this CR. The three concerns above are already separately represented;
collapsing them into one rel_type would recreate the conflation the
metamodel explicitly warns against ("corrects and supersedes are not
interchangeable"). The entity-level `supersedes` field remains the
OpenDEAM-side mechanism for identity supersession (the ISF precedent),
and instance-level supersession belongs to the metric programme's
follow-on if/when metric instances need OpenDEAM-side edges.

## 3. The hygiene gap this CR closes

Two fields are **used in the model but undeclared in the schema**
(discovered during this CR's analysis):

- `supersedes` — used by ISF (`dea:entity-information-system-function`,
  value `dea:entity-system-function`), introduced by CR-AR-FMWK-04
  without a schema declaration.
- `legacy_ids` — used by PRC (`dea:entity-process`, value
  `[dea:entity-process]`), introduced by ADR-0006/CR-AR-FMWK-01
  without a schema declaration.

The schema does not set `additionalProperties: false`, so validation
passes today — the fields are silently tolerated. That is drift
between the schema and the model's actual vocabulary: a future
schema tightening would break the model, and a consumer reading the
schema alone would not know these fields exist.

**Fix:** declare both fields in
`schemas/opendeam-model.schema.json`:

```json
"supersedes": {
  "type": "string",
  "description": "Entity identity supersession: this entity has taken over the architectural role of the named predecessor entity (by entity_id). The predecessor keeps its identity for continuity (EGV-004). See terminology.supersedes (CR-AR-FMWK-13)."
},
"legacy_ids": {
  "type": "array",
  "items": {"type": "string"},
  "description": "Historical identifiers this entity was previously known by (ADR-0006 kernel discipline)."
}
```

## 4. Terminology entry

Add to `terminology:` in `model/opendeam-model.yaml`:

```yaml
  supersedes: 'Entity identity supersession (CR-AR-FMWK-13). An entity MAY declare supersedes:
    <predecessor entity_id> when it has taken over the predecessor''s architectural role at
    the model level; the predecessor retains its identity for consumer continuity (EGV-004).
    Distinct from the metric programme''s instance-level supersedes relation (a newer authoritative
    value for the same period) and from the Core dea:replaces (the target is retired). The
    retirement path for entities remains the lifecycle states deprecated/retired (which require
    an ADR + minor bump).'
```

## 5. Validator rule 10: supersedes target must exist

Add to `scripts/validate_model.py` (rule 10, after rule 9):

```
10. supersedes targets must exist as entity_ids (not aliases — the
    field carries entity_ids, per the ISF precedent); a supersedes
    target must not itself declare supersedes (no chains).
```

Three negative controls verified locally (unknown target; chain;
alias-instead-of-id).

## 6. What this CR deliberately does NOT do

- No `supersedes` rel_type vocabulary value (per §2's ruling).
- No metric instance-level supersession edges (metric follow-on).
- No changes to ISF, PRC, or any entity entry — the fields they
  already carry become *declared*, not modified.
- No `additionalProperties: false` on the entity schema (a broader
  tightening is its own CR; this one only closes the known gap).

## 7. Version impact

Schema declaration + terminology entry + validator rule — no entity
or relationship content change. **PR + patch bump**: v0.8.0 →
v0.8.1. (The terminology entry is additive documentation of an
existing mechanism, not a structural change; no ADR needed.)

## 8. Definition of done

- [ ] `supersedes` + `legacy_ids` declared in the entity schema
- [ ] `terminology.supersedes` entry added to the model
- [ ] Validator rule 10 added (+3 negative controls verified)
- [ ] `VERSION` and `model.version` → `0.8.1`
- [ ] `validate_model.py` PASS; `check_authorship.py` PASS;
      `model-ci.yml` green
- [ ] This CR registered in `change-requests/README.md`

## 9. Cross-references

- CR-AR-FMWK-09 §4 (the deferral); CR-AR-FMWK-04 (the ISF field)
- `dea-metamodel` CR-004 §19 (`dea:replaces`, `dea:transitions-to`)
- `dea-metamodel` docs/metric-capability-map.md §4 (instance-level `dea:supersedes`, 10-type)
- ADR-0006 (`legacy_ids` on the Process kernel)
- `terminology.lifecycle` (deprecated/retired remain the retirement path)
