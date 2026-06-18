---
skill_id: workflow-orchestrator
name: Workflow Orchestrator
version: 1.0.0
description: Coordinates multi-skill execution pipelines (e.g., research → plan → build → test)
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - orchestration
  - pipeline
  - workflow
---

# Workflow Orchestrator

## Purpose

Coordinate the execution of multiple skills in sequence or parallel to achieve a complex goal. Handles dependency resolution, data passing between skills, error recovery, and progress reporting. The top-level orchestrator that makes multi-step agentic workflows reliable.

## When to Use

- A complex goal requires 3+ skills in sequence (e.g., research → plan → build → test)
- Multiple independent subtasks can run in parallel
- A pipeline needs retry logic or error recovery
- The user wants a multi-step workflow executed end-to-end

## When Not to Use

- Only one skill is needed — invoke it directly
- The steps are manual and need user approval at each stage
- The workflow is a simple linear script — use a script instead

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `goal` | string | Yes | The overall objective |
| `pipeline_definition` | array | No | Explicit skill order if known (auto-generated if omitted) |
| `fallback_strategy` | enum | No (default: stop) | stop, retry, skip |

## Expected Outputs

| Output | Description |
|---|---|
| Pipeline result | The output of the final skill |
| Execution trace | What ran, in what order, what each produced |
| Status report | Success, failures, and retries |

## Exact Workflow Steps

1. Accept the goal from the user or from a command
2. Decompose the goal into ordered skills using `planner` skill
3. Identify dependencies between skills (blocking, parallel, sequential)
4. Execute skills in dependency order:
   - Parallel skills run concurrently
   - Sequential skills run in order, passing outputs
5. After each skill, validate output using `validation-engine`
6. On failure: retry, skip, or stop based on fallback strategy
7. Report results to user with execution trace

## Required Checks

- [ ] All skills in the pipeline are available
- [ ] Dependency order is correct (no cycles)
- [ ] Each skill's output is valid before passing to next
- [ ] Fallback strategy is defined for every pipeline step

## Failure Modes

| Failure Condition | Response |
|---|---|
| Required skill not available | Report missing skill and suggest alternatives |
| Pipeline step fails after retries | Report failure with partial results |
| Circular dependency detected | Restructure to eliminate the cycle |

## Examples

### Example: Feature development pipeline
1. planner → decompose: code design, implement, test, document
2. architecture-designer → design module structure
3. code-builder → implement (depends on architecture-designer)
4. test-generator → create tests (parallel with docs)
5. validation-engine → validate all outputs
6. Report results

## References

| Reference | Path |
|---|---|
| Planner skill | `../planner/SKILL.md` |
| Validation Engine skill | `../validation-engine/SKILL.md` |
| Command Executor skill | `../command-executor/SKILL.md` |
