---
description: "Context launcher — load AGENTS.md for full framework rules, then use this as a quick-reference guide"
agent: build
subtask: false
---

# /forge-start — Context Launcher

> **AGENTS.md is the primary context source.** If you haven't read it yet, read it now. This file is a quick-reference supplement.

## Available Commands

| Command | Purpose |
|---|---|
| `forge init --tui <name>` | Scaffold project for OpenCode/Claude/Qwen/Gemini |
| `forge doctor` | Check Python 3.14+, templates, dependencies |
| `/forge-search <query>` | Single web search — quick API lookups, error fixes |
| `/forge-research <topic>` | 6-stage deep research pipeline → report + skill |

## Key Files

| File | Purpose |
|---|---|
| `AGENTS.md` | **Primary context** — global rules, auto-detection, skills, subagents |
| `skills/<name>/SKILL.md` | Domain expertise — load when task matches skill trigger |
| `research/` | Research output (gitignored) |

## Available Skills

| Skill | Use When... |
|---|---|
| `skill-builder` | Creating or improving any skill |
| `playwright-mcp` | Browser automation, JS pages |
| `deep-research` | Comprehensive multi-source research |
| `web-research` | Fetching URLs for clean content |
| `quick-research` | Simple factual questions |
| `architecture-designer` | System design decisions |
| `code-builder` | Scaffolding new modules |
| `test-generator` | Writing tests |
| `refactor-engine` | Code improvement |
| `debugger` | Debugging methodology |
| `validation-engine` | Quality assurance |

## Standards

- Python 3.14+ required
- `forge init` copies templates into project
- Skills follow SKILL.md + scripts/ + references/ + evals/ layout
