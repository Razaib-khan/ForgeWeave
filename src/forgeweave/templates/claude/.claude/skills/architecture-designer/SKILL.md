---
skill_id: architecture-designer
name: Architecture Designer
version: 1.0.0
description: Designs system-level structures including modules, services, data flow, and scaling strategy before implementation begins
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - architecture
  - design
  - planning
---

# Architecture Designer

## Purpose

Design system-level architecture before any code is written. Produces module boundaries, service decomposition, data flow diagrams, and scaling strategy. Ensures the architecture is coherent, testable, and aligned with project constraints.

## When to Use

- Starting a new project or major subsystem
- The current architecture cannot support upcoming requirements
- Performance, scalability, or reliability concerns need addressing at the architectural level
- Multiple services or modules need to be designed together

## When Not to Use

- The change is contained within a single module — use `planner` + `code-builder`
- The user just needs a quick code pattern — not architectural design
- The architecture is already documented and just needs implementation

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `requirements` | string | Yes | Functional and non-functional requirements |
| `constraints` | string | No | Technical, organizational, or timeline constraints |
| `existing_architecture` | string | No | Description of existing system if extending it |

## Expected Outputs

| Output | Description |
|---|---|
| Module decomposition | List of modules with responsibilities |
| Data flow | How data moves between modules and external systems |
| Scaling strategy | How the system handles growth |
| Technology decisions | Key tech choices with rationale |

## Exact Workflow Steps

1. Understand requirements and constraints thoroughly
2. Identify bounded contexts and module boundaries
3. Define interfaces and data flow between modules
4. Design for failure: error handling, retries, fallbacks
5. Plan scaling strategy (horizontal vs vertical, caching, sharding)
6. Document technology decisions with alternatives considered
7. Review with planner to create execution plan

## Required Checks

- [ ] Every requirement is addressed by the architecture
- [ ] Module boundaries are clear and non-overlapping
- [ ] Data flow is documented with direction and format
- [ ] Failure modes are identified per module

## Failure Modes

| Failure Condition | Response |
|---|---|
| Requirements are too vague | Ask clarifying questions before designing |
| Architecture contradicts existing system | Document trade-offs and seek user input |
| Too many modules for scope | Consolidate into coarser boundaries |

## References

| Reference | Path |
|---|---|
| Planner skill | `../planner/SKILL.md` |
| Code Builder skill | `../code-builder/SKILL.md` |
