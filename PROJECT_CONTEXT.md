# Project Context

**Version:** 2.0
**Last updated:** 2026-06-22
**Status:** Active

This document provides high-level architectural context for ForgeWeave. It is the reference for design decisions, supported environments, and project scope.

> **IMPORTANT:** This is the source of truth for architecture decisions. Any change to the architecture must be reflected here first.

---

## Table of Contents

- [What is ForgeWeave?](#what-is-forgeweave)
- [Architecture Overview](#architecture-overview)
- [Module Responsibilities](#module-responsibilities)
- [Data Flow](#data-flow)
- [Supported Environments (TUIs)](#supported-environments-tuis)
- [MCP Server Framework](#mcp-server-framework)
- [Design Principles](#design-principles)
- [Key Specifications](#key-specifications)
- [Project Status](#project-status)
- [Glossary](#glossary)

---

## What is ForgeWeave?

ForgeWeave is a **project scaffolding CLI** for AI agent development environments (TUIs). It is written in Python and:

1. **Initializes projects** with TUI-specific agent, command, hook, and skill scaffolding.
2. **Configures MCP servers** — Playwright and Headroom are mandatory; Firecrawl, GitHub, SQLite, Context7 are optional.
3. **Generates AGENTS.md** with dynamic markers showing which MCP servers are available.
4. **Distributes reusable skills** that encode domain expertise for coding agents.

ForgeWeave is **not** a runtime server. It generates files that the TUI consumes.

---

## Architecture Overview

```
┌─────────────────────────────────────────┐
│              forge CLI                   │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │ forge init  │  │  forge doctor    │  │
│  └──────┬──────┘  └──────────────────┘  │
│         │                                │
│         ▼                                │
│  ┌──────────────────────────────────┐    │
│  │         forgeweave.server        │    │
│  │  ┌────────────────────────────┐  │    │
│  │  │  forge_init()              │  │    │
│  │  │  ├─ Copy templates         │  │    │
│  │  │  ├─ _apply_mcp_configs()   │  │    │
│  │  │  └─ _process_agents_md()   │  │    │
│  │  └────────────────────────────┘  │    │
│  │  ┌────────────────────────────┐  │    │
│  │  │  MCP_SERVER_DEFS           │  │    │
│  │  │  6 servers defined here    │  │    │
│  │  └────────────────────────────┘  │    │
│  └──────────────────────────────────┘    │
└─────────────────────────────────────────┘
          │                      │
          ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│  TUI Config File  │   │   AGENTS.md      │
│  (JSON/YAML)      │   │   (dynamic ✓/—)  │
│  MCP server defs  │   │   tool docs      │
└──────────────────┘   └──────────────────┘
```

### Key Design Decision: No Server

ForgeWeave v1.x included a custom MCP server (`research_mcp`) with browser automation, crawling, document processing, and vector embeddings. This was removed in v2.0.0. All agent orchestration, research, and web interaction now relies on:

- **TUI-native features** (plugins, hooks, subagents)
- **Playwright MCP** for browser automation (separate npm package)
- **Headroom MCP** for context compression (separate npm package)
- **Skills** for domain expertise (loaded by the TUI)

The result is a simpler, more maintainable codebase with 4 core Python files instead of 10+.

---

## Module Responsibilities

### `cli.py` (198 lines)

CLI entry point with two commands:

| Command | Description |
|---|---|
| `forge init [--tui <name>] [--overwrite] [project_dir]` | Scaffold ForgeWeave in a project directory |
| `forge doctor` | Verify environment prerequisites |
| `forge --version` | Print version |

Interactive features:
- TUI selector (prompts if `--tui` not provided)
- Optional MCP server selection (InquirerPy confirm/secret/text prompts)
- Non-interactive mode when `sys.stdin.isatty()` is false

### `server.py` (434 lines)

Core scaffolding logic:

| Function | Purpose |
|---|---|
| `forge_init()` | Main entry: copies templates, writes MCP configs, updates AGENTS.md |
| `_apply_mcp_configs()` | Writes MCP server entries into TUI-specific config files (opencode.json, .claude/settings.json, .gemini/settings.json, qwen-extension.json) |
| `_process_agents_md()` | Updates AGENTS.md tables: ✓ for selected servers, — for unselected, "(not configured)" for unavailable tools |
| `_get_mcp_server_config()` | Generates TUI-specific MCP block format |

### MCP Server Registry

All servers defined in `MCP_SERVER_DEFS`:

| Server | Mandatory | Needs Key | Config Command |
|---|---|---|---|
| Playwright | ✅ | No | `npx @playwright/mcp@latest` |
| Headroom | ✅ | No | `npx -y headroom mcp serve` |
| Firecrawl | ❌ | Yes (`FIRECRAWL_API_KEY`) | `npx -y firecrawl-mcp` |
| GitHub | ❌ | Yes (`GITHUB_PERSONAL_ACCESS_TOKEN`) | `npx -y @anthropic/github-mcp` |
| SQLite | ❌ | No (needs db path) | `npx -y sqlite-mcp <path>` |
| Context7 | ❌ | Optional (`CONTEXT7_API_KEY`) | `npx -y context7-mcp` |

---

## Data Flow

```
User runs: forge init --tui opencode ./project

1. CLI parses arguments, detects TUI
2. (Optional) Prompts for MCP servers via InquirerPy
3. forge_init() is called with:
   - TUI name
   - Project directory
   - Selected MCP configs
4. forge_init() copies template/opencode/ to project/
5. _apply_mcp_configs() writes MCP entries to opencode.json
6. _process_agents_md() updates AGENTS.md with ✓/— markers
7. Result: fully scaffolded project with:
   - All template files (.opencode/, skills, agents, commands, hooks)
   - Configured MCP servers in TUI config
   - AGENTS.md reflecting available MCP tools
```

---

## Supported Environments (TUIs)

| TUI | Config Directory | Config File | MCP Key |
|---|---|---|---|
| OpenCode | `.opencode/` | `opencode.json` | `mcp` |
| Claude Code | `.claude/` | `settings.json` | `mcpServers` |
| Gemini CLI | `.gemini/` | `settings.json` | `mcp` |
| Qwen Code | `.qwen/` | `qwen-extension.json` | `mcpServers` |

All 4 TUIs share the same 20 skills in their template directory. The differences are:
- Config file format (JSON structure varies)
- Config file location (varies by TUI)
- Hook script language (Python for Claude/Gemini, TypeScript for OpenCode/Qwen)
- Agent/command file format (plain MD vs YAML+MD vs TOML)

---

## MCP Server Framework

### Mandatory Servers (always included)

1. **Playwright MCP** — Browser automation. Tools: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_fill_form`, `browser_take_screenshot`, etc.
2. **Headroom MCP** — Context compression. Tools: `headroom_compress`, `headroom_retrieve`, `headroom_stats`.

### Optional Servers (prompted during `forge init`)

3. **Firecrawl MCP** — Web search and scraping. Tools: `firecrawl_search`, `firecrawl_scrape`, `firecrawl_crawl`, `firecrawl_extract`.
4. **GitHub MCP** — Repository management. Tools: `github_list_issues`, `github_create_issue`, `github_search_repos`, `github_get_file`, `github_create_pr`.
5. **SQLite MCP** — Database queries. Tools: `sqlite_query`, `sqlite_execute`, `sqlite_list_tables`, `sqlite_describe_table`.
6. **Context7 MCP** — Library/framework docs lookup. Tools: `resolve-library-id`, `query-docs`.

### Configuration

Each optional server is configured via:
- A yes/no prompt for enabling
- A secret prompt for API keys (if applicable)
- A text prompt for paths (if applicable)

Configs are written to the TUI's config file in the TUI-specific format.

---

## Design Principles

- **Determinism over Creativity** — Same input → same output, always.
- **Explicit over Implicit** — Undocumented behavior does not exist.
- **Template-Driven Generation** — No hardcoded generation logic outside templates.
- **No Hidden State** — All I/O declared and logged.
- **Adapters Are Boundaries** — Business logic never leaks into TUI formats.

---

## Key Specifications

| Document | Version | Purpose |
|---|---|---|
| [SKILL_SPEC.md](./SKILL_SPEC.md) | 1.0 | Canonical format for all ForgeWeave skills |
| [AGENT_SPEC.md](./AGENT_SPEC.md) | 1.0 | Canonical format for all ForgeWeave agents |
| [ADAPTER_SPEC.md](./ADAPTER_SPEC.md) | 1.0 | TUI adapter implementation guide |
| [AGENTS.md](./AGENTS.md) | 1.0 | Project-level agent registration and configuration |

---

## Project Status

**Current version:** 2.0.0
**Status:** Stable

### Implemented

- `forge init` with interactive TUI selector and MCP prompts
- `forge doctor` environment check
- 6 MCP server definitions with config generation for 4 TUI formats
- Dynamic AGENTS.md with ✓/— markers
- 20 template skills per TUI (distributed as template files)
- Full template scaffolding (agents, commands, hooks, skills)

### Not Implemented (Future)

- `forge validate` command for SKILL.md/AGENT.md validation
- Plugin system for community-contributed template overrides
- Version migration commands for template updates

---

## Glossary

| Term | Definition |
|---|---|
| **TUI** | Terminal User Interface — coding environment (OpenCode, Claude Code, etc.) |
| **Skill** | Reusable, deterministic behavior unit defined in SKILL.md |
| **Agent** | Autonomous worker definition (AGENT.md) that invokes skills |
| **MCP** | Model Context Protocol — standardized interface for exposing tools to AI agents |
| **Adapter** | TUI-specific transformation logic (not a class; handled by template copying) |
| **Hook** | Script that runs at specific lifecycle events (pre-command, post-tool-use, etc.) |
| **Command** | TUI-native slash command (e.g., `/forge-research`) that maps to a skill workflow |
