# ADR-0005: OpenDEAM v0.5.0 — Metamodel Governance Layer (entity_role, completeness_contract) + Resource & Information/Knowledge

**Status:** Accepted
**Supersedes:** opendeam-model.yaml v0.4.0
**Version bump:** MINOR (0.4.0 → 0.5.0) — new terminology mechanism, two new building blocks, five new entities.

## Context

This ADR resolves a level confusion in the review that led here (Cash, Equipment, Lease, Inventory, and Product were nearly added as entities when they are catalog-level instances of categories the model already has or should have), and formalizes two things stated in discussion but not yet written into the model:

1. **The metamodel/information-model boundary.** OpenDEAM defines *types of things* (a Resource, a Business Object); a T2 catalog defines *specific things* (a forklift, a customer record). An entity earns metamodel status only if it names a category with its own distinct lifecycle and relationship pattern, applicable regardless of industry — not because a plausible real-world example exists.
2. **The metamodel is prescriptive, not just descriptive.** OpenDEAM doesn't merely tolerate a catalog's internal sub-taxonomy as out-of-scope; for entities that anchor a category (abstract parents, and entities whose job is to constrain other entities), it defines the *completeness contract* that sub-taxonomy must satisfy to be a valid instantiation. This is the mechanism that lets a layer stay "metamodel-strong" while still allowing a catalog to zoom into its own ontology space underneath.

## Decisions

### D1 — Formalize the metamodel/information-model boundary as a standing filter

**Decision:** Add `terminology.metamodel_boundary`, stating the test explicitly: a candidate entity is metamodel-eligible only if it is a *category* (type-of-type) with a lifecycle and relationship pattern distinct from every existing entity, not a *value*, *instance*, or *industry-specific flavor* of one. Instances belong in the T2 catalog governed by the category's schema.

**Applied retroactively to the candidates that prompted this ADR:**
- **Cash** → catalog instance of `Financial Resource` (new, D3). Not an entity.
- **Equipment** → catalog instance of `Physical Resource` (new, D3). Not an entity.
- **Lease** → already fully covered — a catalog instance of `Collaboration Agreement` (L1). No gap; corrects an error in the prior message.
- **Inventory** → not one thing. Splits cleanly along an existing layer boundary: the physical stock is a `Physical Resource` (L3, new); the record of that stock is an `Information Asset` (L4, new, D4). Its ambiguity was evidence the L3/L4 split is doing its job, not a gap.
- **Product** → catalog instance of `Business Object` (already exists). **Not** a specialization of "Value" — Value Exchange (L1) names a *flow/relationship*, not a bounded entity with its own lifecycle. Treating Value as a parent type would repeat the category error already ruled out for Measurement (ADR-0002 D1).

### D2 — Add `entity_role` and `completeness_contract` as governance-layer fields

**Decision:** Add two optional fields to the entity schema:
- `entity_role: content | governance` — **content** entities are things an enterprise operates with, populated by T2 catalogs (Business Process, Data Entity, Financial Resource). **governance** entities exist to constrain or define the shape of other entities' catalogs (Concept, Architecture Pattern, Blueprint, Tenet, Guardrail).
- `completeness_contract` — a stated rule, carried by abstract category roots and governance-role entities, defining what a T2 catalog under that entity must classify by or satisfy to count as MECE-complete. This is the mechanism that makes zoom-in prescriptive rather than merely permitted.

**Scope for this ADR:** these two fields are declared in `terminology` and applied only to the entities introduced below, as a worked example. Retrofitting `entity_role`/`completeness_contract` onto the other 47 existing entities is a materially larger structural pass and is explicitly deferred to its own future ADR — see Consequences.

### D3 — Add `Resource` (abstract) with three specializations, in a new L3 building block

**Derivation:** `"bounded entity"` — a bounded entity has its own economic substrate it must maintain to persist, distinct from what it exchanges (L1: Value Exchange, a flow) and distinct from what it builds digitally (L4/L5).

**Decision:** Add `Resource` — layer L3, `abstract: true`, `entity_role: content`, carrying a `completeness_contract`: any T2 catalog specializing Resource must classify instances along exactly one of three governed dimensions — **liquidity** (Financial Resource), **maintenance regime** (Physical Resource), or **legal protection type** (Intangible Resource) — because each dimension implies a genuinely different relationship and governance pattern, not merely a different label.

**New building block:** `L3-resources` (Enterprise Resources), added to L3.

