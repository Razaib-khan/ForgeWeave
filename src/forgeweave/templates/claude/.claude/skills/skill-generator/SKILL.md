---
skill_id: skill-generator
name: Skill Generator
version: 1.0.0
description: Meta-skill that creates new SKILL.md files from research outputs and patterns discovered in execution
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - meta
  - authoring
  - generation
---

# Skill Generator

## Purpose

Analyze execution patterns, research findings, or user workflows and distill them into reusable ForgeWeave skills. Identifies repeatable jobs, extracts the workflow steps, and produces a complete SKILL.md bundle with scripts, references, and evals.

## When to Use

- A workflow has been repeated 2+ times manually
- Research findings reveal a repeatable process that should be codified
- An ad-hoc process in a session should become a reusable skill
- The user says "we should make this a skill"

## When Not to Use

- The workflow is a one-time task — skip
- The workflow requires no agent judgment (use a regular script)
- Creating a skill for an existing skill (use the `skill-authoring` skill instead)

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `source` | string | Yes | Description of the repeatable job or path to research output |
| `name` | string | Yes | Desired skill name (kebab-case) |
| `workflow_steps` | array | No | Existing workflow notes if available |

## Expected Outputs

| Output | Description |
|---|---|
| SKILL.md | Complete skill bundle following the 10-section format |
| scripts/ | Deterministic steps extracted from the workflow |
| evals/ | Validation tests for the skill |
| references/ | Supporting documentation |

## Exact Workflow Steps

1. Analyze the source workflow or research to identify the repeatable job
2. Scope: one job per skill, max 3 use cases
3. Write SKILL.md with all 10 sections in order
4. Extract deterministic steps into standalone scripts
5. Create eval tests for happy path and failure modes
6. Validate: bundle structure, frontmatter, section order, scripts exist

## Required Checks

- [ ] Skill covers exactly one repeatable job
- [ ] SKILL.md has all 10 sections in order
- [ ] All referenced scripts exist
- [ ] At least one eval covers the happy path

## Failure Modes

| Failure Condition | Response |
|---|---|
| Source workflow is too broad | Narrow to one repeatable job |
| No deterministic steps found | Skill is fine with SKILL.md only |
| Validation fails | Fix issues and regenerate |

## Examples

### Example: Generate a skill from research output
1. Research on "Next.js 16 caching APIs" reveals a repeatable pattern
2. Name: `nextjs-caching`
3. SKILL.md captures: purpose, workflow steps for analyzing caching configs, inputs
4. evals/ test the skill against known Next.js 16 patterns

## References

| Reference | Path |
|---|---|
| Skill Authoring skill | `../skill-authoring/SKILL.md` |
| SKILL_SPEC.md | `./SKILL_SPEC.md` |
