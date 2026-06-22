---
description: "Generate or review documentation for the specified file or module"
subtask: true
model: opencode/gpt-5.1-codex
---

# Forge Docs

Generate or review documentation for the specified file or module.

## Generate Mode (new file)
For a new module, generate:
- JSDoc/PyDoc comments for all exported functions, classes, types
- A README section describing the module's purpose, API, and usage example
- Type definitions and interfaces documentation

## Review Mode (existing file)
For an existing file, review existing docs for:
- Accuracy against implementation
- Completeness (missing parameters, return types, edge cases)
- Clarity and readability
- Outdated documentation

Output format:
```
## {module name}
### {function/class name}
- Signature: ...
- Parameters: ...
- Returns: ...
- Example: ...
- Notes: ...
```
