# ADR-0004: OpenDEAM v0.4.0 — L2 Cleanup & TOGAF-Vocabulary Purge

**Status:** Accepted
**Supersedes:** opendeam-model.yaml v0.3.0
**Version bump:** MINOR (0.3.0 → 0.4.0) — entity removal, entity merge, three renames, building-block removal.

## Context

Six L2 entities — Glossary Term, Reference Model, Principle, Standard, Viewpoint, and Taxonomy Node — had zero relationships to anything else in the model. That's not a wiring oversight; it's a symptom. All six are TOGAF Architecture Content Framework artifacts (Principles Catalog, Standards Information Base, Reference Models, Glossary) imported nearly verbatim, including the name. I stated "don't repeat TOGAF" as a design constraint and then failed to apply it to my own additions. This ADR corrects both the structural problem (orphaned entities) and the naming problem (borrowed vocabulary) together, because in this case they're the same root cause: importing TOGAF's artifact catalog imports TOGAF's framing along with it, and that framing is what made these six feel like documentation-shelf items rather than things that act on anything.

**Guiding reframe for this ADR:** classical EA treats these as *static reference documents* — catalogs you consult. Modern digital-native practice treats the equivalent concepts as *active, often automated, mechanisms* — guardrails-as-code, policy-as-code, platform golden paths, a queryable concept graph. The renames below aren't cosmetic; each one changes what the entity actually *does* in the model.

## Decisions

### D1 — Remove Viewpoint from the architecture entirely

**Finding:** Viewpoint is a perspective *on* the metamodel for rendering/tooling purposes — it was never a thing that exists *in* the enterprise, which is exactly why it could never have a relationship to a Business Process or Capability. It doesn't belong in this model at all.

**Decision:** Delete `dea:entity-viewpoint` and the now-empty `L2-architecture-views` building block. Viewpoint-equivalent concepts belong to the T3 tooling tier (`dea-web-viewer`) as a rendering configuration, not an architecture entity.

### D2 — Merge Glossary Term + Taxonomy Node into a single cross-cutting `Concept`, demoted to an orthogonal dimension

**Finding:** These two were the same category error `Measurement` was before ADR-0002 D1: semantics doesn't belong to one layer, it labels entities *across all of them*. They were two names for one underlying idea (a defined term with hierarchical relationships to other terms) split apart for no structural reason.

