---
skill_id: code-builder
name: Code Builder
version: 1.0.0
description: Translates plans into working code structures with architecture decisions, folder layout, and implementation strategy
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - coding
  - implementation
  - scaffolding
---

# Code Builder

## Purpose

Take a structured plan and produce working, well-organized code. Makes architecture decisions (framework choice, folder structure, module boundaries), generates the code, and verifies it compiles or passes basic checks.

## When to Use

- A `planner` skill has produced an execution plan
- The user asks to "implement" or "build" a feature from requirements
- Scaffolding a new module, component, or service
- Translating architecture decisions into concrete code

## When Not to Use

- The code change is a simple rename or refactor — use `refactor-engine`
- Only tests are needed — use `test-generator`
- The task is debugging an existing issue — use `debugger`

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `plan` | object | Yes | The execution plan from the planner skill |
| `existing_code` | string | No | Description of existing codebase structure |
| `standards` | array | No | Coding standards to follow (e.g., TypeScript strict, PEP 8) |

## Expected Outputs

| Output | Description |
|---|---|
| New or modified files | Working code implementing the plan |
| Folder structure | Organized module layout |
| Architecture notes | Key decisions made during implementation |

## Exact Workflow Steps

1. Review the plan and understand the architecture
2. Create folder structure matching project conventions
3. Implement each module following existing patterns
4. Add type annotations and documentation as code is written
5. Verify the code compiles or passes syntax checks
6. Run existing tests to confirm no regressions

## Required Checks

- [ ] Code compiles without errors
- [ ] Existing tests still pass
- [ ] Code follows project conventions (naming, imports, formatting)
- [ ] New exports are properly typed

## Failure Modes

| Failure Condition | Response |
|---|---|
| Code doesn't compile | Fix type errors and re-verify |
| Existing tests fail | Identify root cause and fix before continuing |
| Architecture decision contradicts plan | Flag to planner for resolution |

## References

| Reference | Path |
|---|---|
| Planner skill | `../planner/SKILL.md` |
| Test Generator skill | `../test-generator/SKILL.md` |
