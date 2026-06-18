---
skill_id: quick-research
name: Quick Research
version: 1.0.0
description: Lightweight single-pass research skill for fast answers without spawning subagents or full planning phases
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - research
  - quick
  - lookup
---

# Quick Research

## Purpose

Get fast, focused answers by crawling a small set of authoritative URLs and extracting the relevant information. No multi-agent pipeline, no planning phase, no validation stage. Ideal for questions that can be answered from 1-3 sources.

## When to Use

- The user asks a narrow, factual question about a library or tool
- Only 1-3 sources need to be consulted
- A quick answer is preferred over a comprehensive report
- The topic is well-defined and does not need decomposition

## When Not to Use

- The topic requires comparing multiple sources or perspectives — use `deep-research`
- The question is about code in the current project — answer directly from the codebase
- The user explicitly asked for "deep research"

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
2. Crawl them using `research_crawl_urls` or `research_single_source`
3. Extract the specific information requested
4. Return a concise answer with sources

## Required Checks

- [ ] Every claim has a source URL
- [ ] Answer directly addresses the question

## Failure Modes

| Failure Condition | Response |
|---|---|
| URL returns 404 | Try `research_browse_js` as fallback |
| Information not found at any URL | Report "not found in searched sources" |

## Examples

### Example: "What's the cacheLife default profile in Next.js 16?"
1. Crawl nextjs.org/docs/app/api-reference/functions/cacheLife
2. Extract: default is stale=5min, revalidate=15min, expire=never
3. Return answer with source URL

## References

| Reference | Path |
|---|---|
| Web Scraper skill | `../web-scraper/SKILL.md` |
