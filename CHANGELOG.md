# Changelog

All notable changes to the OpenDEAM (dea-architecture-framework) repo are
documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this repository is governed by change requests (`change-requests/`) and
ADRs (`docs/ADRs/`).

## [Unreleased]

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
