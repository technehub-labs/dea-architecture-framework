# CR-AR-FMWK-05: Metric Programme Entity Allocation

## 1. Objective

Allocate the twelve Metric entities admitted by CR-MET-001..012 into the
OpenDEAM model, so the viewer renders the Metric capability rather than only
`dea:entity-metric`.

At v0.7.0 the model carries `dea:entity-metric` (`MTR`) and none of the other
twelve. A reader of the published metamodel documentation sees thirteen Metric
entities; the published diagram shows one.

## 2. Why these entities belong to a dimension and not a layer

`dea:entity-metric` is deliberately absent from any layer. Per ADR-0002 D1 the
model replaced a former L6 with a cross-cutting `measurement-dimension`, and
`MTR` was moved out of layer allocation to sit in that overlay:

> No longer allocated to a layer/building_block as of v0.2.0: belongs to
> orthogonal_allocators.measurement-dimension instead (ADR-0002 D1).

The same reasoning applies to all twelve. None of them is an architectural
component; each is an evaluative construct that a layer may be measured
against. They therefore carry `scope_layers` and no `layer` key.

This is a consistency argument, not an extension of the original decision: no
new allocator is introduced and no layer semantics change.

## 3. Entities to allocate

| Entity | Alias | display_name | Catalog repo |
|---|---|---|---|
| `dea:PerformanceMetric` | MTR | Performance Metric | dea-catalog-metrics |
| `dea:Measurement` | MMT | Measurement | null |
| `dea:MeasurementObservation` | MOBS | Measurement Observation | null |
| `dea:IndicatorDesignation` | IDS | Indicator Designation | null |
| `dea:Baseline` | BSL | Baseline | null |
| `dea:PerformanceTarget` | PTG | Performance Target | null |
| `dea:Threshold` | THR | Threshold | null |
| `dea:PerformanceInterpretation` | PIT | Performance Interpretation | null |
| `dea:ReportingPeriod` | RPT | Reporting Period | null |
| `dea:Provenance` | PRV | Provenance | null |
| `dea:AnalyticalResult` | ANR | Analytical Result | null |
| `dea:Correlation` | COR | Correlation | null |
| `dea:CausalHypothesis` | CSH | Causal Hypothesis | null |

`MTR` already exists upstream and is carried forward unchanged. This CR adds
the remaining twelve.

## 4. Identifier convention

`dea-architecture-framework` uses `dea:entity-<kebab-name>` for OpenDEAM
identifiers. The Metric entities follow the same convention:

    dea:entity-measurement
    dea:entity-measurement-observation
    dea:entity-indicator-designation
    dea:entity-baseline
    dea:entity-performance-target
    dea:entity-threshold
    dea:entity-performance-interpretation
    dea:entity-reporting-period
    dea:entity-provenance
    dea:entity-analytical-result
    dea:entity-correlation
    dea:entity-causal-hypothesis

## 5. Alias namespace

The thirteen class_alias values are assigned canonically in `dea-metamodel`
and are unique there with zero collisions, enforced by
`check_alias_uniqueness` in the artifact drift gate:

    MTR  MMT  MOBS  IDS  BSL  PTG  THR  PIT  RPT  PRV  ANR  COR  CSH

Each is at most five characters, satisfying the viewer graph schema.

This CR also corrects one pre-existing collision. `dea:IntegrationInterface` and
`dea:InvestmentInitiative` both carried `II`. The viewer keys nodes on
`class_alias`, so the collision was observable. Resolution: the binding used by
the consumed artefact wins, and `viewer/entity-graph.json` binds `II` to
`dea:entity-investment-initiative`. `dea:IntegrationInterface` becomes `IFI`,
matching the existing `IFC` / `IGC` / `ISC` family convention.

## 6. Consumer-side prerequisite

The viewer generator in `dea-metamodel` resolves a dimension entity's allocator
through `DIMENSION_ALLOCATOR`, because the model declares allocators without
naming which entity backs each. That map must carry all thirteen Metric
aliases before these entries can render. That change is the companion work in
`dea-metamodel` and is a hard prerequisite for this CR to have any visible
effect.

## 7. Relationships

None in this CR. The Metric entities participate in existing canonical
relationships (`applies-metric`, `measures-subject`, `has-evidence`,
`specializes`, and others), and the metamodel-side crosswalk already resolves
viewer labels for those. Relationship allocation is deliberately deferred to a
follow-on CR so that this one stays reviewable and reversible.

## 8. Version impact

This is an **additive** allocation: twelve new entries in
`model/allocation.entities`, no change to any existing entry, no layer
reassignment, no relationship change.

Per the versioning convention in `metamodel-pointer.yaml` comments
("allocation changes go through the root model; structural: ADR + minor bump;
additive: PR + patch bump"), this is a **patch bump**: v0.7.0 to v0.7.1.

## 9. Definition of done

- [ ] Twelve entries added to `model/allocation.entities`, each with
      `entity_id`, `class_alias`, `display_name`, `status`, `description`,
      `scope_layers`, and no `layer` key
- [ ] `dea:entity-metric` unchanged
- [ ] `docs/is-semantic-architecture/opendeam-identifier-map.yaml` gains twelve
      mappings to the canonical `dea-metamodel` identifiers
- [ ] `model-ci.yml` passes
- [ ] `validate-against-model.yml` passes
- [ ] `validate-authorship.yml` passes
- [ ] Version bumped to v0.7.1
- [ ] Companion `dea-metamodel` change to `DIMENSION_ALLOCATOR` merged

## 10. Out of scope

- Relationship allocation between Metric entities and layers (follow-on CR)
- Any change to the `measurement-dimension` allocator itself
- Any change to `dea:entity-metric`
- Any layer or building_block reorganisation

## 11. Cross-references

- `dea-metamodel` change-requests CR-MET-001..012
- `dea-metamodel` docs/metric-capability-map.md
- `dea-metamodel` docs/class-alias-conventions.md
- ADR-0002 D1 (measurement is a dimension, not a layer)
- `dea-metamodel` viewer/entity-graph.json (binding of record for `II`)