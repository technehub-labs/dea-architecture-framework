# Changelog

All notable changes to the OpenDEAM (dea-architecture-framework) repo are
documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this repository is governed by change requests (`change-requests/`) and
ADRs (`docs/ADRs/`).

## [Unreleased]

### CR-AR-FMWK-13: Supersedes/Replaces Vocabulary Resolution + Schema Hygiene

Resolves the CR-AR-FMWK-09 §4 deferral: entity identity supersession stays the
entity-level `supersedes` field (ISF precedent, EGV-004 continuity);
instance-level supersession stays with the metric programme; replacement/
retirement stays the Core `dea:replaces` + the existing deprecated/retired
lifecycle states. No `supersedes` rel_type value added. Closes a hygiene
gap: `supersedes` (ISF) and `legacy_ids` (PRC) were used in the model but
undeclared in the schema — both now declared. Adds `terminology.supersedes`
and validator rule 10 (targets must exist as entity_ids, no chains) with 3
negative controls verified. Patch bump v0.8.0 → v0.8.1. No entity or
relationship content changes. Carrier:
`change-requests/CR-AR-FMWK-13-supersedes-vocabulary.md`.

## [v0.8.0] - 2026-10-27

ADR-0007 (core anchor promotion), executed by CR-AR-FMWK-12. The
CR-004 Core/Profile split is now reflected upstream: 5 abstract
kernels (ArchitectureElement AE, Behavior BEH, Service SRV, Information
INF, Organization ORG) + 5 concrete entities (Decision DEC, Outcome OUT
in L2-intent; Requirement REQ, Constraint CST in L2-rules-guidance;
Change CHG in L3-people-skills-culture), all status planned, catalog_repo
null. 8 existing entities re-parented via one `specializes` field each
(PRC→BEH, BS→SRV, BO/DE/IA/KA/DP→INF, OU→ORG) + 5 specialization
edges. 10 identity mappings added to the identifier map. Model: 70 →
80 entities, 113 → 118 relationships. No existing entity_id,
class_alias, layer, building_block, or status changed; no validator or
schema change.

## [v0.7.7] - 2026-10-27

Consolidation release of the lifecycle truth-up and Metric programme
completion (CR-AR-FMWK-06 through CR-AR-FMWK-11; tags v0.7.2–v0.7.7).
70 entities (14 dimension), 27 building blocks, 113 relationships.

### CR-AR-FMWK-11: Metric Dimension-Entity Lifecycle Promotion (proposed → planned)

Closes the CR-AR-FMWK-08 §8 deferral with a documented governance
convention: dimension entities follow the same ordered lifecycle, but
their status expresses programme commitment, not catalog-content backing
— `planned` when admitted, allocated, and wired; `scaffold`/`existing`
never apply to a `catalog_repo: null` dimension entity unless a
per-entity catalog is later chartered. Validator rule 5 already enforces
this structurally, so the convention is self-enforcing; no validator or
schema change. Twelve Metric dimension entities (MMT, MOBS, IDS, BSL,
PTG, THR, PIT, RPT, PRV, ANR, COR, CSH) promoted proposed → planned:
admitted via CR-MET-001..012, allocated by CR-AR-FMWK-05, wired by
CR-AR-FMWK-09/10. MTR untouched (existing, real catalog); CON untouched
(independent create-on-content question). Patch bump v0.7.6 → v0.7.7 in
both `VERSION` and `model.version`. Carrier:
`change-requests/CR-AR-FMWK-11-dimension-lifecycle-promotion.md`.

### CR-AR-FMWK-10: Metric `measured_by` Integration Surface (root-model slice)

The CR-AR-FMWK-09 §4 follow-on: wires the metamodel's 16-type
measured/assessed integration surface (docs/metric-capability-map.md §5)
onto OpenDEAM entities. Additive: `measured_by: [MTR]` on 9 entries (DE,
OU, VS, APC, AIM, SC, TRE, RSK, CTL) + 10 governance edges (103 → 113
relationships), including the missing `ISF → MTR` edge for consistency
with its BP/CAP/SF peers. Four Core metamodel types documented out of
scope with reasons (AssessmentDimension, MaturityModel, Policy, Service).
Zero pre-existing entries, fields, or edges modified (verified
programmatically). Patch bump v0.7.5 → v0.7.6 in both `VERSION` and
`model.version`. Carrier:
`change-requests/CR-AR-FMWK-10-metric-integration-surface.md`.

### CR-AR-FMWK-09: Metric Programme Relationships (root-model slice)

