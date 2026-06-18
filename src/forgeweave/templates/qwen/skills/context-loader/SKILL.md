---
skill_id: context-loader
name: Context Loader
version: 1.0.0
description: Reads AGENTS.md + project structure + existing skills to build an execution-aware context before any operation
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - context
  - initialization
  - project-awareness
---

# Context Loader

## Purpose

Before any operation begins, load and understand the full project context: AGENTS.md, project structure, available skills, MCP server configuration, and key files. Ensures every subsequent action is informed by the project's conventions and capabilities.

## When to Use

- Starting a new session on a ForgeWeave project
- Before running any skill or workflow that depends on project structure
- The agent needs to understand what agents and skills are available
- After `forge init` has scaffolded a new project

## When Not to Use

- The task is outside the project (e.g., general knowledge question)
- Context has already been loaded in the current session
- The task is a simple isolated operation

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `project_root` | string | No (default: cwd) | Path to project root |

## Expected Outputs

| Output | Description |
|---|---|
| Project overview | Project type, TUI, key structure |
| Available agents | List of registered agents from AGENTS.md |
| Available skills | List of skills with their purposes |
| MCP configuration | Which MCP servers are configured |
| Key files | Paths to important config files |

## Exact Workflow Steps

1. Read AGENTS.md for agent registration and configuration
2. Scan `.<tui>/skills/` for available skills and their SKILL.md descriptions
3. Read `.<tui>/opencode.json` or equivalent for MCP server config
4. Read RESEARCH_INSTRUCTIONS.md if present
5. Identify the TUI being used from the project structure
6. Compile a context summary for the agent to use

## Required Checks

- [ ] AGENTS.md was found and parsed
- [ ] Skills directory was scanned
- [ ] MCP configuration was loaded
- [ ] TUI was identified

## Failure Modes

| Failure Condition | Response |
|---|---|
| No AGENTS.md found | Report: "Not a ForgeWeave project — run forge init first" |
| Skills directory missing | Report: "No skills directory found — run forge init" |
| MCP config missing | Proceed with limited capabilities |

## References

| Reference | Path |
|---|---|
| AGENTS.md | `./AGENTS.md` |
| AGENT_SPEC.md | `./AGENT_SPEC.md` |
