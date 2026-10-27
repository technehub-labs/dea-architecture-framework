# CR-AR-FMWK-12: Core Anchor Promotion (ADR-0007 implementation)

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-12 |
| **Title** | Core Anchor Promotion: ADR-0007 implementation (v0.8.0) |
| **Status** | Proposed (this PR) |
| **Type** | Entity allocation + specialization re-parenting (ADR-gated minor release execution) |
| **Scope** | `technehub-labs/dea-architecture-framework` (root model) |
| **Authority** | ADR-0007 (accepted, PR #29) — this CR executes it |
| **Predecessor** | ADR-0006 → CR-AR-FMWK-01 (the ADR-then-CR pattern this follows); `dea-metamodel` CR-004 (the anchor authority) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-27 |

## 1. Change Request

Per ADR-0007:

1. **Add 10 entity entries** to `model/allocation.entities` — the
   five abstract kernels (D1) and five concrete anchors (D2).
2. **Add `specializes` to 8 existing entities** (D3): PRC→BEH,
   BS→SRV, BO/DE/IA/KA/DP→INF, OU→ORG.
3. **Add 5 specialization relationship edges** mirroring the same
   re-parenting in the graph (following the ADR-0006 pattern of
   `specializes` edges in `relationships:`).
4. Add 10 identity mappings to
   `docs/is-semantic-architecture/opendeam-identifier-map.yaml`.
5. README/CHANGELOG/roadmap sync; version → 0.8.0.

## 2. The ten new entries (ADR-0007 D1/D2)

### Abstract kernels (D1 shape: abstract, realized_in_layers, catalog_repo: null, completeness_contract)

| entity_id | alias | layer | building_block | realized_in_layers |
|---|---|---|---|---|
| `dea:entity-architecture-element` | AE | L2 | L2-reusable-knowledge | L2, L3, L4, L5 |
| `dea:entity-behavior` | BEH | L3 | L3-value-delivery | L3, L4, L5 |
| `dea:entity-service` | SRV | L3 | L3-service-offerings | L3, L5 |
| `dea:entity-information` | INF | L4 | L4-data-foundation | L3, L4 |
| `dea:entity-organization` | ORG | L3 | L3-work-organization | L1, L3 |

All five: `status: planned`, `catalog_repo: null`, `abstract: true`,
definitions quoted from `dea-metamodel/metamodel/core/core-entities.yaml`.

### Concrete anchors (D2 shape: normal layer allocation)

| entity_id | alias | layer | building_block |
|---|---|---|---|
| `dea:entity-decision` | DEC | L2 | L2-intent |
| `dea:entity-outcome` | OUT | L2 | L2-intent |
| `dea:entity-requirement` | REQ | L2 | L2-rules-guidance |
| `dea:entity-constraint` | CST | L2 | L2-rules-guidance |
| `dea:entity-change` | CHG | L3 | L3-people-skills-culture |

All five: `status: planned`, `catalog_repo: null` (create-on-content;
no repos exist — verified).

## 3. Specialization re-parenting (D3)

Eight existing entities gain one `specializes` field each. No other
field of these entries changes; no layer changes.

| Entity | gains `specializes` | validator rule 7 |
|---|---|---|
| PRC (Process kernel, L3) | BEH | BEH abstract ✓, realized L3..L5 ⊇ L3 ✓ |
| BS (Business Service, L3) | SRV | SRV abstract ✓, realized L3/L5 ∋ L3 ✓ |
| BO (Business Object, L3) | INF | INF abstract ✓, realized L3/L4 ∋ L3 ✓ |
| DE (Data Entity, L4) | INF | realized ∋ L4 ✓ |
| IA (Information Asset, L4) | INF | realized ∋ L4 ✓ |
| KA (Knowledge Asset, L4) | INF | realized ∋ L4 ✓ |
| DP (Data Product, L4) | INF | realized ∋ L4 ✓ |
| OU (Organizational Unit, L3) | ORG | ORG abstract ✓, realized L1/L3 ∋ L3 ✓ |

Plus five `specializes` edges in `relationships:` (PRC→BEH, BS→SRV,
BO→INF, OU→ORG; DE/IA/KA/DP share the INF edge by kind — one edge per
parent as the graph renders parent-of relationships), following the
existing `realization`-typed specialization edges.

**ISS** (Information System Service, L5) is deliberately NOT
re-parented in this CR: its specialization lives in the metamodel
(Core `dea:Service` ← ISS via the identifier map), and OpenDEAM's ISS
already carries a `supersedes` chain; re-parenting it would touch a
third field on one entry — deferred to keep this CR's diff exactly the
ADR-0007 D3 list. (ADR-0007 D1 lists ISS under SRV "via specializes"
as a future step.)

## 4. Identifier map additions

Ten identity mappings
(`dea:entity-*` → `dea:ArchitectureElement` etc., disposition D-1,
cr CR-004), appended to
`docs/is-semantic-architecture/opendeam-identifier-map.yaml`.

## 5. Version impact

ADR-gated **minor**: v0.7.7 → **v0.8.0** (change-control table: new
entities + new abstract kernels). Both `VERSION` and `model.version`.

## 6. What does NOT change

- No existing entity's `entity_id`, `class_alias`, `layer`,
  `building_block`, or `status`.
- All 113 existing relationships, except the 5 appended
  specialization edges.
- No new layers, building blocks, dimensions, or rel_type values.
- Validator and schema: no change (rule 7 handles the new shapes;
  the abstract-kernel consumer branch handles the kernels).

## 7. Definition of done

- [ ] 10 new entries in `model/allocation.entities` (80 total)
- [ ] 8 `specializes` fields added to existing entries
- [ ] 5 specialization edges appended (118 relationships total)
- [ ] 10 identifier-map mappings added
- [ ] `VERSION` and `model.version` → `0.8.0`
- [ ] README badge/count sync; CHANGELOG `[v0.8.0]` section; roadmap
      executed-phase entry
- [ ] `validate_model.py` PASS; `check_authorship.py` PASS;
      `model-ci.yml` green
- [ ] This CR registered in `change-requests/README.md`

## 8. Cross-references

- ADR-0007 (`docs/ADRs/0007-opendeam-v0.8.0-core-anchor-promotion.md`) — the authority for this CR
- `dea-metamodel` CR-004 + `metamodel/core/core-entities.yaml` (definitions)
- ADR-0006 → CR-AR-FMWK-01 (the ADR-then-CR pattern)
- CR-AR-FMWK-10 §2 (the SRV-vs-BS anti-conflation ruling this preserves)
