# ADR-0007: OpenDEAM v0.8.0 — Core Anchor Promotion (CR-004 Core/Profile split)

**Status:** Proposed (this PR)
**Supersedes:** opendeam-model.yaml v0.7.7 (tagged; CR-AR-FMWK-06..11)
**Version bump:** MINOR (0.7.7 → 0.8.0) — new abstract kernel entries + new
concrete entity entries. No new layers, no new building blocks, no new
dimensions, no layer re-allocations of existing entities.

**Author:** Emmanuel A. Otchere
**Date:** 2026-10-27

## Context

`dea-metamodel` CR-004 (merged 2026-08-16) established the **OpenDEA Core
Ontology**: 18 core anchors + 10 profiles, with the rule that profiles may
extend/specialize Core but must not redefine it (O002), and every profile
`depends_on` roots at `dea:core` with no cycles (O004). The root model
consumed CR-001..003 downstream at v0.6.0 but deliberately did not adopt
the Core anchors — the README has carried the earmark since: "the CR-004
Core/Profile split introduces 10 new core anchors that are not yet in
this root model — promoting them upstream is the candidate content of the
next minor release."

The six intervening patch releases (v0.7.2–v0.7.7, CR-AR-FMWK-06..11)
completed the lifecycle truth-up and the Metric programme. The model is
at a clean consolidation point (tag `v0.7.7`), which makes this the right
moment for the ADR-gated minor release.

The 10 new CR-004 anchors (from
`dea-metamodel/metamodel/core/core-entities.yaml`, definitions
authoritative there):

| Anchor | Kind | dea-metamodel id | OpenDEAM entity_id |
|---|---|---|---|
| Architecture Element | abstract | `dea:ArchitectureElement` | `dea:entity-architecture-element` |
| Behavior | abstract | `dea:Behavior` | `dea:entity-behavior` |
| Service | abstract | `dea:Service` | `dea:entity-service` |
| Information | abstract | `dea:Information` | `dea:entity-information` |
| Organization | abstract | `dea:Organization` | `dea:entity-organization` |
| Decision | concrete | `dea:Decision` | `dea:entity-decision` |
| Outcome | concrete | `dea:Outcome` | `dea:entity-outcome` |
| Requirement | concrete | `dea:Requirement` | `dea:entity-requirement` |
| Constraint | concrete | `dea:Constraint` | `dea:entity-constraint` |
| Change | concrete | `dea:Change` | `dea:entity-change` |

**Collision check:** none of the ten display names or candidate aliases
collide with any existing OpenDEAM entity (verified against
v0.7.7: 70 entities). Notably `dea:Service` (Core, abstract) is distinct
from OpenDEAM's `dea:entity-business-service` (BS, L3 concrete) — the
CR-AR-FMWK-10 §2 ruling already established that mapping one onto the
other would conflate distinct concepts; this ADR keeps them separate.

## Decisions

### D1 — The five abstract anchors enter as cross-layer kernels

**Decision:** ArchitectureElement, Behavior, Service, Information, and
Organization enter the root model as **abstract kernel entries**, the
shape precedent set by `dea:entity-process` (PRC, ADR-0006) and
`dea:entity-resource` (RES, ADR-0005 D3):

- `abstract: true`
- `status: planned` (admitted by CR-004, allocated here, wired below —
  the same programme-commitment evidence class as CR-AR-FMWK-11, applied
  to kernels)
- `layer` on the kernel's own primary home (validator check #7 requires
  abstract entities to declare `realized_in_layers`; each kernel
  declares the full set of layers its specializations occupy)
- `catalog_repo: null` — kernels anchor categories; their T2 catalogs
  live under the specializations
- `completeness_contract` naming the specialization contract (per
  ADR-0005/0006 kernel discipline)

Kernel homes and realized layers:

| Kernel | Alias | Layer (primary) | Building block | realized_in_layers | Existing specializations re-parented |
|---|---|---|---|---|---|
| Architecture Element | AE | L2 | L2-reusable-knowledge | L2, L3, L4, L5 | none yet (structural root; future ADR may re-parent) |
| Behavior | BEH | L3 | L3-value-delivery | L3, L4, L5 | BP (specializes PRC; PRC specializes BEH — see D3) |
| Service | SRV | L3 | L3-service-offerings | L3, L5 | BS; ISS (via specializes) |
| Information | INF | L4 | L4-data-foundation | L3, L4 | BO, DE, IA, KA, DP |
| Organization | ORG | L3 | L3-work-organization | L1, L3 | OU (via specializes); EA remains L1 concrete (an organization can act as an actor; structure ≠ agency) |

**Why this shape and not layer re-allocation:** the CR-004 anchors are
kinds, not components — a Behavior is not a part of the enterprise, it
is a category several L3/L4/L5 entities realize. OpenDEAM's MECE rule
(each entity exactly one layer + building block) applies to components;
kernels are the sanctioned exception (ADR-0005 D2/D3, ADR-0006 D1). No
existing entity changes layer.

