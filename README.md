# ForgeWeave

Agent orchestration framework — project scaffolding, template distribution, and AGENTS.md global rules.

`pip install forgeweave` or `uv add forgeweave`

## Quick Start

```bash
# Initialize a ForgeWeave project
forge init --tui opencode ./my-project
cd my-project

# Check your setup
forge doctor
```

## Architecture

ForgeWeave is a scaffolding tool — **Templates + Rules + Skills. No server.**

```
forge init    → Copies TUI-specific templates into your project
              → Configures MCP servers (Playwright, Headroom, Firecrawl, etc.)
              → Generates AGENTS.md with dynamic MCP availability markers
forge doctor  → Verifies environment prerequisites
```

### What `forge init` generates

| Component | Description |
|---|---|
| **AGENTS.md** | Global behavioral rules for all coding agents, dynamically marking which MCP servers are available |
| **Skills** | 20+ domain-specific skill bundles (deep-research, playwright-mcp, skill-builder, etc.) |
| **Commands** | 8 predefined `/forge-*` commands (forge-start, forge-research, forge-search, etc.) |
| **Agents** | Worker definitions for autonomous sub-agents (research pipeline, code review, etc.) |
| **Hooks** | Lifecycle hooks for TUI-native orchestration |
| **MCP configs** | Pre-configured Playwright (mandatory), Headroom (mandatory), and optional servers (Firecrawl, GitHub, SQLite, Context7) |

### Supported TUIs

- **OpenCode** — `.opencode/` directory, JSON config
- **Claude Code** — `.claude/` directory, JSON settings
- **Gemini CLI** — `.gemini/` directory, JSON settings
- **Qwen Code** — `.qwen/` directory, extension JSON

## Design

- **Determinism** — Same input always produces the same output
- **Template-driven** — All scaffolding comes from versioned templates
- **No hidden state** — All I/O is declared and logged
- **Adapters are boundaries** — Business logic never leaks into TUI formats

## License

MIT
