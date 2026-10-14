# CR-AR-FMWK-02: Authorship Cardinal Rule (Org-Wide Propagation Slice)

| Field | Value |
|-------|-------|
| **CR** | CR-AR-FMWK-02 |
| **Title** | Authorship Cardinal Rule (R1, R2) - Org-Wide Propagation Slice (dea-architecture-framework) |
| **Status** | Accepted (per user directive 2026-10-13) |
| **Layer** | L0 (OpenDEAM architecture framework) |
| **Depends on** | CR-BP-118 (org-wide authorship cardinal rule, main authority) |
| **Companion to** | CR-DEA-BC-34 (BC slice), CR-BO-03 (BO slice), CR-OU-03 (OU slice), CR-ECF-009 (MF slice), CR-MM-04 (metamodel slice) |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-13 |

## 1. The cardinal rule (pinned)

Two cardinal rules from CR-BP-118 (org-wide authority) are propagated to this
repo (dea-architecture-framework):

- **R1 (Authorship-field cardinal rule)**: every authorship-bearing field must
  carry a value from the allowlist `{Emmanuel A. Otchere, TechNeHub Labs}`.
  Substring matches against the denylist
  `{Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}` are
  blocking (AUT-001).
- **R2 (Named-role file cardinal rule)**: any file or field whose purpose is
  to name a person playing a named role must carry the canonical identity.

The rules are CR-level (immutable by a gate change) and governance-doc-level
(immutable by a code change).

## 2. The retro sweep (architecture-framework-repo scope)

2 files, 2 textual replacements:

| File | Field | Replaced |
|---|---|---|
| change-requests/CR-AR-FMWK-01.md | `**Author**` (table-row) | `Coder (for eaojnr)` -> `Emmanuel A. Otchere` |
| docs/ADRs/0006-opendeam-v0.6.0-process-kernel-specialization.md | `**Author:**` (line metadata) | `Coder (for eaojnr)` -> `Emmanuel A. Otchere` |

Total: 2 files, 2 textual replacements. 0 entity content changes; 0 id
changes; 0 cross-reference changes. The architecture-framework repo has 0
entity YAMLs, 0 CITATION.cff, and 0 catalog-research YAML; the field set is
CR-doc + ADR metadata only.

## 3. The gate (architecture-framework-repo, blocking)

- **AUT-001 (blocking)**: substring denylist against
  `{Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}`.
- **AUT-002 (blocking)**: parent-block present but field empty.
- **AUT-003 (advisory, blocking under --strict)**: value not in allowlist.

Data-driven from `reconciliation/authorship-fields.yaml`. Fields registered
for the architecture-framework repo (per the field shape this repo uses):

| Path | file_glob | prefix_match |
|---|---|---|
| `**Author**` | `change-requests/CR-*.md` | (default: exact) |
| `**Author:**` | `docs/ADRs/*.md` | (default: exact) |

The `**Author:**` shape is architecture-framework-specific: the ADR template
puts the colon INSIDE the bold markers (different from the standard
`**Author**:` form used in change-requests). The bounded-glob walker
prevents this from leaking into other repos' ADRs.

The per-repo `test_registry_loads_expected_fields` is also relaxed: this
repo legitimately has no `**Owner**` fields (the standard CR template
uses only `**Author**` here), and the cross-repo invariant is now
"registry must declare at least one authorship-bearing field of an
author/owner/actor family", rather than the strict "**Owner** AND
**Author**" of the 118a baseline.

## 4. CI wiring

A new workflow `.github/workflows/validate-authorship.yml` runs the gate
in `--strict` mode on every push and PR. The gate has its own per-repo
test module `tests/test_check_authorship.py` (21 tests, 21/21 pass on
the architecture-framework repo's tree).

## 5. Out of scope (CR-118c, deferred)

Prose-content occurrences of `Agent` / `Coder` / etc. in record `name` /
`definition` / `description` fields (not the authorship-metadata fields)
are inventoried for the 118c follow-on but not rewritten in this slice.

## 6. Test posture

- 21/21 `test_check_authorship` pass.
- Gate `--strict` exit 0 against the live architecture-framework tree.
- 0 D-004 violations across 4 new/modified files.

## 7. Carrier

This document. Plus the CHANGELOG `[Unreleased]` entry and the new
`.github/workflows/validate-authorship.yml` workflow.
