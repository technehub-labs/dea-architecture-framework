# OpenDEAM Program Roadmap

The single program-level plan for the OpenDEAM rollout across the org.
Phase detail lives in the ADRs and PR history; this file tracks **what is
done, what is live, and what is earmarked for future action**.

## Executed phases (ADR-0004 rollout, Aug 14 2026)

| Phase | Scope | Evidence |
|---|---|---|
| 0 | T0: ADR-0004 accepted, model v0.4.0 **verbatim as authored** (47 entities, 25 BBs, 63 rels, +semantic-dimension; L2 7→5 BBs; VP removed; GT+TXN→CON; PR→TNT, STD→GRD, RM→BLU); schema `enforcement` enum + validator check 6c (`defined_by`/`parent_concept` integrity, 6 negative controls verified) | PR #5, tag `v0.4.0` |
| 1 | T1 dea-metamodel: generator dimension-allocator map + field passthrough fix; schemas renamed/deleted/added; pydantic/TS/TTL/sqlite regen; graph + SVG regenerated | PR #69 |
| 2 | T3 viewers: Pages graph v0.4.0 (47 ent / 63 rels / 2 dims) verified live; dea-web-viewer per-entity dimension labels fix + deploy, bundle verified live | PR #15, live URLs |
| 3 | T2: repos renamed (principles→tenets, standards→guardrails, reference-models→blueprints, glossary→concepts — history preserved via GitHub rename); taxonomy archived (merged into concepts); pointers regenerated + pinned `@v0.4.0` — 4/4 caller CI green | 4× PR #2 |

Caller pin census after this rollout: 24 repos `@v0.2.1`, 11 `@v0.3.0`, 4 `@v0.4.0`.

## Executed phases (ADR-0003 rollout, Aug 13 2026)

| Phase | Scope | Evidence |
|---|---|---|
| 0 | T0: ADR-0003 accepted, model v0.3.0 (49 entities, 27 BBs, 56 rels, +ai-automation-governance dimension), `governed_by` schema+validator, D6 discriminator check downgraded to warning (user decision: models land as authored) | tag `v0.3.0` |
| 1 | T1 dea-metamodel: graph regen, 12 new entity schemas, TS/TTL/pydantic regen | PR (see repo) |
| 2 | T3 viewers: new entities flow via sync chain — Pages graph v0.3.0 (49 ent / 56 rels), SVG 49 markers, viewer bundle verified live | live URLs |
| 3 | T2: 11 catalog repos scaffolded foundation-first (12 entities; MDP+MFS share `dea-catalog-model-deployments`), each with README entity detail + pointer + `validate-allocation` CI — 11/11 green | repo list |

## Executed phases (ADR-0002 rollout, Aug 13 2026)

| Phase | Scope | Evidence |
|---|---|---|
| 0 | T0 `dea-architecture-framework`: ADR-0002 accepted, model v0.2.0, schema + validators upgraded, docs aligned | PR #1, tag `v0.2.0` |
| 0b | T0 validator: multi-entity pointers + discriminator enforcement | PR #2, tag `v0.2.1` |
| 1 | T1 `dea-metamodel`: entity-graph.json generated from pinned model; PUML/SVG pipeline; 4 new schemas (EA/VE/CA/BF); pydantic scaffold; TS/TTL updated; `opendeam-sync` receiver | PR #67 |
| 2 | T3 viewers: `technehub-labs.github.io` graph-derived viewer; `dea-web-viewer` dimension support | PR #9, PR #14 |
| 3 | T2 catalogs: 28 `dea-catalog-*` pointers regenerated + `validate-allocation.yml` caller CI pinned to `@v0.2.1` | 28/28 caller CI green |

Auto-propagation: `fan-out.yml` (T0) → `opendeam-sync.yml` (T1) → render +
Pages notify → viewer bake. `MODEL_SYNC_TOKEN` configured.