**New entities (all `specializes: RES`, layer L3, building_block L3-resources):**
- `Financial Resource (FR)` — liquid or near-liquid economic value the enterprise holds. `funds Investment Initiative`.
- `Physical Resource (PHR)` — tangible assets requiring upkeep. `enables Business Process`.
- `Intangible Resource (INR)` — legally protected non-physical value (IP, brand, licenses). `protects Business Capability`.

**Why this makes the model hold for a small business, not only a platform business:** L3 was previously heavily service/data-oriented (Work Organization, Value Delivery, Business Information, Service Offerings). A bakery's oven or a courier's van had no home. Resource is the tangible/economic substrate the operating model runs on, regardless of digital maturity.

### D4 — Add `Information Asset` and `Knowledge Asset` in a new L4 building block

**Derivation:** `"persists by exchanging value"` (digital plane) — Data Entity (existing, L4) models raw facts; persistence also requires those facts given context and shape for a consuming purpose (Information), and applied know-how made explicit and durable independent of any one Actor (Knowledge). This completes the Data→Information→Knowledge progression on the digital plane. (Wisdom is deliberately excluded — it fails the non-generic-derivation filter, the same test that excluded a standalone AI layer and Sustainability.)

**New building block:** `L4-information-knowledge` (Information & Knowledge), added to L4.

**New entities:**
- `Information Asset (IA)` — layer L4, `entity_role: content`. Data given context/form for a specific consumer or purpose (a report, dashboard, invoice). `contextualized from Data Entity`; `consumed by Actor`.
- `Knowledge Asset (KA)` — layer L4, `entity_role: content`. Applied know-how made explicit and durable, distinct from `Skill` (which an Actor *possesses*) — a Knowledge Asset exists independent of any one Actor. `captured from Actor`; `informs Tenet`.

**Reconciling with Skill (L3, ADR-0003 D4):** Skill is tacit/embodied capability held by a person. Knowledge Asset is what's left when that capability is made explicit enough to survive the person leaving. They're related (a Knowledge Asset can document what a Skill requires) but are not the same category — kept as two entities, not merged, because their lifecycles genuinely differ (Skill: acquired/assessed/developed by an individual; Knowledge Asset: captured/versioned/decays and needs refresh as an organizational artifact).

## Consequences

- L3 building blocks: 5 → 6 (adds `L3-resources`).
- L4 building blocks: 6 → 7 (adds `L4-information-knowledge`).
- New entities: Resource (abstract), Financial Resource, Physical Resource, Intangible Resource, Information Asset, Knowledge Asset — 6 total (1 abstract + 5 concrete/leaf).
- New entity schema fields: `entity_role`, `completeness_contract` — optional, applied only to the six new entities in this ADR.
- New relationships: `FR funds II`, `PHR enables BP`, `INR protects CAP`, `IA contextualized from DE`, `IA consumed by AC`, `KA captured from AC`, `KA informs TNT`.
- **Deferred, explicitly out of scope for v0.5.0:** retrofitting `entity_role`/`completeness_contract` onto the other 47 entities. Recommended as its own future ADR once the mechanism has been exercised in practice against these six and any friction is known. That ADR should also introduce the validator rule "abstract or governance-role entities MUST carry `completeness_contract`" — deliberately not enforced now, to avoid over-fitting the validator to one worked example.
- **Deferred:** formal `completeness_contract` validation in CI — recommended as a fast-follow once a second and third worked example exist, to avoid over-fitting the validator to one case.

## Review Amendments (adoption review, 2026-08-15)

Recorded here so the ADR remains the complete decision record:

1. **`terminology.abstract_entities` broadened in the model** — the original text defined abstract entities as cross-layer realization parents only, contradicting D3's same-layer `Resource` root. Amended at adoption to formally admit same-layer category roots carrying a `completeness_contract`. (Without this, the model's glossary contradicted its content while CI stayed green.)
2. **Schema declarations added** — `entity_role` (enum: `content` | `governance`) and `completeness_contract` (string) are declared in `schemas/opendeam-model.schema.json`; without declarations they validated as uncontrolled free-form extras.
3. **Repo-per-specialization confirmed as the intended pattern** for Resource subclasses (dea-catalog-financial-resources, -physical-resources, -intangible-resources), diverging deliberately from Solution Component's shared-repo + discriminator pattern: the completeness contract's single-dimension rule is then enforced structurally by repo separation. This sets the precedent for future category roots.
4. **Earmarked, not fixed:** D1's Lease mapping references Collaboration Agreement's catalog, but CA carries `catalog_repo: null`. Conceptually consistent; a CA catalog is a future candidate, not a v0.5.0 gap.
