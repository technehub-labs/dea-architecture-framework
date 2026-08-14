# DEA Architecture Framework — OpenDEAM

> **OpenDEAM (Open Digital Enterprise Architecture Model)** — the root authority for the TechNeHub Labs DEA architecture: layers, building blocks, entity allocation, and relationships.

[![Model Version](https://img.shields.io/badge/OpenDEAM-v0.4.0--alpha-2DD4BF?style=flat-square)](./VERSION)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](LICENSE)

## What this is

One file — [`model/opendeam-model.yaml`](model/opendeam-model.yaml) — defines:

1. **Architecture parts**: 5 layers → building blocks (first-level components).
2. **Object allocation**: every first-level entity mapped to exactly one layer + building block (MECE), with its catalog repository. Abstract entities may be realised by subclasses in other layers (ADR-0002 D3).
3. **Relationships**: typed edges between entities (`rel_type` + `cardinality`).
4. **Orthogonal allocators**: the ECF 7×7 city-block matrix (owned by `dea-metaframework`), and the **Measurement Dimension** (cross-cutting, owned here) — referenced and exercised, never treated as layers.

Everything else in the organisation — `dea-metamodel` schemas and viewer graph, catalog `metamodel-pointer.yaml` files, README badges, the Pages viewers, `dea-web-viewer` — is a **derived consumer** of this model, version-pinned and CI-validated.

## The five layers

| Layer | Name | Scope | Entities |
|---|---|---|---|
| **L1** | Ecosystem & Value Network | External | 6 |
| **L2** | Strategic & Governance | Intent & Rules | 15 |
| **L3** | Business Operating Model | Internal | 12 |
| **L4** | Digital & Intelligence | Data & Brain | 8 |
| **L5** | Technology & Execution | Systems & Infra | 7 |

Plus two orthogonal dimensions: the **Measurement Dimension** (`Performance Metric` — measurable entities declare `measured_by`, metrics declare `scope_layers`; ADR-0002 D1) and **AI & Automation Governance** (AI-driven entities may declare `governed_by: [Risk/Control/Regulation]`; ADR-0003 D6). See the ADRs for why these are dimensions, not layers.

Derived from the enterprise axiom: *"An enterprise is any bounded entity that persists by exchanging value with its environment."* See [`docs/allocation-rationale.md`](docs/allocation-rationale.md).

## Terminology (binding)

- **Layer** — architecture layer L1–L5. Defined only here. Measurement is NOT a layer (v0.2.0+) — it is an orthogonal dimension.
- **Tier** — repository-stack position T0–T3. **Never** call a tier a "layer".
- **Building block** — named grouping of entities within a layer.
- **Entity** — first-level architecture object, exactly one layer + one building block (unless abstract or a dimension entity).

## Consumption contract

Consumers pin a model **tag** and validate against it:

```yaml
# In a consumer repo's workflow (e.g. dea-catalog-processes)
jobs:
  allocation:
    uses: technehub-labs/dea-architecture-framework/.github/workflows/validate-against-model.yml@v0.4.0
    with:
      model_ref: v0.4.0
      pointer_file: metamodel-pointer.yaml
```

- PRs that drift from the pinned model (wrong layer, stale alias, unknown entity) **fail CI**.
- A central drift-detection cron diffs all consumers against the model and opens issues (Phase 4).

## Change control

| Change | Requirement |
|---|---|
| New/removed layer, new dimension, re-allocation | ADR + **minor** version bump |
| New entity / building block / relationship | PR + **patch** version bump |
| Every PR | `scripts/validate_model.py` passes |

See [`docs/ADRs/0001-opendeam-governance.md`](docs/ADRs/0001-opendeam-governance.md).

## Repository map

```
T0  dea-architecture-framework   ← this repo (root model)
T1  dea-metamodel                ← machine schemas, viewer graph (consumer)
T2  dea-catalog-*                ← entity instance catalogs (consumers)
T3  dea-cli, dea-web-viewer, technehub-labs.github.io  ← tooling & viewers (consumers)
⟨orthogonal⟩  dea-metaframework  ← ECF 7×7 city-block matrix (referenced allocator)
```

## Structure

```
├── model/opendeam-model.yaml          # THE source of truth
├── schemas/opendeam-model.schema.json # JSON Schema for the model
├── scripts/
│   ├── validate_model.py              # schema + referential integrity (CI)
│   └── validate_consumer.py           # consumer pointer drift check
├── docs/
│   ├── ADRs/0001-opendeam-governance.md
│   └── allocation-rationale.md        # 5→6 layer mapping + boundary rules
└── .github/workflows/
    ├── model-ci.yml                   # validate on every PR/push
    ├── validate-against-model.yml     # reusable consumer validator
    └── fan-out.yml                    # dispatch model changes to consumers
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
