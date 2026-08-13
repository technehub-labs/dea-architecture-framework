# ADR-0002: OpenDEAM v0.2.0 — Structural Upgrade

**Status:** Accepted
**Supersedes:** opendeam-model.yaml v0.1.0 (alpha)
**Version bump:** MINOR (0.1.0 → 0.2.0) — per the model's own edit rules, this is a structural change (layer re-scoping, new dimension, entity re-allocation) and therefore requires this ADR.

## Context

A review of v0.1.0 surfaced eight structural weaknesses. Each is real but not equally serious. This ADR fixes the ones that would otherwise get baked into the T1 machine-schema generation (TTL/SQLite/Pydantic) and become expensive to unwind later. It deliberately does *not* fix cosmetic issues that carry no downstream cost.

## Decisions

### D1 — Demote Measurement from a numbered layer to a cross-cutting dimension

**Problem:** L6 has one building block, no internal qualifier logic comparable to L1–L5, and its own `derivation` text ("measurement cuts across all layers") argues against treating it as a peer layer.

**Decision:** Remove L6 as an architecture layer. Model measurement as a second `orthogonal_allocator`, parallel to the ECF matrix, named `measurement-dimension`. `Performance Metric` becomes an entity with no home layer of its own — instead every measurable entity carries an optional `measured_by: [MTR...]` back-reference, and Metric itself carries `scope_layers: [L1..L5]` to declare which layers it can evaluate.

**Consequence:** The layer count changes from 6 to 5. This is the single biggest structural change in this ADR and is why it needs a minor bump rather than a patch.

**Rejected alternative:** Give L6 more building blocks (health, adoption, compliance, risk breakdowns) to make it structurally symmetric with the others. Rejected because it treats the symptom (asymmetric building-block count) rather than the cause (measurement isn't a layer, it's a dimension — same category error the model already avoided for ECF).

### D2 — Move Collaboration Agreement from L2 to L1

**Problem:** `EA →(engages in)→ CA →(governs)→ VE` places the thing that governs the exchange in a different layer than the exchange itself and the actor who is party to it. L1's derivation is "the exchange surface"; an agreement *is* a feature of that surface, not an internal governance rule.

**Decision:** Add `L1-agreements` building block; reallocate `dea:entity-collaboration-agreement` from `L2-agreements` to `L1-agreements`. Remove the now-empty `L2-agreements` building block. L2 keeps only genuinely internal-facing governance products (Intent, Rules & Guidance, Reusable Knowledge, Semantics, Architecture Views).

**Consequence:** L1 becomes: External Parties, Value Flows, Experience Points, Agreements. L2 loses one building block.

### D3 — Make layer-spanning abstract entities explicit

**Problem:** `Solution Component` is declared in L3 but its three subclasses (Application/Infrastructure/Integration Component) live in L5. This is a legitimate pattern (abstract parent, concrete children in different layers) but v0.1.0 enforced it only implicitly via `component_type`, with no schema signal.

**Decision:** Add two fields to the entity schema: `abstract: bool` and `realized_in_layers: [layer ids]`. `Solution Component` is marked `abstract: true, realized_in_layers: [L5]`. Its three subclasses stay in L5 as before but now carry `specializes: SC`. This makes the split machine-checkable instead of convention-only.

### D4 — Add a relationship type taxonomy and cardinality

**Problem:** All 40 relationships share one untyped schema (`from`, `to`, `label`, `style`). `style: solid/dashed` is being used as an implicit, undocumented stand-in for relationship semantics.

**Decision:** Add `rel_type` (controlled vocabulary: `realization | composition | aggregation | dependency | flow | governance | association`) and `cardinality` (`0..1 | 1 | 0..N | 1..N` on each side, expressed as `"1:N"` etc.) to every relationship. `style` is retained only as a rendering hint derived from `rel_type` (viewers should compute it, not authors set it) — kept for backward compatibility with T3 viewers but marked `deprecated: prefer rel_type`.

**Consequence:** Every one of the 40 relationships needs re-classification. This is mechanical but real work; done for all of them in the attached model file.

### D5 — Define the entity/relationship lifecycle formally

**Problem:** `status` values (`planned`, `scaffold`, `existing`) were used with no defined state machine, inconsistent with the model's own ADR-for-structural-change discipline.

**Decision:** Add a `lifecycle` block to `terminology` defining the ordered states `proposed → planned → scaffold → existing → deprecated → retired`, and the rule that any backward transition (e.g. `existing → planned`) or `→ retired` requires an ADR, while forward transitions only require a PR.

### D6 — Document shared `catalog_repo` usage

**Problem:** `dea-catalog-patterns` and `dea-catalog-application-components` are each reused across unrelated or related-but-distinct entities with no documented rule.

**Decision:** Add a `terminology.shared_catalog_convention` note: a `catalog_repo` may be shared by multiple entities only if every entity sharing it declares a `discriminator` field naming the property that distinguishes its instances within that repo (mirrors the existing `component_type` pattern). Retrofitted onto the three `dea-catalog-application-components` entities, the two `dea-catalog-patterns` entities, and — caught by the upgraded validator on first run — the two `dea-catalog-digital-business-service-factory` entities (`Business Service` and `Solution Component`, discriminator `entry_kind`).

### D7 — Demonstrate `ecf_coordinates` usage

**Problem:** The ECF orthogonal allocator was documented but never exercised by any entity in the file, so the file couldn't validate its own claim.

**Decision:** Add example `ecf_coordinates: {domain: <TBD>, stage: <TBD>}` stubs (nullable, to be populated by ADR-owning teams) to the two entities the model text already names as ECF-bearing: `Business Capability` and `Business Object`.

## Deferred (explicitly out of scope for v0.2.0)

- Formal cardinality validation in CI (`validate_model.py`) — recommended as a fast-follow once `rel_type`/`cardinality` fields exist to validate.
- Full retrofit of `ecf_coordinates` across all ECF-eligible entities — left to catalog-owning teams per entity, since populating real coordinates is a content task, not a structural one.
- Splitting `L3-service-offerings` further — D3's `abstract`/`realizes` fields resolve the ambiguity without requiring entity movement.

## Consequences

- Layer count: 6 → 5.
- One building block removed (`L2-agreements`), one added (`L1-agreements`).
- Entity schema gains 4 optional fields: `abstract`, `realizes`/`specializes`, `discriminator`, `ecf_coordinates`, `measured_by`.
- Relationship schema gains 2 required fields: `rel_type`, `cardinality`; `style` becomes deprecated/derived.
- Downstream T1 (`dea-metamodel`) must regenerate TTL/SQLite/Pydantic types against the new schema — breaking change for consumers pinned to v0.1.x tags, hence the minor bump.
