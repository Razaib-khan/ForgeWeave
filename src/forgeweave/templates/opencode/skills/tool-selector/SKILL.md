---
skill_id: tool-selector
name: Tool Selector
version: 1.0.0
description: Determines which tools, APIs, MCP actions, or system capabilities are required for a given task
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - tools
  - selection
  - routing
---

# Tool Selector

## Purpose

Analyze a task and determine the optimal set of tools, MCP actions, APIs, and system capabilities needed to complete it. Prevents using the wrong tool for the job and ensures all required capabilities are available before execution starts.

## When to Use

- Starting a complex task that may need multiple tools
- The user asks "what tool should I use for X?"
- A skill or agent needs to determine its tooling requirements
- Before invoking the workflow-orchestrator to plan execution

## When Not to Use

- The tool is obvious from the task description
- Only one tool type is relevant (e.g., always "read" for documentation)
- The task is already executing and tools are already selected

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task_description` | string | Yes | What needs to be done |
| `available_tools` | array | Yes | Tools, MCP actions, and capabilities available |
| `constraints` | string | No | Any restrictions on tool usage |

## Expected Outputs

| Output | Description |
|---|---|
| Required tools | Ordered list of tools needed |
| Tool configuration | Parameters, permissions, or setup needed per tool |
| Missing tools | Any required capabilities not available |

## Exact Workflow Steps

1. Analyze the task to determine what operations are needed (read, write, search, execute, etc.)
2. Map each operation to the appropriate available tool
3. Verify each selected tool has the required permissions
4. Identify any gaps where no available tool covers a needed operation
5. Return the tool list with ordering suggestions

## Required Checks

- [ ] Every required operation has a corresponding tool
- [ ] Selected tools have necessary permissions
- [ ] No tool is selected for operations it cannot perform

## Failure Modes

| Failure Condition | Response |
|---|---|
| No tool available for a needed operation | Report gap and suggest creating a new tool |
| Tool permissions insufficient | Report what permissions need to be added |
| Task is too vague to analyze | Ask clarifying questions |

## References

| Reference | Path |
|---|---|
| MCP Schema (12 forge.* tools) | `./MCP-SCHEMA.md` |
| Available Tools (full registry) | `./forgeweave/Templates/<tui>/skills/tool-selector/references/available-tools.md` |
| Workflow Orchestrator skill | `../workflow-orchestrator/SKILL.md` |
