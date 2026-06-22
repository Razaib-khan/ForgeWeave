# ForgeWeave Template Instructions

This project uses ForgeWeave — a framework-agnostic agent orchestration layer.

## Key Principles

- **AGENTS.md = primary context** — global rules, auto-detection, skills, subagents. Read first.
- **Skills = logic layer** — SKILL.md + Python scripts + references. Every capability is a skill.
- **Commands = triggers** — `/forge-*` commands invoke skills or agents directly via TUI-native routing (no MCP server).
- **Playwright MCP = browser automation** — `browser_navigate`, `browser_snapshot`, etc. for web interaction.

## Lifecycle

```
User prompt → read AGENTS.md → load skills → code → build skills → commit
```

## Hooks

ForgeWeave hooks fire at each lifecycle stage:
- `pre_command` / `post_command` — around commands
- `pre_skill` / `post_skill` — around skill execution
- `pre_research` / `research_iteration` / `research_complete` / `post_research` — around research
- `pre_agent_create` / `post_agent_create` — around agent creation
- `pre_file_write` / `post_file_write` — around file modifications

Hooks only observe, validate, prepare, or finalize. They never contain business logic.
