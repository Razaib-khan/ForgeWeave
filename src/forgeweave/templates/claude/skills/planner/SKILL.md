---
skill_id: planner
name: Planner
version: 1.0.0
description: Converts user intent into structured execution plans, including steps, dependencies, risks, and required tools
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - planning
  - decomposition
  - workflow
---

# Planner

## Purpose

Transform vague, high-level user intent into a concrete, actionable execution plan. Breaks down complex goals into ordered steps, identifies dependencies, assesses risks, and determines which tools or agents are needed at each stage.

## When to Use

- The user says "I want to build X" or "implement Y" without specifying how
- Multiple steps are needed and the order matters
- Different parts of the task require different tools or skills
- The task has dependencies that must be resolved in sequence

## When Not to Use

- The user has already given step-by-step instructions — execute directly
- The task is a single, well-defined action (e.g., "rename this function")
- The task is purely research — use `deep-research` or `quick-research`

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `goal` | string | Yes | What the user wants to accomplish |
| `context` | string | No | Project context, constraints, or existing work |
| `available_skills` | array | No | Which skills are available for execution |

## Expected Outputs

A structured plan containing:
- Goal restatement (clarified)
- Ordered steps with dependencies
- Required tools or skills per step
- Risk assessment per step
- Estimated complexity

## Exact Workflow Steps

1. Clarify the goal by restating it and asking for confirmation if ambiguous
2. Decompose into ordered, atomic steps
3. Identify dependencies between steps (blocking, parallel, sequential)
4. Map each step to required tools, skills, or agents
5. Assess risks per step (e.g., "this step may break existing tests")
6. Present the plan for user approval before execution

## Required Checks

- [ ] Goal is clarified and unambiguous
- [ ] Steps are ordered with dependencies identified
- [ ] Each step maps to an available tool or skill
- [ ] Risks are documented

## Failure Modes

| Failure Condition | Response |
|---|---|
| Goal is too vague to decompose | Ask clarifying questions iteratively |
| No available skill covers a step | Report as uncovered and suggest creating a new skill |
| Steps have circular dependencies | Restructure to break the cycle |

## Examples

### Example: "Build a CLI tool"
Plan: 1) Choose framework (argparse/click/typer), 2) Define commands, 3) Implement each command, 4) Add tests, 5) Write README

## References

| Reference | Path |
|---|---|
| Workflow Orchestrator skill | `../workflow-orchestrator/SKILL.md` |
