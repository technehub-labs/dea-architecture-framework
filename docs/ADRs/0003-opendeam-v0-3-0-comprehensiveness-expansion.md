# ADR-0003: OpenDEAM v0.3.0 — Comprehensiveness Expansion (Ecosystem, Risk, Foresight, People, AI Operations)

**Status:** Accepted
**Supersedes:** opendeam-model.yaml v0.2.0
**Version bump:** MINOR (0.2.0 → 0.3.0) — five new building blocks, one new orthogonal dimension.

## Context

The model was reviewed for gaps against three explicit filters, applied to every candidate before it was allowed in:

1. **Does it already exist under another name?** — if yes, extend an existing entity; don't add a block.
2. **Is it single-layer or genuinely cross-cutting?** — cross-cutting concepts become `orthogonal_allocators`, never building blocks.
3. **Does it have a non-generic one-sentence derivation from the axiom** ("persists by exchanging value with its environment")? — if the derivation could equally justify three other concepts, it's too coarse.

Everything below passed all three. Two candidates that were considered and explicitly rejected are recorded at the end, so future contributors don't re-propose them without re-litigating the reason.

## Decisions

### D1 — Add `L1-ecosystem-platforms`

**Gap:** L1 modeled bilateral exchange (actor ↔ actor via value exchange, agreement) but not the enterprise acting as a platform host for many third parties at once — marketplaces, partner API programs, developer portals. This is materially different from a single Value Exchange.

**Derivation:** `"environment"` — a platform is a standing structure the enterprise erects *in* its environment for repeated multilateral exchange, distinct from any one exchange.

**New entity:** `Ecosystem Platform (EP)` — layer L1, building block `L1-ecosystem-platforms`.

**Why not a TOGAF/ArchiMate repeat:** neither framework has a first-class object for multi-sided/platform dynamics; both model exchange only bilaterally (actor–actor, application–application).

### D2 — Add `L2-risk-compliance`

**Gap:** No architectural object for risk, controls, or regulatory obligation. Previously implicit in "governance" relationships with no entity to point to.

**Derivation:** `"persists"` — an enterprise that does not manage existential and regulatory risk does not persist; risk management is a condition of persistence, not an activity layered on top of it.

**New entities:** `Risk (RSK)`, `Control (CTL)`, `Regulation (REG)` — layer L2, building block `L2-risk-compliance`.

**Why not a repeat:** TOGAF handles risk as a cross-phase *activity* in the ADM (assessed at each phase gate), not as first-class architectural objects with their own relationships to capabilities and systems. Here risk is a thing you can point at, not a checklist step.

### D3 — Add `L2-innovation-foresight`

**Gap:** No object for sensing environmental change before it becomes a forced adaptation — weak signals, experiments, emerging-tech tracking.

**Derivation:** `"persists by exchanging value with its environment"` — persistence requires sensing environmental change in advance, not only responding to realized change.

**New entities:** `Signal (SIG)`, `Experiment (EXP)`, `Technology Radar Entry (TRE)` — layer L2, building block `L2-innovation-foresight`.

**Why not a repeat:** neither framework models a formal sense→experiment→adopt pipeline. This is also the correct, disciplined home for "emerging AI capability" tracking — a radar entry, evaluated via an experiment, before it becomes a governed L5 Technology. It avoids the common anti-pattern of bolting "AI trends" onto the Technology entity directly.

### D4 — Add `L3-people-skills-culture`

**Gap:** L3-work-organization models organizational *structure* (Organizational Unit, Actor, Business Function) but not the capability *of the people themselves*, nor the deliberate change effort required to shift it. This is the single most common cause of digital-transformation failure and neither framework models it at all.

**Derivation:** `"bounded entity"` internally organizes — but the entity is bounded by what its people can actually do and are willing to change to, not only by its formal structure.

**New entities:** `Skill (SKL)`, `Role (ROL)`, `Change Initiative (CHI)` — layer L3, building block `L3-people-skills-culture`.

