---
description: "Review staged or specified files for code quality, security, and performance issues"
agent: primary
subtask: false
model: opencode/gpt-5.1-codex
---

# Forge Review

Review the staged changes (or specified files) for:
- Code quality issues
- Potential bugs
- Security vulnerabilities
- Performance concerns
- Edge cases and error handling
- Documentation completeness

Format output as a structured checklist with severity levels:

```
[CRITICAL] Issue with explanation and fix suggestion
[HIGH] Issue with explanation
[MEDIUM] Issue with explanation
[LOW] Suggestion with explanation
```

Provide specific remediation suggestions with code examples where applicable.
