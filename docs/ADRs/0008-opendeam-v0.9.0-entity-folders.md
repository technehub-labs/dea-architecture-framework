# ADR-0008: OpenDEAM v0.9.0 — Per-Entity Folder Structure (self-contained entity sources)

**Status:** Proposed (this PR)
**Supersedes:** opendeam-model.yaml v0.8.2 (monolithic entity list)
**Version bump:** MINOR (0.8.2 → 0.9.0) — structural re-organisation of the
model's source layout, with the monolith retained as a generated artifact.

**Author:** Emmanuel A. Otchere
**Date:** 2026-10-27

## Context

The model's 80 entities live as one list — `allocation.entities` — inside a
single 1,300-line `model/opendeam-model.yaml`. Every entity edit touches the
same file, so:

1. **Concurrent development collides.** Two CRs touching different
   entities conflict in git on the shared file (this session's stacked-PR
   version-site collisions were a small taste of the class).
2. **Review surface is the whole model.** A one-line status flip produces a
   diff readers must scan past 79 unrelated entities to verify — every CR
   this session carried a "zero semantic drift, verified programmatically"
   paragraph precisely because the diff shape invites doubt.
3. **No per-entity home.** An entity has no folder where its definition,
   its relationships, its catalog pointer expectations, and (later) its
   worked examples and notes can live together. Developing "each entity"
   means developing a region of a shared file.

The consumer contract is the hard constraint. `model/opendeam-model.yaml`
is read at a **fixed path** by:

- `scripts/validate_model.py` (this repo's CI, every PR)
- `scripts/validate_consumer.py` — invoked by
  `.github/workflows/validate-against-model.yml`, which **30+ consumer
  repos pin by tag** (`@v0.x.y`) and call from their own CI
- `scripts/check_catalog_index_matches_model.py` (the STRUCT-07c smoke
  test, wired into `model-ci.yml`)
- `dea-metamodel/.github/scripts/generate_entity_graph.py` (via
  `opendeam-sync.yml`, dispatched by this repo's `fan-out.yml` on every
  model/VERSION change to main)

Any layout change that breaks the fixed path breaks every pinned consumer
simultaneously, with no upgrade path short of every consumer re-pinning.

## Decisions

### D1 — Entity sources move to per-entity folders; a folder per first-level entity

**Decision:** each entity gets a self-contained folder under
`model/entities/`, keyed by class_alias:

```
model/entities/
├── ROL/
│   └── entity.yaml        # the entity entry (the exact allocation.entities item)
├── SKL/
│   └── entity.yaml
├── MTR/
│   └── entity.yaml
...
```

`entity.yaml` contains exactly the mapping that today is one item of
`allocation.entities` — same fields, same schema item, no new fields.
Entity **development** now happens in one folder: edit `entity.yaml`,
open a PR, review reads one small file.

Shared model context (layers, building blocks, allocators, terminology,
model metadata) stays in `model/context.yaml` — the parts that are not
per-entity.

Relationships are **not** split per-entity in this ADR (see D4).

### D2 — The monolith becomes a generated artifact, and stays at the fixed path

**Decision:** `model/opendeam-model.yaml` remains in the tree, at the same
path, with identical semantic content — but becomes **generated**:
`scripts/build_model.py` assembles it from `model/context.yaml` +
`model/entities/*/entity.yaml`, in stable (class_alias-sorted) order.
Deterministic output: identical inputs produce byte-identical YAML, so
 diffs of the artifact remain reviewable and merges of the artifact are
trivially resolvable by regeneration.

CI (`model-ci.yml`) gains a **build+drift step**: rebuild the monolith
and fail if it differs from the committed artifact — the generated file
cannot silently drift from the sources. This mirrors how generated
artifacts are already governed downstream (`entity-graph.json` is
committed and drift-checked in `dea-metamodel`).

**Consumer impact: zero.** The pinned-path consumers read the same file,
same shape, same semantics. Consumers do not re-pin, do not change
workflows, and their `@v0.x.y` pins continue to resolve. The fan-out and
sync chain see the same artifact.

### D3 — Validation runs against the sources (and the artifact)

**Decision:** `scripts/validate_model.py` gains a `--source` mode that
builds the model from sources in-memory and validates it; the default
path (monolith) is unchanged so every pinned consumer's invocation keeps
working without modification. CI order becomes:

1. `build_model.py` (sources → monolith)
2. drift check (regenerated == committed)
3. `validate_model.py` (monolith; schema + integrity rules 1–10)
4. smoke test (unchanged)

The schema (`schemas/opendeam-model.schema.json`) is unchanged — the
monolith it validates has the same shape. Per-entity `entity.yaml` files
validate against the same entity item schema (the validator's source
mode validates each file against the `allocation.entities.items`
subschema).

### D4 — Relationships: one shared registry file, split deferred

**Decision:** `relationships` stays a single registry
(`model/relationships.yaml`) moved out of the monolith as a source file
with the same list shape. Per-entity splitting of relationships is
deliberately **deferred**: an edge has two endpoints, so a per-entity
split creates either duplication (each edge in both folders) or
ownership ambiguity (whose folder owns the edge?). Both are worse than
the shared file. The registry is append-only in practice (CR-09/10/12
each appended edges); append-bys are low-collision. A future ADR may
introduce per-entity relationship declarations with a dedup rule if
real collision pain emerges.

### D5 — Migration and idempotence guarantee

**Decision:** the migration CR executes a mechanical split:

1. `build_model.py` is added first, with a `--check` mode proving the
   round-trip: monolith → sources → monolith is **semantically
   identical** (parsed-equal, entity-for-entity and edge-for-edge).
2. Sources are generated from the current monolith (never hand-typed).
3. The monolith is regenerated from sources and compared to the
   pre-split model: zero semantic drift, verified programmatically in
   the CR (the same discipline as CR-AR-FMWK-09/10/12).
4. CI wiring (build + drift + validate) lands in the same CR so main
   is never in a sources-without-drift-gate state.

Ordering inside the monolith changes from insertion-order to
class_alias-sorted (the only acceptable textual difference; semantic
comparison is the acceptance gate, and consumers parse rather than diff).

### D6 — Version and rollout

**Decision:** v0.8.2 → **v0.9.0** (minor: structural re-organisation,
ADR-gated per the change-control table — the "re-allocation"-adjacent
class; no entity, layer, or relationship semantics change).

Rollout:

- **T0 (this ADR + CR-AR-FMWK-15):** sources, builder, CI wiring,
  regenerated monolith, README structure section update.
- **T1 `dea-metamodel`:** no action required (reads the same artifact);
  the next sync run after merge is the live verification.
- **T2 consumers:** no action; pins keep resolving.
- **T3 viewers:** no action (downstream of T1's artifact).

The README's "One file" framing becomes "One model, assembled from
per-entity sources" — the source of truth is the **sources**; the
monolith is its deterministic projection.

## Consequences

- Entity development is folder-scoped: CRs touch one `entity.yaml` plus
  the shared registries only when relationships/version change.
- Review surfaces shrink to the entity folder; the drift paragraph in
  future CRs cites the builder's `--check` idempotence rather than ad-hoc
  comparison scripts.
- New entities land as a new folder + a builder re-run (the append-only
  pattern continues; `build_model.py` picks up folders automatically,
  so no registration list is needed).
- The monolith remains the consumer contract surface until a future ADR
  moves consumers to per-entity reads — deliberately **not** this ADR;
  one breaking change class per release.
- Risk accepted: two CRs editing the *same* entity still collide (as
  they must). The win is cross-entity independence.

## Alternatives considered

1. **Keep the monolith, add comments/markers.** — does not deliver
   folder-scoped development or small review surfaces; rejected.
2. **Split per-entity without keeping the monolith.** — breaks 30+
   pinned consumers at once with no migration path; rejected.
3. **Monolith generated but uncommitted (build on demand).** — pinned
   tags must contain the artifact for `validate-against-model.yml`'s
   checkout to work; rejected.
4. **Per-entity relationship files now.** — endpoint duplication or
   ownership ambiguity (D4); deferred.

## Implementation CR (follow-on, ADR-0006/0007 pattern)

CR-AR-FMWK-15 will execute: `model/context.yaml`,
`model/entities/<ALIAS>/entity.yaml` × 80, `model/relationships.yaml`,
`scripts/build_model.py` (with `--check`), `model-ci.yml` wiring, README
structure section, version → 0.9.0. Acceptance: round-trip idempotence
proven; semantic equality with v0.8.2 proven; all gates green.