**Class-alias choices** (≤5 chars, no collisions, following the
metamodel's alias conventions where visible): AE, BEH, SRV, INF, ORG;
concretes DEC, OUT, REQ, CST, CHG.

### D2 — The five concrete anchors enter as layer-allocated entities

**Decision:** Decision, Outcome, Requirement, Constraint, and Change
enter as normal layer-allocated entities with `catalog_repo: null`
(create-on-content; no repos exist yet — verified) and `status:
planned` (admitted by CR-004 with schemas/tables/pydantic/TTL already
delivered downstream; allocated here).

| Entity | Alias | Layer | Building block | Rationale (axiom clause) |
|---|---|---|---|---|
| Decision | DEC | L2 | L2-intent | A determination selecting a course of action is intent expressed; foundation for agentic architecture (CR-7) |
| Outcome | OUT | L2 | L2-intent | "persists" — the resulting state/value strategy targets; anchor for strategy, value, DMM, measurement |
| Requirement | REQ | L2 | L2-rules-guidance | A stated need that governs — rules & guidance, sibling of Tenet/Guardrail (distinct: a Guardrail enforces; a Requirement must be satisfied) |
| Constraint | CST | L2 | L2-rules-guidance | Limits the solution space — rules & guidance (distinct from REQ per CR-004 §16) |
| Change | CHG | L3 | L3-people-skills-culture | A deliberate modification to capabilities/behavior/organization — the operating-model change effort; sibling of CHI (CHI targets people/culture specifically; CHG is the general modification) |

All five definitions are quoted from
`dea-metamodel/metamodel/core/core-entities.yaml` (authoritative).

**Naming-philosophy check (ADR-0004 D7):** each name was checked against
TOGAF/Zachman/ArchiMate. "Requirement" and "Constraint" are conceptual
matches to classical-EA documentation artifacts, but they pass the
reframe test: they carry their own lifecycle and relationship pattern
(REQ is satisfied-by; CST constrains; neither is a documentation shelf
item). No renames.

### D3 — Relationship wiring: specialization edges only, deferred surface

**Decision:** this ADR adds the **structural** edges and defers the
full relationship surface to the implementation CR:

- 5 kernel self-edges are NOT added; kernels connect through their
  specializations.
- PRC (Process kernel) gains `specializes: BEH` — the Process kernel is
  the first Behavior specialization, exactly as CR-004 §9 states.
- BS gains `specializes: SRV`; ISS's existing specialization chain
  reaches SRV through the Core `dea:Service`.
- BO, DE, IA, KA, DP gain `specializes: INF` (all are Information
  specializations per CR-004 §12).
- OU gains `specializes: ORG`.
- Realization edges for the kernel set (kernel realized-in-layer
  markers) follow the ADR-0006 pattern where applicable.

The full Core relationship grammar (CR-004 §19) and the integration
surface (informs-decision now has a DEC target, constrains has CST,
etc.) are **implementation-CR scope**, mirroring how ADR-0006 deferred
its CR-AR-FMWK-01 execution.

**`specializes` chains:** validator check #7 permits `specializes` to
target abstract entities; BEH/SRV/INF/ORG are abstract, so the re-
parenting edges validate. PRC's `specializes: BEH` makes the chain
BEH ← PRC ← BP; the chain depth is unchanged from the consumer's view
(they resolve against BP).

### D4 — Consumer impact and validator

**Decision:** no validator change in this ADR. The abstract-kernel
branch (ADR-0006 D2) already handles kernel entries in
`validate_consumer.py`; the five concrete anchors take the standard
layer-allocated branch. Consumer pointers are unaffected: no existing
entity changes `entity_id`, `class_alias`, `layer`, or
`building_block`. The new aliases (AE, BEH, SRV, INF, ORG, DEC, OUT,
REQ, CST, CHG) are additive.

**Identifier-map note:** `docs/is-semantic-architecture/opendeam-identifier-map.yaml`
gains ten open_deam→metamodel mappings (identity mappings: the
OpenDEAM `dea:entity-*` ids map to the Core `dea:*` ids) in the
implementation CR.

### D5 — Version and rollout

**Decision:** v0.7.7 → **v0.8.0** (minor: new abstract kernels + new
entities, the change-control table's ADR + minor case). Rollout
mirrors prior minors: T0 (this ADR + implementation CR) → T1
(`dea-metamodel` sync, no action expected — it is the authority) → T3
viewers via the standard fan-out. T2: no new catalogs (create-on-content).
The roadmap gains the ten anchors in its executed-phases table on
landing.

## Consequences

- The root model goes from 70 → **80 entities** (5 abstract kernels +
  5 concretes added; no removals), 113 → ~125 relationships
  (implementation CR).
- The Core/Profile split is now reflected upstream: consumers can key
  on Core anchors via the root model, closing the two-year-old earmark.
- `dea:Service` (SRV, abstract) and `dea:entity-business-service` (BS)
  coexist with distinct semantics; CR-AR-FMWK-10 §2's anti-conflation
  ruling is preserved.
- Future CRs may re-parent additional existing entities onto the
  kernels (e.g., Activity-type entities onto BEH); each is its own
  patch-class CR.
- The dimension-lifecycle convention (CR-AR-FMWK-11 §1) applies
  unchanged; the new kernels use the kernel discipline (ADR-0005/0006)
  instead.

## Alternatives considered

1. **Promote concretes only** — smaller ripple, but leaves the Core
   grammar half-represented and forces a second minor release for the
   abstracts; rejected for double release overhead.
2. **Wait for more anchors** — no; the consolidation point is now and
   the earmark is the oldest open one.
3. **Re-allocate existing entities to match Core** — violates MECE and
   the no-re-allocation-without-ADR rule; kernels are the sanctioned
   alternative.

## Implementation CR (follow-on, ADR-0006 pattern)

CR-AR-FMWK-12 will execute: ten entity entries, the D3 specialization
edges, identifier-map additions, README/CHANGELOG/roadmap sync, patch
steps within the minor (0.7.7 → 0.8.0 in one step per the change-control
table).
