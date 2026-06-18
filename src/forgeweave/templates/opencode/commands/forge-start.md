---
description: "Complete overview of the ForgeWeave framework — read this first when starting work"
agent: primary
subtask: false
---

# ForgeWeave Framework Overview

Run `/forge-start` at the beginning of every session to load this context.

## What is ForgeWeave?

ForgeWeave is a framework-agnostic agent orchestration layer. Ships as Python package `forgeweave` with CLI (`forge`) and TUI-specific templates.

## Architecture

```
forgeweave/                 # Python package + Templates
├── forge-mcp/              # Control Plane (12 forge.* tools)
├── research-mcp/           # Data Plane (10 research_* tools, internal)
└── Templates/
    ├── opencode/           # agents/, commands/, hooks/, skills/
    ├── claude/
    ├── qwen/
    └── gemini/
```

## CLI Commands

| Command | Purpose |
|---|---|
| `forge init --tui <name>` | Scaffold project for OpenCode/Claude/Qwen/Gemini |
| `forge doctor` | Check Python 3.14+, templates |
| `forge mcp` | Start ForgeWeave MCP server (stdio) |

## Key Files

| File | Purpose |
|---|---|
| `AGENTS.md` | Agent registration & discovery |
| `MCP-SCHEMA.md` | JSON contracts for all 12 forge.* tools |
| `TEMPLATE_INSTRUCTIONS.md` | Agent instructions |
| `research/` | All research output (gitignored) |

## Design Principle

**Expose capabilities. Hide orchestration.**
- MCP tools are a thin execution interface
- Skills are the logic layer
- Agents are internal workers
- Commands are triggers

## Deep Research

Run `/forge-research <topic>` which calls `forge.research` — a single tool that
internally runs the full 5-stage pipeline. Pipeline stages are implementation details.

## ForgeWeave MCP Tools

| Tool | Category | Purpose |
|---|---|---|
| `forge.init` | Setup | Initialize ForgeWeave in a project |
| `forge.execute_command` | Routing | Route `/forge-*` commands |
| `forge.execute_skill` | Execution | Execute a skill by name |
| `forge.create_agent` | Generation | Create agent definition file |
| `forge.research` | Pipeline | Full deep-research pipeline |
| `forge.search` | Lookup | Lightweight web lookup |
| `forge.load_context` | Introspection | Load project state snapshot |
| `forge.validate` | Quality | Validate outputs against rules |
| `forge.memory_read` | Persistence | Read from memory |
| `forge.memory_write` | Persistence | Write to memory |
| `forge.status` | Meta | Poll job status |
| `forge.capabilities` | Meta | List available tools and skills |

## Hooks

ForgeWeave hooks fire at each lifecycle stage. They observe, validate, prepare, or finalize — never contain business logic.

| Hook | When it fires |
|---|---|
| `pre_command` | Before any /forge-* command |
| `post_command` | After a command completes |
| `pre_skill` | Before a skill executes |
| `post_skill` | After a skill completes |
| `pre_research` | Before deep research starts |
| `research_iteration` | After each research cycle |
| `research_complete` | When research finishes |
| `post_research` | After output is written |
| `pre_agent_create` | Before agent file creation |
| `post_agent_create` | After agent file creation |
| `pre_file_write` | Before any file modification |
| `post_file_write` | After any file modification |

## Standards

- Python 3.14+ required
- Skills: `skills/<name>/` with SKILL.md + scripts/ + references/ + evals/
- `forge init` copies Templates/<tui>/ → project via copytree
- Skills follow the 10-section SKILL.md format
