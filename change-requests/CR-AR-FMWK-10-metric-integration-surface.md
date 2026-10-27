# CR-AR-FMWK-10: Metric `measured_by` Integration Surface (root-model slice)

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-10 |
| **Title** | Metric `measured_by` Integration Surface: wiring the metamodel's 16-type measured/assessed surface onto OpenDEAM entities |
| **Status** | Proposed (this PR) |
| **Type** | Entity-entry extension (additive `measured_by` fields) + relationship edges |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Predecessor** | CR-AR-FMWK-09 (metric relationships, PR #24): §4 deferred the 16-type `measured-by`/`assessed-by` integration surface to "a follow-on CR touching entity entries" — this is that follow-on |
| **Authority** | `dea-metamodel` docs/metric-capability-map.md §5 — the canonical integration surface; this CR is the root-model translation, not a re-authoring |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. Change Request

Two additive changes to `model/opendeam-model.yaml`:

1. Add `measured_by: [MTR]` to **9 entity entries** that participate
   in the metamodel's measurement/assessment surface but carry no
   OpenDEAM-side wire today.
2. Add **9 relationship edges** (`<entity> → MTR`, label
   `measured by` / `evaluated by`, rel_type `governance`), mirroring
   the existing `SO/CAP/SF → MTR` edge pattern.

No existing entry, field, or edge changes. No rel_type vocabulary
change (governance already exists).

## 2. Translation

The metamodel distinguishes `measured-by` (16 source types) from
`assessed-by` (5 source types). OpenDEAM has a single `measured_by`
field and a single edge label family (`measured by` / `evaluated
by`), so both metamodel relations land on the same OpenDEAM wire.
The distinction is preserved at the metamodel layer where it is
canonical; OpenDEAM records participation in the measurement
surface, which is the root-model-appropriate granularity.

Metamodel type → OpenDEAM entity resolution:

| Metamodel type | OpenDEAM | Wire today | This CR |
|---|---|---|---|
| BusinessProcess | BP | `measured_by` + edge | already wired (v0.5.0-era) |
| BusinessCapability | CAP | `measured_by` + edge | already wired |
| InformationSystemFunction | ISF | `measured_by` (no edge) | edge added (CR-AR-FMWK-09 style) |
| SystemFunction | SF | `measured_by` + edge | already wired |
| DataEntity | DE | none | **field + edge** |
| OrganizationalUnit | OU | none | **field + edge** |
| ValueStream | VS | none | **field + edge** |
| ApplicationComponent | APC | none | **field + edge** |
| AIMLModel | AIM | none | **field + edge** |
| SolutionComponent | SC | none | **field + edge** |
| TechnologyRadarEntry | TRE | none | **field + edge** |
| Risk | RSK | none | **field + edge** |
| Control | CTL | none | **field + edge** |
| AssessmentDimension | — | — | **out of scope**: no OpenDEAM entity (Core metamodel entity; OpenDEAM does not allocate Core per CR-AR-FMWK-04 D-3) |
| MaturityModel | — | — | **out of scope**: no OpenDEAM entity (Core) |
| Policy | — | — | **out of scope**: no OpenDEAM entity (Core) |
| Service | — | — | **out of scope**: `dea:Service` is Core; OpenDEAM's `dea:entity-business-service` (BS) is a distinct L3 concept — mapping Core Service onto BS would be a semantic conflation, not a translation |

The `ISF → MTR` edge is added for consistency: ISF already declares
`measured_by: [MTR]` but has no edge, unlike its peers BP/CAP/SF.

## 3. The 9 entity-entry additions

Each gains exactly one field:

```yaml
    measured_by:
    - MTR
```

| Entity | Alias | Layer | Metamodel relation |
|---|---|---|---|
| `dea:entity-risk` | RSK | L2 | measured-by |
| `dea:entity-control` | CTL | L2 | measured-by |
| `dea:entity-technology-radar-entry` | TRE | L2 | assessed-by |
| `dea:entity-organizational-unit` | OU | L3 | measured-by |
| `dea:entity-value-stream` | VS | L3 | measured-by |
| `dea:entity-solution-component` | SC | L3 | assessed-by |
| `dea:entity-data-entity` | DE | L4 | measured-by |
| `dea:entity-ai-ml-model` | AIM | L4 | assessed-by |
| `dea:entity-application-component` | APC | L5 | measured-by |

All 9 layers are within `MTR`'s `scope_layers` [L1..L5], so
validator rule 6 (measured layer within metric scope) passes for
every addition.

## 4. The 10 relationship edges

Mirroring the existing pattern (label `measured by` for
measured-by sources, `evaluated by` for assessed-by sources;
rel_type `governance`):

| # | from | to | label | rel_type | cardinality |
|---|---|---|---|---|---|
| 1 | RSK | MTR | measured by | governance | 0..N:0..N |
| 2 | CTL | MTR | measured by | governance | 0..N:0..N |
| 3 | TRE | MTR | evaluated by | governance | 0..N:0..N |
| 4 | OU | MTR | measured by | governance | 0..N:0..N |
| 5 | VS | MTR | measured by | governance | 0..N:0..N |
| 6 | SC | MTR | evaluated by | governance | 0..N:0..N |
| 7 | DE | MTR | measured by | governance | 0..N:0..N |
| 8 | AIM | MTR | evaluated by | governance | 0..N:0..N |
| 9 | APC | MTR | measured by | governance | 0..N:0..N |
| 10 | ISF | MTR | evaluated by | governance | 1:0..N |

Total: 103 → **113 relationships**.

ISF edge 10 exists because ISF declares the field without the edge;
its peers (BP, CAP, SF) each have both. Cardinality `1:0..N` matches
the existing SO/CAP/SF → MTR edges.

## 5. What does NOT change

- The 4 pre-existing `measured_by` declarations (BP, CAP, SF, ISF) —
  values unchanged.
- The 3 pre-existing MTR edges (SO, CAP, SF) — unchanged.
- All 12 metric dimension entities and the 24 CR-AR-FMWK-09 edges —
  unchanged.
- MTR's `scope_layers` — unchanged (already L1..L5).
- Entity statuses (R SK, CTL, TRE are `planned` from CR-AR-FMWK-08;
  this CR does not touch status).
- No rel_type vocabulary change; no schema change (the
  `measured_by` field is already schema-declared).

## 6. Version impact

**Additive**: 9 new fields on existing entries + 10 new edges, zero
modifications to existing content. Per the versioning convention:
**PR + patch bump**: v0.7.5 → v0.7.6. No ADR, no minor bump.

## 7. Consumer-side prerequisite

None new. `MTR` already renders via `DIMENSION_ALLOCATOR`
(CR-AR-FMWK-05 §6, dea-metamodel PR #196 merged); the 9 entities all
render today. The `measured_by` field and the governance edges are
consumed by the standard sync chain (fan-out → metamodel receiver →
viewers).

## 8. Definition of done

- [ ] `measured_by: [MTR]` added to 9 entity entries in
      `model/opendeam-model.yaml`
- [ ] 10 edges appended to `relationships:` (103 → 113)
- [ ] Zero pre-existing entries, fields, or edges modified
      (verified programmatically)
- [ ] `VERSION` → `0.7.6`
- [ ] `model.version` → `0.7.6`
- [ ] `scripts/validate_model.py` PASS (rule 6 exercised by all 9)
- [ ] `scripts/check_authorship.py` PASS (AUT-001/002/003 = 0)
- [ ] `model-ci.yml` green
- [ ] This CR registered in `change-requests/README.md`

## 9. Out of scope

- AssessmentDimension, MaturityModel, Policy, Service (Core
  metamodel entities; OpenDEAM does not allocate Core —
  CR-AR-FMWK-04 D-3. Mapping Core Service onto BS would conflate two
  distinct concepts.)
- `measured_by` for any other entity (the metamodel's 16-type list
  is the complete canonical surface; anything beyond it is
  speculative)
- Metric dimension-entity lifecycle semantics (still deferred,
  CR-AR-FMWK-08 §8)
- The `constrains` extension (Threshold→PerformanceMetric edge
  already delivered in CR-AR-FMWK-09 edge 20)
- Status changes for any entity

## 10. Cross-references

- `dea-metamodel` docs/metric-capability-map.md §5 (canonical integration surface)
- CR-AR-FMWK-09 (`change-requests/CR-AR-FMWK-09-metric-relationships.md`, PR #24) — predecessor; §4 deferred this surface
- CR-AR-FMWK-05 (entity allocation), CR-AR-FMWK-08 (RSK/CTL/TRE status evidence)
- Validator rule 6 (`scripts/validate_model.py`; measured layer within metric `scope_layers`)
- ADR-0002 D1 (measurement dimension), ADR-0003 D6 (`governed_by` precedent for cross-cutting fields)
