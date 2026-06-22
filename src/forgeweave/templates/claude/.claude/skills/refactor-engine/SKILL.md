---
skill_id: refactor-engine
name: Refactor Engine
version: 1.0.0
description: Improves existing codebases by restructuring for clarity, performance, and maintainability without changing external behavior
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - refactoring
  - cleanup
  - optimization
---

# Refactor Engine

## Purpose

Restructure existing code to improve readability, performance, and maintainability while preserving exact external behavior. Every refactor is verified by ensuring existing tests continue to pass and no observable behavior changes.

## When to Use

- Code has duplicated logic that should be extracted
- A function or module is too long or does too many things
- Naming is unclear or inconsistent with project conventions
- Performance can be improved by algorithmic changes
- Dead code, commented-out code, or unused imports need removal

## When Not to Use

- The code has a bug — use `debugger` first
- New features need to be added — use `code-builder`
- The code works fine and doesn't need changes

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `target` | string | Yes | File, module, or code area to refactor |
| `goal` | enum | Yes | clarity, performance, maintainability, or all |
| `constraints` | string | No | What must NOT change (public API, performance bounds) |

## Expected Outputs

| Output | Description |
|---|---|
| Refactored code | Restructured code preserving external behavior |
| Diff summary | What changed and why |
| Verification | Test results confirming no behavior change |

## Exact Workflow Steps

1. Read and understand the target code fully
2. Run existing tests to establish baseline
3. Identify refactoring opportunities (duplication, complexity, naming)
4. Apply one refactoring at a time (small, atomic changes)
5. Run tests after each change to confirm no regression
6. Repeat until all planned refactorings are applied

## Required Checks

- [ ] All existing tests pass before and after
- [ ] No public API changed unless explicitly requested
- [ ] Each change is atomic (one concern per change)
- [ ] No dead code or debug artifacts left behind

## Failure Modes

| Failure Condition | Response |
|---|---|
| Test fails after refactor | Revert last change and re-approach differently |
| Refactor touches too many files | Break into smaller, focused refactors |
| Goal is unclear | Ask for specific examples of what to improve |

## References

| Reference | Path |
|---|---|
| Test Generator skill | `../test-generator/SKILL.md` |
| Code Builder skill | `../code-builder/SKILL.md` |
