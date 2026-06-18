# ForgeWeave

Framework-agnostic agent orchestration layer — **12 forge.\* MCP tools**.

`pip install forgeweave` or `uv add forgeweave`

## Quick Start

```bash
# Initialize a project
forge init --tui opencode ./my-project
cd my-project

# Start the MCP server
forge mcp

# Check your setup
forge doctor
```

## Design

```
MCP = thin execution interface (12 forge.* tools)
Skills = logic layer (SKILL.md + scripts)
Agents = internal workers (never directly invoked)
Commands = triggers (/forge-* routes through registry)
```

**Expose capabilities. Hide orchestration.**

## The 12 Tools

| Tool | Purpose |
|---|---|
| `forge.init` | Initialize ForgeWeave in a project |
| `forge.execute_command` | Route /forge-* commands |
| `forge.execute_skill` | Execute a skill by name |
| `forge.create_agent` | Create agent definition file |
| `forge.research` | Full deep-research pipeline |
| `forge.search` | Lightweight web lookup |
| `forge.load_context` | Load project state snapshot |
| `forge.validate` | Validate outputs against rules |
| `forge.memory_read` | Read from persistent SQLite |
| `forge.memory_write` | Write to persistent SQLite |
| `forge.status` | Poll job status |
| `forge.capabilities` | List available tools and skills |

## Hooks

12 lifecycle hooks: pre/post command, pre/post skill, pre/post research,
research_iteration, research_complete, pre/post agent_create, pre/post file_write.

Hooks observe, validate, prepare, or finalize — they never contain business logic.

## License

MIT
