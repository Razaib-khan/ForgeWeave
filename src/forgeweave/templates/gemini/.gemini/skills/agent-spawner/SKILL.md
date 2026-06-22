---
skill_id: agent-spawner
name: Agent Spawner
version: 1.0.0
description: Creates and configures subagents dynamically with defined roles, constraints, and tool permissions
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - agents
  - subagents
  - spawning
---

# Agent Spawner

## Purpose

Dynamically create and configure sub-agents for specific tasks. Each spawned agent gets a defined role, constraints, tool permissions, and a task-specific prompt. Enables the multi-agent patterns used in deep-research and workflow-orchestrator.

## When to Use

- A multi-agent pipeline needs to be executed (e.g., deep-research)
- A task requires a specialized agent with specific permissions
- Parallel execution of independent subtasks is needed
- An agent needs to be sandboxed with restricted capabilities

## When Not to Use

- The task is simple enough for a single agent
- The user explicitly asked for a single-agent approach
- The overhead of spawning a sub-agent exceeds the complexity of the task

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task` | string | Yes | What the sub-agent should do |
| `role` | string | Yes | The sub-agent's role (e.g., "researcher", "validator") |
| `constraints` | array | No | Rules the sub-agent must follow |
| `permissions` | object | No | Tool permissions for the sub-agent |

## Expected Outputs

| Output | Description |
|---|---|
| Spawned agent | A configured sub-agent ready to execute |
| Agent manifest | The agent's instructions and constraints |

## Exact Workflow Steps

1. Define the agent's role based on the task requirements
2. Set constraints: what the agent MUST and MUST NOT do
3. Set permissions: which tools the agent can use
4. Write the agent's instructions prompt
5. Spawn the agent using the TUI's sub-agent mechanism
6. Monitor execution for constraint violations

## Required Checks

- [ ] Agent has a clearly defined role
- [ ] Constraints are explicit and enforceable
- [ ] Permissions match the task requirements
- [ ] Agent instructions are self-contained

## Failure Modes

| Failure Condition | Response |
|---|---|
| Permission mismatch | Adjust permissions to match the task |
| Agent goes out of scope | Enforce constraints and restart |
| Sub-agent mechanism unavailable | Execute the task directly with a prompt template |

## References

| Reference | Path |
|---|---|
| Agent Spec | `./AGENT_SPEC.md` |
| AGENTS.md | `./AGENTS.md` |
| Deep Research skill | `../deep-research/SKILL.md` |
