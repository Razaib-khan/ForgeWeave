---
skill_id: debugger
name: Debugger
version: 1.0.0
description: Systematic issue diagnosis skill that isolates root causes, tests hypotheses, and produces minimal fix strategies
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - debugging
  - diagnosis
  - troubleshooting
---

# Debugger

## Purpose

Apply systematic debugging methodology to identify root causes of software issues. Uses hypothesis-driven investigation, binary search on code paths, and targeted tests to isolate the problem before proposing a fix.

## When to Use

- The user reports a bug, error, or unexpected behavior
- A test is failing and the cause is not obvious
- A feature works locally but fails in production
- Performance regression needs investigation

## When Not to Use

- The error message is self-explanatory — fix it directly
- The fix is already known and just needs implementation
- The task is refactoring — use `refactor-engine`

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `symptom` | string | Yes | The observed error or unexpected behavior |
| `reproduction_steps` | string | No | Steps to reproduce the issue |
| `environment` | string | No | Environment details (OS, versions, deployment) |
| `logs_or_stacktrace` | string | No | Error output, logs, or stack trace |

## Expected Outputs

| Output | Description |
|---|---|
| Root cause | Identified source of the issue |
| Fix strategy | Minimal change to fix the issue |
| Verification steps | How to confirm the fix works |
| Prevention | How to avoid similar issues |

## Exact Workflow Steps

1. Understand the symptom and reproduction steps
2. Formulate 2-3 hypotheses for root cause
3. For each hypothesis, design a diagnostic test
4. Narrow down by eliminating hypotheses
5. Isolate the exact root cause
6. Design minimal fix that doesn't break other functionality
7. Verify fix resolves the symptom
8. Run existing tests to confirm no regressions

## Required Checks

- [ ] Root cause is identified before any fix is proposed
- [ ] Fix is minimal (no scope creep)
- [ ] Existing tests pass after fix
- [ ] Prevention strategy is documented

## Failure Modes

| Failure Condition | Response |
|---|---|
| Cannot reproduce the issue | Ask for more detailed reproduction steps |
| All hypotheses eliminated | Broaden search to adjacent systems or dependencies |
| Fix breaks other functionality | Revert and explore alternative fix strategy |

## Examples

### Example: "API returns 500 intermittently"
1. Hypotheses: database connection pool exhaustion, unhandled exception, timeout
2. Check connection pool metrics → pool is fine
3. Add error logging around the failing endpoint → caught unhandled promise rejection
4. Fix: wrap async handler in try/catch

## References

| Reference | Path |
|---|---|
| Test Generator skill | `../test-generator/SKILL.md` |
