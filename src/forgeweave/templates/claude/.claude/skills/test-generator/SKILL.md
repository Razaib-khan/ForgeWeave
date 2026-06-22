---
skill_id: test-generator
name: Test Generator
version: 1.0.0
description: Creates test plans and test cases (unit, integration, edge cases) based on existing or planned code
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - testing
  - quality
  - coverage
---

# Test Generator

## Purpose

Analyze existing or planned code and produce comprehensive test suites. Covers unit tests for individual functions, integration tests for module interactions, and edge case tests for boundary conditions. Detects the project's test framework automatically.

## When to Use

- New code has been written without tests
- Existing code lacks coverage in critical paths
- A bug was fixed and a regression test is needed
- The user explicitly asks for tests

## When Not to Use

- The code is prototype or throwaway
- The user asked for debugging, not testing
- The testing strategy needs architectural design first

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `target` | string | Yes | File, module, or feature to test |
| `type` | enum | No (default: all) | unit, integration, edge-case, all |
| `framework` | string | No | Test framework (auto-detected if omitted) |

## Expected Outputs

| Output | Description |
|---|---|
| Test files | New test files following project conventions |
| Coverage report | What's covered and what's not |
| Test run command | How to execute the tests |

## Exact Workflow Steps

1. Detect test framework from project config (Jest, Vitest, pytest, etc.)
2. Read the target code and identify all exported functions, classes, and behaviors
3. For each function: test happy path, error cases, edge cases (empty input, null, boundaries)
4. Create test file following existing test conventions (naming, location, patterns)
5. Mock external dependencies (APIs, databases, file system)
6. Run tests to confirm they pass

## Required Checks

- [ ] All tests pass
- [ ] Edge cases are covered (not just happy path)
- [ ] Mocks are used for external dependencies
- [ ] Tests are deterministic (no flaky tests)

## Failure Modes

| Failure Condition | Response |
|---|---|
| Test framework not detectable | Ask user to specify framework |
| Tests fail due to code bugs | Report failing tests and suggest fixes |
| Mock is too complex | Suggest integration test instead of mocked unit test |

## References

| Reference | Path |
|---|---|
| Code Builder skill | `../code-builder/SKILL.md` |
| Debugger skill | `../debugger/SKILL.md` |
