# Changelog

All notable changes to the OpenDEAM (dea-architecture-framework) repo are
documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this repository is governed by change requests (`change-requests/`) and
ADRs (`docs/ADRs/`).

## [Unreleased]

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
