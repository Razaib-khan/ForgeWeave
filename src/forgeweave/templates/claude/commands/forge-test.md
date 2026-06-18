---
description: "Generate comprehensive tests for the specified file or module"
agent: primary
subtask: true
model: opencode/gpt-5.1-codex
---

# Forge Test

Generate comprehensive tests for the specified file or module.

If no file is specified, analyze all unstaged `.ts`, `.tsx`, `.py`, `.js` files and test each.

For each file, generate:
1. Unit tests covering all exported functions/classes
2. Edge case and boundary condition coverage
3. Mock external dependencies (APIs, databases, file system)
4. Integration tests if the module interacts with other modules
5. Error handling and failure mode tests

Output:
- Test file path relative to project root
- Test cases with descriptions
- Coverage targets
- `!{npm test}` or `!{pytest}` or equivalent run command

Detect the test framework from project config (Jest, Vitest, pytest, etc.).
