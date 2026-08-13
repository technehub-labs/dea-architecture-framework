# OpenDEAM v0.1.0 — Allocation Rationale

How the 6-layer model was derived and where every entity landed, with
provenance from the two predecessor models.

## Layer derivation

Layers are derived from the enterprise axiom (MECE by construction):

> **"An enterprise is any bounded entity that persists by exchanging value with its environment."**

| Axiom clause | Layer |
|---|---|
| *"with its environment"* | **L1 Ecosystem & Value Network** (External) — the exchange surface |
| *"persists"* (intent) | **L2 Strategic & Governance** (Intent & Rules) |
| *"bounded entity"* | **L3 Business Operating Model** (Internal) — how work is organised |
| *"exchanging value"* (digital plane) | **L4 Digital & Intelligence** (Data & Brain) |
| *"persists"* (execution plane) | **L5 Technology & Execution** (Systems & Infra) |
| persistence over time requires feedback | **Measurement Dimension** (orthogonal, cross-cutting — demoted from L6 by ADR-0002 D1) |

L4/L5 also reflect the conventional digital/technology split (accepted
convention, documented tie-breakers) — the axiom anchors the boundary at
"representation" (L4) vs "substrate" (L5).

## Predecessor models

| Source | Model | Fate |
|---|---|---|
| `dea-metamodel/viewer/entity-graph.json` v2.0.0-alpha | 5 layers, 33 entities | Superseded as authority; all 33 entities reallocated here (see `prior_layer_v2` per entity) |
| `dea-metaframework/metamodel/` v3.0 | 6 layers, 23 entities | Layer skeleton + external entities (EA, VE, CA) and BF adopted; narrative role retained, source-of-truth claim relinquished (ADR-0001 §3) |

## Notable re-allocations (v2 5-layer → OpenDEAM 6-layer)

| Entity | v2 | OpenDEAM | Why |
|---|---|---|---|
| Journey Touchpoint (JT) | L2 | **L1** | Boundary crossing point — lives on the external surface (v3 ruling) |
| Stakeholder (SH) | L1 | **L1** | Definitionally external/affected party — confirmed on the external layer |
| Business Process (BP) | L1 | **L3** | Processes are internal work organisation, not strategic intent |
| Actor (AC) | L1 | **L3** | Internal performer — operating model |
| Business Service (BS) | L2 | **L3** | Offering of the operating model |
| Principle / Standard / Pattern / Reference Model / Glossary / Taxonomy / Viewpoint | L1/L2 | **L2** | All are intent, rules, or governed knowledge |
| Data Entity / Information Class | L4 | **L4** | Data plane confirmed under Digital & Intelligence |
| Performance Metric (MTR) | L5 | **Measurement Dimension** (no home layer) | Measurement is a cross-cutting dimension, not a layer (ADR-0002 D1) |
| *(new)* Ecosystem Actor, Value Exchange, Collaboration Agreement, Business Function | — | L1, L1, L1, L3 | Required by the model; status `planned`, catalog repos TBD. CA initially placed L2 (v0.1.0), moved to L1 by ADR-0002 D2 |

## Boundary rules (MECE discipline)

- **Ecosystem Actor vs Stakeholder.** An Ecosystem Actor *transacts* — it is a
  party to a Value Exchange. A Stakeholder is any engaged or affected party,
  transacting or not. Every EA is implicitly a stakeholder; the SH catalog is
  the register of affected parties, EA the register of transacting parties.
- **Business Function vs Business Capability.** A capability is *what the
  enterprise can do*; a function is *how capabilities are grouped for
  ownership*. CAP → BF "grouped by", BF → OU "owned by".
- **Solution Component (L3) vs Application/Infrastructure/Integration
  Component (L5).** SC is the solution-level abstraction owned by the
  operating model; APC/IFC/IGC are its concrete realisations on the
  execution substrate.
- **Layer vs Tier.** "Layer" = L1–L5 architecture layer (this model; L6 was demoted to the Measurement Dimension by ADR-0002 D1).
  "Tier" = T0–T3 repository-stack position. Catalog READMEs must not use
  "Layer" for stack position.

## Relationship deltas vs v2 (30 → 37)

- Removed: `CAP → OU "owned by"` (superseded by the `CAP → BF → OU` chain).
- Added (from dea-metaframework v3): `EA → CA`, `CA → VE`, `EA → SO`,
  `VE → JT`, `VE → BO`, `EA → DI`, `CAP → BF`, `BF → OU`.
