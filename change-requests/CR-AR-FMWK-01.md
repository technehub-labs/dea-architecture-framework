# CR-AR-FMWK-01: Process Kernel + Business Process Specialization (root model)

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-01 |
| **Title** | Process Kernel + Business Process Specialization (root model) |
| **Status** | Proposed (working-folder draft; awaiting sign-off) |
| **Type** | Structural root-model update + validator extension |
| **Scope** | `technehub-labs/dea-architecture-framework` |
| **Predecessor** | CR-MM-PROC-01 (`dea-metamodel`, merged 2026-09-03; PR #163); WSF Foundational Semantic Synthesis §6 |
| **Authority** | WSF (`wsf:Process`); `dea-metamodel` (canonical Core authority; declares `dea:Process` kernel + `dea:BusinessProcess` specialization); this root model ( lags downstream and must sync) |
| **Author** | Coder (for eaojnr) |
| **Date** | 2026-09-03 |

## 1. Change Request

Update `dea-architecture-framework/model/opendeam-model.yaml` to declare
**both** `dea:entity-process` (abstract root-model kernel entry; new)
**and** `dea:entity-business-process` (Core specialization; new), with
a discriminator that tracks the legacy id (`dea:entity-process`).

This mirrors the `dea:entity-resource` → `dea:entity-financial-resource` /
`dea:entity-physical-resource` / `dea:entity-intangible-resource`
template (ADR-0005) and is the root-model sync that unblocks
`CR-BP-SPEC-BP-01` (catalog-side) and the
`validate-allocation` workflow on `dea-catalog-processes`.

Also extend `scripts/validate_consumer.py` with a third branch for
abstract kernel entities (no `layer`, no `dimension`): the validator
must accept these as structural anchors without forcing a dimension
allocation.

## 2. Why This CR Exists

`dea-metamodel` has merged CR-MM-PROC-01 (kernel + specialization)
at PR #163. The catalog `dea-catalog-processes` declares both ids
in its metamodel pointer (per CR-BP-SPEC-BP-01, in progress). The
consumer validator (`validate_consumer.py`) on
`dea-architecture-framework` is the CI contract — it reads the
root model and validates that every `entity_id` in any consumer
pointer is declared here.

Today the root model declares `dea:entity-process` only (line 500).
The catalog's CR-BP-SPEC-BP-01 pointer will declare `dea:BusinessProcess`
(the new specialization id), which the validator cannot resolve
against the root model → `validate-allocation` fails on
`dea-catalog-processes`.

The clean fix: declare both `dea:entity-process` (abstract, no
layer) and `dea:entity-business-process` (L3, specialization) in
the root model. The legacy `dea:entity-process` id remains
semantically (a pre-WSF root-model alias) but the canonical
specialization id becomes `dea:entity-business-process`.

## 3. Architectural Decision

**Decision AR-FMWK-01-D01** — Add `dea:entity-process` to the root
model as an **abstract kernel entry**, allocated to **L3**
(`layer: L3`; `building_block: L3-value-delivery`) with
`discriminator: process-kernel`. The kernel declares
`completeness_contract` for any T2 catalog specializing it: the T2
catalog must declare its specialization context (e.g. Business,
Operational, Engineering) via `specializes:` in its pointer.

**Note**: an earlier draft of this CR proposed a kernel with **no
layer allocation** (`layer: null`; only `realized_in_layers`).
`scripts/validate_model.py` rejected that shape: an abstract entity
must declare `realized_in_layers` (check #7), and `realized_in_layers`
is an array of layer IDs from `architecture.layers` — so the kernel
must declare at least one layer. Resource (ADR-0005) follows the same
pattern (abstract + `layer: L3`). This matches the precedent and keeps
the kernel's "abstract + completeness_contract" semantics intact.

**Decision AR-FMWK-01-D02** — Add `dea:entity-business-process` to
the root model as the **first Core specialization** of
`dea:entity-process`. Allocated to `layer: L3`,
`building_block: L3-value-delivery`, with `class_alias: BP`
(preserved from the prior allocation). `specializes: PRC` (the
kernel's `class_alias`, per the schema constraint that `specializes`
takes an alias, not an entity_id).

**Decision AR-FMWK-01-D03** — The legacy root-model entry
`dea:entity-process` is **retained as the abstract kernel**, with
`class_alias: PRC` (Process) and `display_name: Process` (the
kernel-true name). A new entry `dea:entity-business-process` carries
the legacy alias `BP` and the legacy `display_name: Business Process`.
This preserves backward compatibility: existing consumers that
reference `class_alias: BP` continue to resolve against the
specialization, not the kernel.

**Decision AR-FMWK-01-D04** — `scripts/validate_consumer.py` gains
a third branch: if the root-model entity has `abstract: true`
and lacks both `layer` and `dimension`, the consumer's pointer
need not declare a layer or dimension for that entity; the
class_alias check still applies. The discriminator check (if
declared in the root model) still applies.

## 4. Required Changes — `dea-architecture-framework`

### 4.1 Root model: model version bump

`model/opendeam-model.yaml`:

- `model.version: 0.5.0` → `model.version: 0.6.0` (structural change;
  new abstract kernel introduced; ADR-0005 edit rules require a
  minor version bump).
- `VERSION` file: `0.5.0` → `0.6.0`.

### 4.2 Root model: model top header

The header block (lines 1–75) gains a "CHANGE FROM v0.5.0" section
recording:

- New abstract root-model entry: `dea:entity-process` (kernel; no
  layer; `discriminator: process-kernel`).
- New specialization: `dea:entity-business-process` (L3;
  `specializes: dea:entity-process`; replaces the old
  `dea:entity-process` allocation).
- Legacy `dea:entity-process` semantics migrate to the kernel; the
  catalog's specialization pointer is `dea:entity-business-process`.
- Validator extension: abstract kernel branch in
  `scripts/validate_consumer.py`.

### 4.3 Root model: allocation.entities[] edits

Two coordinated edits to `allocation.entities[]` (around line 500):

1. **Replace** the existing `dea:entity-process` block (lines 500–508)
   with a renamed block that declares the kernel:

   ```yaml
   - entity_id: dea:entity-process
     class_alias: PRC
     display_name: Process
     layer: L3
     building_block: L3-value-delivery
     status: proposed
     catalog_repo: null
     abstract: true
     discriminator: process-kernel
     realized_in_layers: [L3]
     entity_role: content
     completeness_contract: >
       Any T2 catalog specializing Process must declare its context
       (Business, Operational, Engineering, etc.) via `specializes:`
       on its metamodel pointer; the kernel itself is not directly
       allocated to a layer. (CR-AR-FMWK-01; mirrors ADR-0005 D3
       Resource template.)
     legacy_ids:
     - dea:entity-process         # semantic preservation
     description: >
       The OpenDEAM Process kernel (CR-MM-PROC-01; abstract; aligned
       with WSF wsf:Process). Structural organization of activities
       into a meaningful temporal/causal pattern. Specializations
       carry the context (Business, Operational, Engineering).
   ```

2. **Add** a new entry immediately after the kernel:

   ```yaml
   - entity_id: dea:entity-business-process
     class_alias: BP
     display_name: Business Process
     layer: L3
     building_block: L3-value-delivery
     status: scaffold
     catalog_repo: dea-catalog-processes
     specializes: PRC
     measured_by: [MTR]
     entity_role: content
     description: >
       The OpenDEAM Business Process specialization (CR-MM-PROC-01;
       CR-BP-SPEC-BP-01). A structured set of activities that
       produces a defined outcome in the Business context.
       Sub-classifications (operational / support / management,
       carried by the catalog's process_intent field) are
       catalog-internal; they do not promote to root-model
       entities.
   ```

### 4.4 Validator extension: abstract-kernel branch

`scripts/validate_consumer.py`:

Current behaviour (lines 41–66): an entity without `layer` is
treated as a dimension entity; the consumer must declare
`dimension:` in its pointer.

New behaviour (after this CR): an entity with `abstract: true` and
neither `layer` nor `dimension` is treated as an **abstract
kernel**. The consumer pointer may declare the entity id without a
layer or dimension; the class_alias and discriminator checks still
apply. A non-abstract entity without `layer` is still treated as
a dimension entity (no behaviour change for non-abstracts).

The new branch is a single conditional in `check_one()`:

```python
if "layer" in canon:
    # ... existing layer branch (unchanged) ...
elif canon.get("abstract"):
    # New: abstract kernel branch (CR-AR-FMWK-01).
    if mm.get("layer"):
        errors.append(
            f"drift: {entity_id} is an abstract kernel; {label} should "
            f"not declare layer={mm.get('layer')}"
        )
    if mm.get("dimension"):
        errors.append(
            f"drift: {entity_id} is an abstract kernel; {label} should "
            f"not declare dimension={mm.get('dimension')}"
        )
    # Note: pointer may declare the entity id standalone (e.g.
    # dea:Process in a multi-entity list) without layer/dimension.
    # The class_alias check below still applies.
else:
    # ... existing dimension branch (unchanged) ...
```

The `discriminator` check (line 74) already requires the consumer
to declare the discriminator if the root model declares one; this
applies uniformly to all branches.

### 4.5 `validate_model.py` must still pass

`scripts/validate_model.py` (the model's own internal validator)
must accept the new abstract-kernel entries. Read it first; if it
flags abstract-without-layer entries, extend its check to mirror
the consumer extension. (The consumer extension above should be
sufficient because the model's internal validator usually checks
shape and ADR-compliance; abstract-with-no-layer is ADR-0005 D3
compliant.)

### 4.6 ADRs and CHANGELOG

- `docs/ADRs/ADR-0006-opendeam-v0.6.0-process-kernel.md` (new ADR;
  required by the structural-change edit rules). Records:
  - The Process kernel introduction.
  - The Business Process specialization.
  - The legacy-id migration semantics.
  - The validator extension.
  - The decision to keep the root-model version `v0.6.0`.
- `README.md`: bump version `0.5.0` → `0.6.0` in the badge /
  header.
- `CHANGELOG.md` (if present): record the v0.6.0 change set.

## 5. Sequencing (after Sign-Off)

1. Branch `feature/cr-ar-fmwk-01-process-kernel` on
   `dea-architecture-framework`.
2. Land CR-AR-FMWK-01.md verbatim to `change-requests/`.
3. Apply the model edits (4.1, 4.2, 4.3, 4.4).
4. Apply the validator edits (4.4).
5. Local verification (validator + model validator + test suite
   if present).
6. Open PR; pause-before-merge per convention.
7. After merge, tag `v0.6.0` on `dea-architecture-framework`
   (consumer pins update is downstream of the tag).
8. The catalog's CR-BP-SPEC-BP-01 pointer's `model_ref` advances
   from `v0.5.0` to `v0.6.0` in CR-BP-SPEC-BP-01 §5.2.

## 6. Acceptance Criteria

- [ ] `model.version: 0.6.0` recorded.
- [ ] `VERSION: 0.6.0` file content.
- [ ] `dea:entity-process` declared as abstract kernel (`class_alias: PRC`;
      `layer: L3`; `building_block: L3-value-delivery`; `status: proposed`;
      `abstract: true`; `discriminator: process-kernel`;
      `realized_in_layers: [L3]`; `completeness_contract`).
- [ ] `dea:entity-business-process` declared as specialization
      (`class_alias: BP`; `layer: L3`; `building_block: L3-value-delivery`;
      `specializes: PRC`; `catalog_repo: dea-catalog-processes`).
- [ ] `scripts/validate_consumer.py` accepts abstract-kernel
      entities without requiring a `dimension:` field.
- [ ] `scripts/validate_model.py` passes (54 entities; 70 relationships).
- [ ] Local dry-run: the catalog's future pointer
      (`dea:entity-business-process` + `entities: [dea:entity-process]`)
      validates 0-drift against the new model.
- [ ] ADR-0006 lands with all required sections.
- [ ] README badge bumped to v0.6.0.

## 7. Out of Scope

- The introduction of `dea:entity-operational-process`,
  `dea:entity-engineering-process`, or any other Process
  specialization beyond Business. Gated on concrete demand.
- The catalog-side re-anchoring (CR-BP-SPEC-BP-01). This CR
  unblocks it.
- Workflow / Activity semantics (WSF discipline applies
  unchanged).
- The dea-catalog-processes `validate-allocation` workflow
  itself; that workflow will pick up the new model automatically
  via the `model_ref` pin update in CR-BP-SPEC-BP-01 §5.2.

## 8. References

- `dea-metamodel/change-requests/CR-MM-PROC-01.md` (this CR's
  dependency; merged PR #163).
- `dea-metamodel/metamodel/dea-metamodel.yaml:562+` (kernel entry;
  after CR-MM-PROC-01).
- `dea-architecture-framework/docs/ADRs/ADR-0005-opendeam-v0.5.0-metamodel-governance-resource-information.md`
  (Resource template; ADR-0005 D3).
- `dea-architecture-framework/model/opendeam-model.yaml:500–508`
  (current `dea:entity-process` allocation; replaced by this CR).
- `World-Semantic-Foundation/00_inbox/WSF-Foundational-Semantic-Synthesis-baseline-insight.md`
  §6 (Capability Becomes Specialization; template).

## 9. Pitfalls

- The validator extension (4.4) must not change the dimension
  branch's behaviour for non-abstract entities; a regression here
  would silently accept declarations that previously failed.
- The legacy root-model entry (`dea:entity-process`) is renamed
  in `display_name` ("Business Process" → "Process") and gains
  `discriminator: process-kernel`. Consumers that grep for
  the legacy display_name must migrate to either the new
  `dea:entity-business-process` entry or the kernel's
  `display_name: Process`.
- The `discriminator` check (validator line 74) already exists
  and will require the catalog pointer to declare
  `discriminator: process-kernel` when it references the
  kernel. This is an additional pointer field not present in
  CR-BP-SPEC-BP-01 §5.2's draft; a follow-up edit may be needed.

## 10. Provenance

- Date: 2026-09-03
- Triggered by: CR-MM-PROC-01 (metamodel kernel) merge at
  PR #163; user reframe 2026-09-03 (WSF as authoritative on
  Process).
- Working folder: `/home/hermes/dea-work/process/00_inbox/`.
- Supersedes: the implicit root-model lag that CR-MM-PROC-01
  exposed on the consumer side.