**Decision:** Merge into one entity, `Concept`, with a `parent_concept` field for hierarchy (replacing Taxonomy Node's tree structure). Remove the now-empty `L2-semantics` building block. Add new `orthogonal_allocator`: `semantic-dimension` — any entity across L1–L5 may carry `defined_by: [Concept ids]`, the same pattern used for `measured_by` and `governed_by`.

**Naming note:** "Glossary" and "Taxonomy" are themselves inherited EA-documentation vocabulary (static, human-curated reference lists). "Concept" plus a `defined_by` graph reframes this as what it actually is in modern practice: a queryable knowledge/concept graph any entity links into, closer to how a data catalog or a knowledge graph works than a PDF glossary appendix.

### D3 — Rename Principle → Tenet; wire it to actually inform something

**Finding:** "Principle" is TOGAF's own term (the Principles Catalog) for a stated belief. As modeled, it stated the belief and connected to nothing — it governed nothing and nothing referenced it.

**Decision:** Rename to `Tenet` — a non-binding, human-authored belief (e.g. "API-first," "prefer managed services"). Add relationship `Tenet informs Guardrail` (D4). A Tenet by itself constrains nothing; it exists to justify and motivate the Guardrails that do.

**Why this is the modern-EA move, not just a synonym swap:** classical EA treats principles as persuasive documentation — read the catalog, try to comply. Splitting belief (Tenet) from enforcement (Guardrail) mirrors how platform engineering actually works today: a design tenet lives in a wiki or ADR; the thing that actually stops a non-compliant deploy is a policy-as-code rule. Collapsing both into one static "Principle" object, as TOGAF does, hides that distinction.

### D4 — Rename Standard → Guardrail; add an `enforcement` maturity field; wire it to Technology, Solution Component, and Control

**Finding:** The `Technology` entity's own description already claimed to be "governed via Standards + Principles," but no such relationship existed anywhere in the model — the model was breaking its own stated promise.

**Decision:** Rename to `Guardrail`. Add field `enforcement: advisory | automated-warn | automated-block | platform-enforced` — a maturity ladder from "documented recommendation" (TOGAF's whole model) up to "you structurally cannot violate this because the platform doesn't offer the non-compliant path" (the modern platform-engineering ideal, sometimes called a golden path when it's the *default*, not just the *permitted*, route). Add relationships:
- `Guardrail governs Technology`
- `Guardrail governs Solution Component`
- `Guardrail implements Control` — connects this directly to ADR-0003's Risk & Compliance block: a Guardrail is how a Control actually gets enforced in the digital estate, rather than being two disconnected governance vocabularies.

**Why this is the modern-EA move:** TOGAF's Standards Information Base is a static compliance list someone checks against manually. Framing the same concept as `Guardrail` with an `enforcement` level makes automatable, CI/CD-enforced compliance (OPA/Rego-style policy-as-code, cloud landing-zone guardrails) a first-class part of *what the entity is*, not an implementation detail left to whoever builds the pipeline.

### D5 — Rename Reference Model → Blueprint; wire it to Architecture Pattern

**Finding:** Reference Model and Architecture Pattern sat in the same building block with no stated relationship, despite an obvious one: a reference model is naturally a composition of patterns.

**Decision:** Rename to `Blueprint`. Add relationship `Blueprint composed of Architecture Pattern` (1:1..N).

**Naming note:** "Reference Model" is Zachman/TOGAF vocabulary for a static template. "Blueprint" is the term digital-native platform teams already use for the same underlying idea (a composed, reusable target-state design), without inheriting the connotation of a document you photocopy rather than a composition you actually assemble from parts.

### D6 — Remove now-empty building blocks; consolidate L2 from 7 to 5

**Decision:** `L2-architecture-views` (D1) and `L2-semantics` (D2) are deleted. `L2-rules-guidance` renamed (display name only, id unchanged) to **Tenets & Guardrails**; `L2-reusable-knowledge` renamed to **Patterns & Blueprints**. L2 building blocks: Intent, Tenets & Guardrails, Patterns & Blueprints, Risk & Compliance, Innovation & Foresight — five, each with a real internal relationship, none orphaned.

### D7 — Standing rule: no verbatim TOGAF/Zachman/ArchiMate terminology going forward

**Decision:** Add to `terminology`: before naming any new entity, check it against TOGAF's Content Metamodel, Zachman's cell labels, and ArchiMate's element catalog. A name match is not automatically disqualifying (some words — "Process," "Actor," "Service" — are generic English, not framework-owned), but a *conceptual* match to a classical-EA static-documentation artifact (a catalog, a matrix cell, a reference model, a principle) requires the modern-digital reframe test applied in D3–D5: **does renaming it around what it actually does (automate, enforce, compose, link) change the entity's relationships, or only its label?** If only the label changes, the rename is cosmetic and should be skipped; if relationships follow from the reframe (as they did in D3–D5), it's a real conceptual fix, not a find-and-replace.

## Consequences

- L2 building blocks: 7 → 5.
- Entities removed: Viewpoint, Glossary Term, Taxonomy Node (3 removed).
- Entities added: Concept (1 added, replaces the two merged ones — net entity count -2).
- Entities renamed with new relationships: Principle→Tenet, Standard→Guardrail, Reference Model→Blueprint (all three go from 0 relationships to ≥1).
- New orthogonal_allocator: `semantic-dimension`, alongside `ecf-matrix`, `measurement-dimension`, `ai-automation-governance`.
- Net effect: every entity in L2 now has at least one outbound or inbound relationship. Zero orphans remain in the layer.
- T1 (`dea-metamodel`) regeneration required — entity_id changes for the three renamed entities are breaking for any T2 catalog that already reference the old ids; a migration note with old→new alias mapping is included in the model file for consumers pinned to v0.3.x.
