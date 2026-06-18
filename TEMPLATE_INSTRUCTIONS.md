# ForgeWeave Template Instructions

This project uses ForgeWeave — a framework-agnostic agent orchestration layer.

## Key Principles

- **MCP = thin execution interface** — forge.* tools trigger pipelines, load skills, manage state. They never contain business logic.
- **Skills = logic layer** — SKILL.md + Python scripts + references. Every capability is a skill.
- **Agents = workers** — Internal pipeline components. Never called directly by the user.
- **Commands = triggers** — `/forge-*` commands route through `forge.execute_command` to skills/agents.

## Available Tools

All 12 forge.* tools are available via the forge-mcp server. Data-plane tools (research_*) are used internally by skills.

## Lifecycle

```
User prompt → forge.execute_command → pre_command hook → skill/agent → post_command hook → result
```

## Hooks

ForgeWeave hooks fire at each lifecycle stage:
- `pre_command` / `post_command` — around commands
- `pre_skill` / `post_skill` — around skill execution
- `pre_research` / `research_iteration` / `research_complete` / `post_research` — around research
- `pre_agent_create` / `post_agent_create` — around agent creation
- `pre_file_write` / `post_file_write` — around file modifications

Hooks only observe, validate, prepare, or finalize. They never contain business logic.
