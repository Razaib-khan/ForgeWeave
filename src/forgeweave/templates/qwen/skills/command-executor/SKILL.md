---
skill_id: command-executor
name: Command Executor
version: 1.0.0
description: Routes /forge-* commands through the command registry to skills and agents via forge.execute_command
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - commands
  - execution
  - routing
---

# Command Executor

## Purpose

Receive a slash command from the user (e.g., `/forge-start`, `/forge-research`), route it through `forge.execute_command`, which resolves it to a skill or agent workflow via the command registry, and returns the result.

## When to Use

- A user invokes a `/forge-*` command
- A command needs argument parsing and routing
- Pre/post hooks need to fire around command execution

## When Not to Use

- The user's request is a natural language question, not a command
- The action is trivial (e.g., "list files") — execute directly

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `command` | string | Yes | The full command string including arguments |
| `registry` | object | Yes | Command registry mapping names → handlers |

## How Routing Works

1. `pre_command` hook fires — loads context, validates command exists
2. `forge.execute_command` called with command name + args
3. Tool reads command registry (`.forge/command_registry.json`)
4. Resolves command to a skill pipeline or agent workflow
5. `forge.execute_skill` called if the command maps to a skill
6. `post_command` hook fires — logs result, updates memory

## Command Registry Schema

```json
{
  "version": "1.0.0",
  "commands": {
    "forge-start": {
      "description": "Start a new feature/component",
      "handler": "skill",
      "skill": "code-builder",
      "hooks": ["pre_command", "post_command"]
    },
    "forge-research": {
      "description": "Execute deep research pipeline",
      "handler": "tool",
      "tool": "forge.research",
      "hooks": ["pre_command", "post_command"]
    },
    "forge-review": {
      "description": "Review staged changes",
      "handler": "skill",
      "skill": "validation-engine",
      "hooks": ["pre_command", "post_command"]
    },
    "forge-commit": {
      "description": "Commit with forge context",
      "handler": "bash",
      "script": "git commit",
      "hooks": ["pre_command", "post_command"]
    },
    "forge-test": {
      "description": "Run tests with forge wrappers",
      "handler": "bash",
      "script": "pytest",
      "hooks": ["pre_command", "post_command"]
    },
    "forge-docs": {
      "description": "Generate documentation",
      "handler": "skill",
      "skill": "agent-spawner",
      "hooks": ["pre_command", "post_command"]
    }
  }
}
```

## Required Checks

- [ ] Command is recognized and registered
- [ ] Arguments are valid for the command
- [ ] Handler executes without error
- [ ] Pre/post hooks fire correctly
- [ ] Results are reported to the user

## Failure Modes

| Failure Condition | Response |
|---|---|
| Command not found | Report available commands from registry |
| Invalid arguments | Show usage for the command |
| Handler fails | Report the error with context |
| Hook blocks execution | Report hook reason to user |

## References

| Reference | Path |
|---|---|
| Command registry schema | `./MCP-SCHEMA.md` (forge.execute_command) |
| Workflow Orchestrator skill | `../workflow-orchestrator/SKILL.md` |
| Forge hooks | `./hooks/` (TUI-specific) |