## Earmarked for future action

### Legacy catalog repos (not mapped to any OpenDEAM entity)

These four repos predate the OpenDEAM allocation and host no entity in the
model. Their `metamodel-pointer.yaml` files still reference the superseded
`v3.0.0-alpha` scheme. **No action taken in the v0.2.0 rollout — parked
deliberately.** Each needs one of: (a) map to a model entity (may require a
new entity → additive PR + patch bump), (b) re-classify as a composite /
non-catalog repo, or (c) retire/archive.

| Repo | Current state | Candidate disposition |
|---|---|---|
| `dea-catalog-agent-foundry` | Legacy pointer, no model entity | Composite concept (agents span L3–L5) — likely (b) |
| `dea-catalog-solution-hub` | Legacy pointer, no model entity | Composite (solution archetypes) — likely (b) |
| `dea-catalog-reference-architecture` | Legacy pointer, no model entity | Overlaps `dea:entity-blueprint` (BLU, L2 — renamed from RM in v0.4.0) — candidate (a) |
| `dea-catalog-ontologies` | Legacy pointer, no model entity | Semantics content — `dea:entity-concept` (CON) + semantic-dimension now exist (v0.4.0) — candidate (a) via CON or (b) |

**Trigger for action:** any of these repos gaining real content, or the next
structural ADR touching L2 semantics / reference knowledge. Until then they
are excluded from `validate-allocation` wiring by design.

### New catalog repos named by v0.5.0 (ADR-0005, not yet created)

The model names five T2 repos that do not exist yet. **Create when first
content lands**, foundation-first per the ADR-0003 Phase 3 pattern (README
entity detail + pointer + `validate-allocation` CI):

| Repo | Entity | Pattern |
|---|---|---|
| `dea-catalog-financial-resources` | Financial Resource (FR, L3) | repo-per-specialization |
| `dea-catalog-physical-resources` | Physical Resource (PHR, L3) | repo-per-specialization |
| `dea-catalog-intangible-resources` | Intangible Resource (INR, L3) | repo-per-specialization |
| `dea-catalog-information-assets` | Information Asset (IA, L4) | single entity |
| `dea-catalog-knowledge-assets` | Knowledge Asset (KA, L4) | single entity |

Resource subclasses use **repo-per-specialization** (no shared repo, no
discriminator) — the completeness contract's single-dimension rule is enforced
structurally by repo separation. Confirmed as the precedent for future
category roots (ADR-0005 review amendment 3). Resource itself is abstract and
carries `catalog_repo: null` — no RES catalog.

### `entity_role` / `completeness_contract` retrofit (future ADR)

Retrofit the two ADR-0005 governance fields onto the 47 pre-v0.5.0 entities
and introduce the validator rule "abstract or governance-role entities MUST
carry `completeness_contract`". **Trigger:** after 2–3 worked examples
exercise the mechanism (ADR-0005's six are the first), to avoid over-fitting
the validator to one case.

### Collaboration Agreement catalog candidate

`dea:entity-collaboration-agreement` (CA, L1) carries `catalog_repo: null`,
but ADR-0005 D1's Lease mapping (a lease is a CA catalog instance) points at
a CA catalog conceptually. Candidate: `dea-catalog-collaboration-agreements`
when agreements content lands. Earmarked, not a v0.5.0 gap.

## Known non-blocking items

- `reports/REPORT.md` (Pages repo) retains pre-OpenDEAM layer names —
  dated historical report, intentionally not rewritten.
- `metamodel.yaml` per-entity `ttl/entities/*.ttl` paths reference files
  that do not exist (same drift class as the pre-v0.2.0 `pydantic/` gap;
  pydantic was scaffolded in Phase 1, TTL per-entity split deferred).
- SVG relationship lines render as 0 with the ELK layout engine —
  relationships are drawn by the viewer.js overlay; validator treats this
  as informational. Revisit if we switch layout engines.