The CR-AR-FMWK-05 §7 follow-on: wires the twelve Metric dimension
entities with 24 intra-capability edges (79 → 103 relationships),
translated from the canonical 23-relationship capability in
`dea-metamodel` docs/metric-capability-map.md §4 onto the existing
closed rel_type vocabulary (no expansion). Includes the
`MOBS → MOBS corrects` self-edge. Out-of-scope metamodel edges
documented with reasons. Additive only: zero entity entries and zero
pre-existing edges changed. Patch bump v0.7.4 → v0.7.5 (merge-artifact
restore via PR #25). Carrier:
`change-requests/CR-AR-FMWK-09-metric-relationships.md`.

### CR-AR-FMWK-08: Org-Wide `proposed`-Status Audit (9 Promotions)

The org-wide audit deferred by CR-AR-FMWK-06 §7: every `proposed` entity
enumerated, each `catalog_repo` checked live against GitHub (2026-10-27).
Nine promotions proposed → planned (EP, RSK, CTL, REG, SIG, EXP, TRE, MDP,
MFS) — each has an existing foundation-first catalog repo with no
`CATALOG.yaml`, the exact evidence class accepted in CR-AR-FMWK-06/07.
Nineteen remain `proposed` with reasons documented: six named-but-nonexistent
repos (CON, FR, PHR, INR, IA, KA — create-on-content), two abstract kernels
(PRC, RES), twelve metric-programme dimension entities (deferred to the
metric follow-on). Patch bump v0.7.3 → v0.7.4 in both `VERSION` and
`model.version`. Zero semantic drift verified: exactly 9 entities changed,
only `status`, relationships and terminology untouched. Carrier:
`change-requests/CR-AR-FMWK-08-org-proposed-audit.md`.

### CR-AR-FMWK-07: Skill (SKL) & Change Initiative (CHI) Status Promotion (proposed → planned)

Forward lifecycle transitions for `dea:entity-skill` (SKL) and
`dea:entity-change-initiative` (CHI), both L3, L3-people-skills-culture:
`status: proposed` → `status: planned`, one line each in
`model/allocation.entities`. Same evidence class as CR-AR-FMWK-06:
`dea-catalog-skills` and `dea-catalog-change-initiatives` both exist with
the foundation-first scaffold but no `CATALOG.yaml` and no canonical
entries — the exact `planned` state per the STRUCT-07c status↔content
contract. Completes the promotion of the entire L3-people-skills-culture
building block out of `proposed`. Patch bump v0.7.2 → v0.7.3 in both
`VERSION` and `model.version`. All other fields, the `SKL → ROL` and
`CHI → OU` relationships, and every other entity unchanged. Carrier:
`change-requests/CR-AR-FMWK-07-skl-chi-status-promotion.md`.

### CR-AR-FMWK-06: Role (ROL) Status Promotion (proposed → planned)

Forward lifecycle transition for `dea:entity-role` (ROL, L3,
L3-people-skills-culture): `status: proposed` → `status: planned`, one
line in `model/allocation.entities`. Evidence: `dea-catalog-roles` exists
with the foundation-first scaffold (README entity detail, LICENSE, NOTICE,
`metamodel-pointer.yaml`) but no `CATALOG.yaml` and no canonical Role
entries — the exact `planned` state per the STRUCT-07c status↔content
contract. Patch bump v0.7.1 → v0.7.2 in both `VERSION` and `model.version`
(forward transition = PR + patch bump, no ADR). All other ROL fields, both
ROL relationships (`SKL → ROL` required by, `ROL → AC` fulfilled by), and
every other entity unchanged. Sibling promotions (SKL, CHI) deferred to a
follow-on audit CR. Carrier:
`change-requests/CR-AR-FMWK-06-role-status-promotion.md`.

### CR-AR-FMWK-03: Entity System Cross-Reference (Architecture Framework Slice)

Architecture Framework cross-reference slice of the General Entity System institutionalisation (cross-repo cascade T7 of the umbrella programme). The Architecture Framework repo is an architecture framework (ADRs) repo; it does not contain entity records and does NOT adopt the entity-system gate. This PR records the cross-reference to `dea-governance` (DEA-ID-000 + CR-012) and enumerates the Architecture Framework repo's commitments to the General Entity System standard. D-004 clean. 118a/b/c authorship gates remain CONFORMANT.

### CR-AR-FMWK-02: Authorship Cardinal Rule (R1, R2) - Org-Wide Propagation Slice

User directive 2026-10-13: "no `Coder` / `Agent` / agent or tool names in any
authorship field of any published artifact". The CR-BP-118 cardinal rules (R1
and R2) are propagated to this repo. New blocking gate
`scripts/check_authorship.py` (CR-BP-118 / AUT-001..003), data-driven from
`reconciliation/authorship-fields.yaml` (allowlist
`{Emmanuel A. Otchere, TechNeHub Labs}`; denylist
`{Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}`).
A retroactive sweep rewrites every authorship-metadata hit in the repo: 2
files, 2 textual replacements (`**Author**` in CR-AR-FMWK-01 and
`**Author:**` in ADR-0006). 0 entity content changes; 0 id changes; 0
cross-reference changes. The architecture-framework repo uses TWO field
shapes: `**Author**` (in change-requests/CR-*.md, table-row form) and
`**Author:**` (in docs/ADRs/*.md, line metadata with colon inside bold).
The registry enumerates both. CI wiring: new workflow
`.github/workflows/validate-authorship.yml` runs the gate in `--strict` mode
on every push and PR. 21/21 `test_check_authorship` pass. Carrier:
`change-requests/CR-AR-FMWK-02-authorship-cardinal-rule.md`.
