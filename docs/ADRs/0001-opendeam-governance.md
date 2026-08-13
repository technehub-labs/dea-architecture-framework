# ADR-0001: OpenDEAM Governance — Root Authority for DEA Architecture

- **Status:** Accepted
- **Date:** 2026-08-12
- **Deciders:** eaojnr
- **Supersedes:** de-facto authority of `dea-metamodel/viewer/entity-graph.json` (v2.0.0-alpha, 5 layers)

## Context

The DEA organisation accumulated three competing "layer" models:

1. `dea-metamodel/viewer/entity-graph.json` — 5 layers, 33 entities. Machine-enforced; all tooling consumes it.
2. `dea-metaframework/metamodel/README.md` — "Enterprise Concepts Metamodel v3.0", 6 layers, 23 entities, claiming source-of-truth status.
3. Catalog READMEs — a repository-stack usage of "Layer" (L0 metamodel / L1 catalogs / L2 tooling / L3 governance), colliding with architecture-layer nomenclature.

Version strings also drifted (`0.1.0-alpha` / `v2.0.0-alpha` / `v3.0.0-alpha` across repos).

Decision (2026-08-12, eaojnr): adopt the **6-layer ecosystem-on-top model**, establish a **new root repository** with dea-metamodel as a consumer, keep **dea-metaframework separate** as the orthogonal "city-block" allocation structure, brand the model **OpenDEAM**, and enforce consistency via **both** a reusable PR validator and a central drift-detection cron.

## Decision

1. **Single root.** This repository (`dea-architecture-framework`) hosts `model/opendeam-model.yaml` — the single source of truth for architecture layers (L1–L6 as of v0.1.0; L1–L5 + Measurement Dimension as of v0.2.0 per ADR-0002), building blocks, entity allocation, and relationships. No other repo may claim source-of-truth status for these concepts.
2. **dea-metamodel is a consumer.** Its `viewer/entity-graph.json`, PUML, SVG, and schema layer-enums become generated from / pinned to this model (Phase 2).
3. **dea-metaframework is an orthogonal allocator, not a competitor.** It owns the ECF 7×7 "city-block" matrix (domain × lifecycle stage). OpenDEAM answers *which layer does this object belong to*; the ECF matrix answers *which city block does this object operate in*. The model references the matrix via `orthogonal_allocators`; it does not redefine it.
4. **Terminology rule.** "Layer" (L1–L6 as of v0.1.0; L1–L5 as of v0.2.0 per ADR-0002) means architecture layer, defined only here. Repository-stack position is "Tier" (T0–T3). Any org document using "Layer" for stack position is drift.
5. **Change control.**
   - Structural changes (add/remove layer, new orthogonal dimension, entity re-allocation, relationship semantic change) → ADR + minor version bump.
   - Additive changes (new entity in an existing building block, new relationship, new building block) → PR + patch version bump.
   - `scripts/validate_model.py` must pass on every PR.
6. **Enforcement.**
   - `validate-against-model.yml` (reusable workflow) runs in consumer repos on PRs touching allocation declarations, pinned to a model tag.
   - A central drift-detection cron (Phase 4) diffs every consumer's declared state against the model and opens issues.
7. **Versioning.** The model is versioned independently (`VERSION` file + git tags `vX.Y.Z`). Consumers pin a tag; they never track `main`.

## Consequences

- `dea-metaframework/metamodel/README.md`'s "Source of truth" claim must be reframed to "canonical *narrative* of the ECF matrix; architecture layering defers to OpenDEAM" (Phase 5).
- Four entities enter the model as `planned` without catalog repos: Ecosystem Actor (EA), Value Exchange (VE), Collaboration Agreement (CA), Business Function (BF). Their catalog allocation is future ADR business.
- One relationship from the v2 set is superseded: `CAP → OU "owned by"` is replaced by the v3 chain `CAP → BF "grouped by"` + `BF → OU "owned by"`.
- Consumers carry a migration burden (pointer files, badges, READMEs) handled in Phases 2–4.
