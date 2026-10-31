# CR-AR-FMWK-15: Information Model Entity Allocation (IM)

| Field | Value |
|---|---|
| **CR** | CR-AR-FMWK-15 |
| **Title** | Information Model entity allocation (IM; L4-information-knowledge) |
| **Status** | Merged (this PR) |
| **Layer** | OpenDEAM (T0 root-model) |
| **Programme** | Information Model governance chain (root model → metamodel → catalog) |
| **Architectural parent** | ADR-0005 (information family); dea-metamodel CR-4 §12 (Information core anchor) |
| **Depends on** | None (additive) |
| **Enables** | dea-metamodel CR-MET-019 (canonical entity); `dea-catalog-information-models` stand-up (catalog-side CR-IM-CAT series); CR-013 portfolio registration (dea-governance CR-017) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-01 |
| **Version bump** | MINOR (0.8.2 → 0.9.0) — additive entity allocation |

## 1. Executive summary

Allocates `dea:entity-information-model` (alias `IM`) to layer L4, building block L4-information-knowledge, specializing the Information kernel (`INF`), with `catalog_repo: dea-catalog-information-models` and `status: planned`. This closes a real gap in the information family: the family has classification (InformationClass — the sensitivity/regulatory band) and consumption forms (InformationAsset — the consumable shape) but no entity for the **conceptual/logical blueprint** that specifies the structure, semantics, and constraints of information for a domain.

## 2. Scope

### In scope

1. The allocation entry (81st entity; validator: 5 layers, 27 building blocks, 81 entities, 118 relationships, v0.9.0).
2. `VERSION` + `model.version` MINOR bump.

### Out of scope (per CR-AR-FMWK-04 §2 precedent)

1. The canonical entity definition, schema, and relationships — owned by dea-metamodel CR-MET-019.
2. The new catalog repository and its foundation — owned by the catalog-side CR-IM-CAT series.
3. The governance portfolio registration — owned by CR-013 (dea-governance), CR-017.

## 3. Entity allocation

| Entity | Layer | Building block | Alias | Specialises | Catalog |
|---|---|---|---|---|---|
| `dea:entity-information-model` | L4 | L4-information-knowledge | IM (unassigned prior to this CR) | INF | `dea-catalog-information-models` (status: planned) |

**Definition** (canonical text; the metamodel CR carries the full relationship surface): *"A formal model that specifies the structure, semantics, and constraints of information for a domain — the conceptual or logical blueprint from which Data Entities are shaped and Information Assets take form. Distinct from Information Class (the sensitivity/regulatory band) and Information Asset (the consumable form)."*

## 4. Distinctness

| Sibling | Boundary |
|---|---|
| InformationClass (IC) | The sensitivity/regulatory **band** other records map to via `dea:maps-to`; not a model of structure |
| InformationAsset (IA) | Data given **consumable form** (report, dashboard, invoice); takes form *from* a model, is not one |
| DataEntity (DE) | The **persistent structure** itself; a model specifies it, is not it |
| AIMLModel (AIM) | A trained model (an AI artifact); unrelated sense of "model" |
| Concept (CON) | A unit of meaning; conceptual meaning precedes formal structure (CR-CM-001 §4) — the promotion path for this entity's own definition followed exactly that route |

Alias `IM` was verified unassigned in the root model's 99-alias set and the metamodel alias registry (validator enforces uniqueness).

## 5. Version-site note

ADR-0008 (Proposed, unlanded) targets v0.9.0 for a per-entity folder-structure restructure. This CR's additive allocation lands first and takes v0.9.0 (both are MINOR-bump class); when ADR-0008 lands it rebases to v0.10.0. Recorded here so the rebase is expected, not a surprise.

## 6. Verification

`scripts/validate_model.py`: OpenDEAM model OK — 5 layers, 27 building blocks, 81 entities (14 dimension), 118 relationships (v0.9.0). Pre-existing SC/MDP discriminator convention warnings unchanged.

## 7. NOT-list

1. No relationship-type changes in the root model.
2. No metamodel, catalog, or governance content changes in this PR.
3. No existing entity entry is modified.
