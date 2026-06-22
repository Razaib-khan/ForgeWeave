---
description: "Quick single-search via websearch tool: lightweight web lookup for when context is missing"
subtask: false
---

# Forge Search

Triggers the `websearch` tool for lightweight on-demand web searches. Use this when you need a quick answer about an API, error, library, or configuration detail — not a full research pipeline.

## Usage: `/forge-search <query> [--max=<1-10>] [--source=<domain.com>]`

## When to Use

- You don't know a specific API parameter, function signature, or import path
- You encounter an error message you haven't seen before
- You need a quick code example for a specific method
- You need to confirm a library version, feature flag, or deprecation
- You need to verify a CLI flag or configuration option
- You are about to write code with an unfamiliar library — **stop and search first**

## When NOT to Use

- The question requires comparing 3+ sources or understanding a new framework — use `/forge-research`
- The information is in the local codebase — search the codebase directly
- The user asked for a comprehensive report — use `/forge-research`

## Behavior

1. Calls `websearch` with the query and options
2. Returns top results with extracted content from each source
3. Results are synchronous — no polling needed

## Examples

```
/forge-search next.js 16 cacheLife default profile
/forge-search python 3.14 match statement syntax
/forge-search playwright mcp browser_snapshot --source=playwright.dev
/forge-search react 19 useActionState signature --max=3
```
