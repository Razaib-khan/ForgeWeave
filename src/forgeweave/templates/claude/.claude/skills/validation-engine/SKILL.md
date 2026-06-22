---
skill_id: validation-engine
name: Validation Engine
version: 1.0.0
description: Checks outputs from other skills for consistency, correctness, and adherence to AGENTS.md rules
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - validation
  - quality
  - review
---

# Validation Engine

## Purpose

Systematically inspect outputs from any skill or agent for correctness, consistency, completeness, and compliance with project rules defined in AGENTS.md. Acts as a quality gate before outputs are presented to the user or used by downstream skills.

## When to Use

- After any skill produces output that needs quality assurance
- Before presenting research results to the user
- When cross-checking claims across multiple sources
- After code generation, before presenting the code

## When Not to Use

- The output is trivial and doesn't need validation
- The user is iterating quickly and doesn't want validation overhead
- The output is an intermediate step that will be further processed

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `output` | string | Yes | The content to validate |
| `type` | enum | Yes | research, code, documentation, plan |
| `rules` | array | No | Specific rules to enforce (defaults from AGENTS.md) |

## Expected Outputs

| Output | Description |
|---|---|
| Validation report | Pass/fail per rule, with details |
| Issues found | List of problems with severity and location |
| Suggestions | How to fix each issue |

## Exact Workflow Steps

1. Load validation rules from AGENTS.md and the specific skill's requirements
2. For research: check every claim has a source URL, flag contradictions, check no blog sources
3. For code: check syntax, check against project conventions, verify tests pass
4. For documentation: check completeness, accuracy, clarity
5. For plans: check steps are ordered, dependencies identified, risks documented
6. Compile validation report with pass/fail per rule

## Required Checks

- [ ] All required fields are present in the output
- [ ] No contradictions across the output
- [ ] Output follows applicable rules from AGENTS.md
- [ ] All claims are traceable to sources

## Failure Modes

| Failure Condition | Response |
|---|---|
| Validation rules are ambiguous | Ask for clarification |
| Output fails critical rules | Reject and report specific failures |
| Output fails minor rules | Accept with warnings |

## References

| Reference | Path |
|---|---|
| AGENTS.md | `./AGENTS.md` |
| Internal validator component | Used by the deep-research skill pipeline |
