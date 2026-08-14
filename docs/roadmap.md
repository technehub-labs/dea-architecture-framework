# OpenDEAM Program Roadmap

The single program-level plan for the OpenDEAM rollout across the org.
Phase detail lives in the ADRs and PR history; this file tracks **what is
done, what is live, and what is earmarked for future action**.

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

## Known non-blocking items

- `reports/REPORT.md` (Pages repo) retains pre-OpenDEAM layer names —
  dated historical report, intentionally not rewritten.
- `metamodel.yaml` per-entity `ttl/entities/*.ttl` paths reference files
  that do not exist (same drift class as the pre-v0.2.0 `pydantic/` gap;
  pydantic was scaffolded in Phase 1, TTL per-entity split deferred).
- SVG relationship lines render as 0 with the ELK layout engine —
  relationships are drawn by the viewer.js overlay; validator treats this
  as informational. Revisit if we switch layout engines.