**Why not a repeat:** ArchiMate has no people-capability layer; TOGAF's Business Architecture touches organization structure but not skill/role/change-readiness as architectural objects with relationships to capability gaps.

### D5 — Add `L4-model-operations`

**Gap:** `AI/ML Model` (L4-intelligence) models the model as a decision artifact, but not its operational lifecycle — deployment, monitoring, drift, feedback-driven retraining. This is a materially different concern from the model's existence, the same way L5 already separates *Systems* from *Infrastructure*.

**Derivation:** `"persists"` — a model that is deployed but not operated (monitored, retrained, retired) does not persist as a trustworthy decision component; operations is what makes intelligence durable rather than a one-time artifact.

**New entities:** `Model Deployment (MDP)`, `Model Feedback Signal (MFS)` — layer L4, building block `L4-model-operations`.

**Why not an "AI layer":** deliberately not modeled as a new top-level layer. AI/AI-driven concepts are distributed across five existing extension points (Actor subtype, AI/ML Model entity, this new operations block, the new AI-governance dimension below, and the existing `AIM enhances/automates SF` relationship pattern) rather than centralized into one silo that would duplicate concerns already owned by L2, L3, and L5.

### D6 — Add `ai-automation-governance` orthogonal dimension

**Gap:** No standard way to say "this AI-driven thing is subject to this policy" without inventing an AI-specific parallel governance structure.

**Decision:** New `orthogonal_allocators` entry. Any entity that is AI-driven (`Actor` of AI-agent subtype, `AI/ML Model`, any `System Function` with an `enhances/automates` relationship from an AIM) may carry `governed_by: [Risk/Control/Regulation ids]`, reusing D2's entities rather than creating AI-specific ones.

**Explicit rejection — a separate "Responsible AI" layer:** rejected. Responsible AI is governance applied to AI-driven entities, not a different kind of architecture object. Modeling it as its own layer would duplicate `L2-risk-compliance` under an AI-flavored name — precisely the anti-pattern this ADR's filter exists to catch.

## Explicitly rejected candidates (record for future contributors)

- **Sustainability/Environmental Impact as a layer or building block** — deferred, not rejected outright. Recommended as a future `orthogonal_allocator` (`sustainability_impact` tag on Infrastructure Component, Technology, Value Stream) *only when a real consuming team needs it* — per the model's own additive-only-when-needed discipline. Adding it speculatively now would violate filter #3 (no concrete, non-generic derivation yet, because no org has asked to allocate against it).
- **"AI Layer" (L6, replacing the old measurement L6 slot)** — rejected. See D5's rationale: AI is a property distributed across existing layers/dimensions, not a domain requiring its own layer. Re-centralizing it into one layer would re-create the exact asymmetry ADR-0002 D1 removed.
- **ADM-style "Governance Gate" or "Phase" building block** — rejected. TOGAF's ADM is a process; OpenDEAM is a state model. A consuming org can map ADM phases onto OpenDEAM entities externally; OpenDEAM does not need to model the process itself without collapsing back into TOGAF.

## Consequences

- Layers unchanged (still 5, per ADR-0002): L1–L5 each gain one building block, except L2 (gains two) and L5 (unchanged).
- New entities: EP, RSK, CTL, REG, SIG, EXP, TRE, SKL, ROL, CHI, MDP, MFS — 12 total.
- New orthogonal_allocator: `ai-automation-governance`, alongside existing `ecf-matrix` and `measurement-dimension`.
- New relationships wiring the above into existing entities (Risk→Capability, Signal→Experiment→Investment Initiative, Skill→Role→Actor, Model Deployment→AI/ML Model→System Function).
- T1 (`dea-metamodel`) regeneration required — additive at the schema level (new optional `governed_by` field), non-breaking for existing consumers pinned to v0.2.x, so no forced migration — but new entity/building-block IDs are new, hence still a minor bump per the model's own rule for new building blocks.
