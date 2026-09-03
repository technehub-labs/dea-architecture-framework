# ADR-0006: OpenDEAM v0.6.0 — Process Kernel + Business Process Specialization

**Status:** Accepted
**Supersedes:** opendeam-model.yaml v0.5.0 (see ADR-0005)
**Version bump:** MINOR (0.5.0 → 0.6.0) — new abstract root-model kernel + new specialization + consumer-validator extension. No new layers or building blocks.

## Context

The DEA metamodel and the dea-catalog-processes catalog are aligning on a **kernel + specializations** discipline for the Process concept, mirroring the established Capability + specialization discipline (dea-metamodel, CR-016 / ADR-015). This ADR synchronizes the OpenDEAM root model with that alignment.

The discipline is rooted in the upstream **WSF (World Semantic Foundation)** discipline: `wsf:Process` is the foundational reference class (Tier-3 derived construct; structural activity organization; WSF Foundational Semantic Synthesis §6). DEA inherits via specialization. "Business" is one specialization context (Business Architecture / Business Operations); other specialization contexts (Operational, Engineering) may exist without being mistaken for the kernel.

The root model at v0.5.0 declared `dea:entity-process` as a single layer-allocated entity (L3; `class_alias: BP`; `display_name: Business Process`). That single-entity shape conflicted with the kernel + specialization discipline: a kernel cannot be `Business Process` if "Business" is supposed to be one specialization context among several.

This ADR resolves the conflict by splitting `dea:entity-process` into two entries:

1. The **kernel** (`dea:entity-process`; `class_alias: PRC`; abstract; layer L3; `discriminator: process-kernel`; `completeness_contract` for the T2-catalog specialization contract; `legacy_ids: [dea:entity-process]`).
2. The **first Core specialization** (`dea:entity-business-process`; `class_alias: BP`; `display_name: Business Process`; layer L3; `specializes: PRC`; `catalog_repo: dea-catalog-processes`).

This mirrors the existing Resource kernel + specializations template (ADR-0005 D3).

## Decisions

### D1 — Process kernel + Business Process specialization discipline

