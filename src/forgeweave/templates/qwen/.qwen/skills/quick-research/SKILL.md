---
skill_id: quick-research
name: Single Search
version: 2.0.0
description: |
  Lightweight single-pass search for fast answers when context is missing. Use this skill whenever the agent needs to: look up an API signature, verify a library version, check a CLI flag, find a code example, research an error message, or confirm a configuration option. Triggers automatically when you are about to write code with an unfamiliar library or encounter a gap in context. NOT for comprehensive research — use deep-research for that.
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - search
  - lookup
  - quick
  - reference
---

# Single Search

## Purpose

Get fast, focused answers by crawling a small set of authoritative URLs and extracting the relevant information. No multi-agent pipeline, no planning phase, no validation stage. This is the default research mode — use it whenever you lack context about any technology.

## When to Use (Auto-Detect)

**Always call `websearch` or load this skill when:**
- You are about to write code using an API/library you're not 100% confident about
- You encounter an unfamiliar function signature, parameter, or return type
- You need to verify a library version, feature availability, or deprecation status
- You need a quick code example for a specific API method
- You encounter an error and need to look up the error message or fix
- You need to confirm a configuration option, CLI flag, or environment variable
- The question can be answered from 1-3 sources
- You are short on context for any technology usage — **stop and search before coding**

## When NOT to Use

- The topic requires comparing multiple sources or perspectives — use `deep-research`
- You need to understand a new framework from scratch (3+ subtopics) — use `deep-research`
- The question is about code in the current project — answer directly from the codebase
- The user explicitly asked for "deep research" or "comprehensive report"
- The project will need this knowledge repeatedly — research and convert to skill

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | The specific question to answer |
| `seed_urls` | array of string | No | Suggested URLs to check (auto-discovered if omitted) |

## Expected Outputs

A concise answer with:
- Direct answer to the question
- 1-3 code examples if applicable
- Source URLs for each claim

## Exact Workflow Steps

1. Determine 1-3 authoritative URLs (official docs, API refs)
2. Fetch them using `webfetch`
3. For JS-rendered pages or incomplete responses, use Playwright MCP tools:
   - `browser_navigate` to load the page
   - `browser_snapshot` to extract structured content via element refs
4. Extract the specific information requested
5. Return a concise answer with sources

## Required Checks

- [ ] Every claim has a source URL
- [ ] Answer directly addresses the question

## Failure Modes

| Failure Condition | Response |
|---|---|
| URL returns 404 | Try Playwright MCP as fallback |
| Information not found at any URL | Report "not found in searched sources" |

## Examples

### Example: "What's the cacheLife default profile in Next.js 16?"
1. Crawl nextjs.org/docs/app/api-reference/functions/cacheLife
2. Extract: default is stale=5min, revalidate=15min, expire=never
3. Return answer with source URL

### Example: "Fix: ModuleNotFoundError: No module named 'aiohttp'"
1. This is a context gap — stop and search
2. `websearch("python install aiohttp package")`
3. Extract: `pip install aiohttp`
4. Proceed with the fix

## References

| Reference | Path |
|---|---|
| Web Scraper skill | `../web-scraper/SKILL.md` |
