---
skill_id: memory-manager
name: Memory Manager
version: 1.0.0
description: Handles local persistence of research outputs, intermediate reasoning, and reusable knowledge chunks
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - memory
  - persistence
  - cache
---

# Memory Manager

## Purpose

Persist and retrieve structured data across sessions — research outputs, intermediate reasoning steps, reusable knowledge chunks, and cache entries. Prevents redundant work by reusing previously computed results when inputs match.

## When to Use

- Research results should be saved for future reference
- Intermediate reasoning needs to be persisted for multi-step workflows
- Previously computed results can be reused instead of recomputed
- Debug or trace information needs to be logged

## When Not to Use

- The data is ephemeral and only needed for the current response
- The data contains secrets or credentials (use secure storage instead)
- The storage would exceed reasonable size limits

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `operation` | enum | Yes | save, load, search, clear |
| `key` | string | Depends | Unique key for the data |
| `data` | object | For save | The data to persist |
| `namespace` | string | No (default: general) | Category for the data |

## Expected Outputs

| Output | Description |
|---|---|
| Operation result | Success with location, or loaded data, or search results |

## Exact Workflow Steps

1. Determine the persistence location based on namespace and TUI
2. For save: serialize data to disk at `research/` or `.<tui>/memory/`
3. For load: deserialize data from its persisted location
4. For search: scan persisted data for matching keys or content
5. For clear: remove caches and temporary data

## Required Checks

- [ ] Saved data is retrievable with the correct key
- [ ] Cache entries have expiration or size limits
- [ ] No sensitive data is persisted without warning

## Failure Modes

| Failure Condition | Response |
|---|---|
| Key not found on load | Report "not found" |
| Storage full | Suggest clearing old entries |
| Serialization fails | Report the unsupported type |

## References

| Reference | Path |
|---|---|
| Cache & Store skill | `../cache-store/SKILL.md` |
| research/ directory | `./research/` |
