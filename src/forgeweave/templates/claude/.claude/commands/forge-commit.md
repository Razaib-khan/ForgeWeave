---
description: "Generate a Conventional Commits message from staged git changes"
subtask: true
model: opencode/gpt-5.1-codex
---

# Forge Commit

Analyze the staged changes and generate a Conventional Commit message.

1. Run `!{git diff --staged}` to inspect changes
2. Determine commit type from: `feat | fix | docs | style | refactor | perf | test | build | ci | chore | revert`
3. Determine scope from the modified files (e.g., `cli`, `server`, `templates`)
4. Write a concise description (50 chars max, imperative mood)
5. Add a detailed body explaining what and why (wrap at 72 chars)

Format:
```
<type>(<scope>): <description>

<optional body>
<optional footer>
```

If no changes are staged, notify the user and list unstaged files.