**Decision:** Mirror the Capability + specialization discipline (CR-016 / ADR-015) and the Resource kernel + specializations discipline (ADR-0005 D3) for the Process concept:

  - **Kernel** (`dea:entity-process`): abstract; `class_alias: PRC`; `layer: L3`; `building_block: L3-value-delivery`; `status: proposed`; `abstract: true`; `discriminator: process-kernel`; `realized_in_layers: [L3]`; `entity_role: content`; `completeness_contract` for T2-catalog specialization contract; `legacy_ids: [dea:entity-process]`; description aligned with WSF `wsf:Process` + dea-metamodel `dea:Process`.
  - **First specialization** (`dea:entity-business-process`): concrete; `class_alias: BP` (preserved from v0.5.0 allocation for backward compatibility); `display_name: Business Process`; `layer: L3`; `building_block: L3-value-delivery`; `status: scaffold`; `specializes: PRC`; `catalog_repo: dea-catalog-processes`; `measured_by: [MTR]`; `entity_role: content`.
  - Sub-classifications (operational / support / management; carried by the catalog's `process_intent` field) are **catalog-internal**. They do not promote to root-model entities. (This matches how Business Capability sub-taxonomies are handled in `dea-catalog-business-capabilities`.)

**Note on layer allocation of the kernel:** an earlier draft of this ADR proposed a kernel with **no layer allocation** (`layer: null`). `scripts/validate_model.py` rejected that shape: an abstract entity must declare `realized_in_layers` (check #7), and `realized_in_layers` is an array of layer IDs from `architecture.layers`. The Resource kernel (ADR-0005) follows the same pattern (abstract + `layer: L3`). This matches the precedent and keeps the kernel's "abstract + completeness_contract" semantics intact.

**Note on `class_alias` choice:** the kernel gets `PRC` (3 chars, ≤ schema maxLength of 5) instead of `BP`. The `BP` alias is preserved on the new `dea:entity-business-process` specialization so existing catalog consumers that declare `class_alias: BP` continue to resolve against the specialization (backward compatibility).

**Note on `specializes` value:** `specializes` takes a `class_alias`, not an entity_id (schema constraint; `maxLength: 5`). The Business Process specialization declares `specializes: PRC` (pointing to the kernel's alias).

### D2 — Consumer-validator extension: abstract-kernel branch

**Decision:** `scripts/validate_consumer.py` gains a third branch that handles abstract root-model kernels. The validator previously routed consumers to one of two paths:

  - **Layer-allocated branch**: if `canon["layer"]` exists, require `mm["layer"] == canon["layer"]`.
  - **Dimension branch**: if `canon` has no `layer`, require `mm["dimension"]` to name an orthogonal allocator.

The new branch is **first** in the order, since `abstract: true` is the most specific signal:

  - **Abstract-kernel branch**: if `canon["abstract"]` is true:
    - **Skip** the layer-equality check (the kernel's layer is for the model's own constraint; the consumer declares the kernel id without claiming a layer of its own).
    - **Reject** `mm["layer"]` and `mm["dimension"]` in the consumer pointer for the kernel (the kernel is realized by specializations, not allocated to a layer directly).
    - **Still check** `mm["class_alias"] == canon["class_alias"]` (the kernel alias must echo exactly).
    - **Still check** `mm["discriminator"] == canon["discriminator"]` if the kernel declares a discriminator (the consumer must echo the discriminator contract).

**Why this matters:** without the new branch, a consumer pointer that declares the kernel id in a multi-entity `entities:` list (typical for a T2 catalog that specializes a kernel) trips the dimension branch's "must declare dimension" check, false-positiving as drift.

### D3 — Consumer-validator scenario matrix (verified)

The validator extension was verified locally against five scenarios:

| # | Scenario | Expected | Result |
|---|---|---|---|
| A | Future catalog pointer: kernel + specialization (`entities: [PRC, BP]`) | PASS | PASS |
| B | Legacy pointer: BP-only (`layer=L3`; no discriminator) | FAIL (3 drifts) | FAIL (abstract-kernel drift, class_alias drift, discriminator drift) |
| C | Kernel pointer with `layer=L3` | FAIL (abstract-kernel constraint) | FAIL (abstract-kernel drift) |
| D | Specialization-only pointer (BP, L3) | PASS (backward compat for v0.6.0 consumers) | PASS |
| E | Specialization with bad class_alias (`WRONG`) | FAIL | FAIL (class_alias drift) |

All 5 scenarios behaved as expected.

### D4 — Authority chain (end-to-end)

The kernel + specialization discipline propagates through the layered authority chain:

  - **WSF** (org): `wsf:Process` (Tier-3 derived; structural activity organization). The upstream reference class.
  - **`dea-metamodel`** (canonical Core authority): `dea:Process` (abstract Core kernel; CR-MM-PROC-01; merged PR #163 / commit `1665209`) → `dea:BusinessProcess` (Core specialization). Federation mapping `dea:Process ↔ wsf:Process` (EXACT; LOSSLESS).
  - **`dea-architecture-framework`** (root model; **v0.6.0**): `dea:entity-process` (abstract kernel; `PRC`) → `dea:entity-business-process` (specialization; `BP`). Mirrors the metamodel discipline in the root-model layer.
  - **`dea-catalog-processes`** (catalog authority; CR-BP-SPEC-BP-01): declares both ids in its metamodel pointer (kernel entry in a multi-entity `entities:` list; specialization as the primary `metamodel:` block).

## Consequences

### Positive

- **Semantic consistency end-to-end**: the kernel + specialization discipline propagates from WSF through dea-metamodel, the root model, and the T2 catalogs. A reader of any layer sees the same discipline.
- **Backward compatibility preserved**: the legacy `BP` class_alias continues to resolve against the new Business Process specialization. Existing catalog consumers pinned to v0.5.0 that declare `metamodel.entity_id: dea:entity-process` will fail validation against v0.6.0 — this is expected; they should declare `metamodel.entity_id: dea:entity-business-process` and add the kernel to `entities:` with `discriminator: process-kernel`.
- **Other Process specializations (Operational, Engineering, etc.) can be added** in future ADRs without changing this template. Each specialization gets its own `class_alias` (≤5 chars) and its own `catalog_repo`.
- **Sub-classifications remain catalog-internal** (operational / support / management; via `process_intent`). The root model stays metamodel-strong.

### Negative

- **Minor version bump required** (per ADR-0005 D3 edit rules — introducing a new abstract root-model kernel is a structural change). Catalog repos pinned to `v0.5.0` of the root model will fail `validate-allocation` against the new v0.6.0 root model. The catalog's `metamodel-pointer.yaml` `model_ref` must advance to `v0.6.0`.
- **The kernel's `class_alias` is `PRC`, not `BP`**. This is a one-time cost; subsequent specializations will follow the same pattern.

### Neutral

- **No new layers or building blocks.** The kernel lives at `L3` / `L3-value-delivery` (same as Business Process). The two entries share the same building block.
- **The validator's dimension branch is unchanged in behaviour** for non-abstract entities. The new abstract-kernel branch is purely additive.

## Scope for follow-on work (not in this ADR)

- **CR-AR-FMWK-02** (future): introduce additional Process specializations (`dea:entity-operational-process`, `dea:entity-engineering-process`, etc.) when concrete demand exists. Each future ADR follows this same kernel + specialization template.
- **CR-AR-FMWK-03** (future): introduce other kernel + specialization chains (e.g. Activity kernel + Workflow specialization). The validator extension in D2 supports any abstract kernel + any number of specializations.

## Provenance

- **CR:** CR-AR-FMWK-01 (`change-requests/CR-AR-FMWK-01.md`).
- **Predecessor ADR:** ADR-0005 (Resource kernel + specializations; v0.5.0).
- **Predecessor CR (cross-repo):** CR-MM-PROC-01 (`dea-metamodel`; merged PR #163 / commit `1665209`).
- **Cross-repo CRs gated on this ADR:** CR-BP-SPEC-BP-01 (`dea-catalog-processes`); CR-BP-02 (Process Context register).
- **Date:** 2026-09-03.
- **Author:** Coder (for eaojnr).