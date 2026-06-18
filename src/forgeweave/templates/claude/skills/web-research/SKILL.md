---
skill_id: web-research
name: Web Research
version: 1.0.0
description: Browser-driven or scraping-based skill for real-time internet extraction using Playwright and HTTP-based fetching
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - web
  - scraping
  - browsing
  - research
---

# Web Research

## Purpose

Fetch and extract content from live web pages using HTTP-based fetching (httpx + trafilatura) for standard pages and Playwright headless browser for JavaScript-rendered pages. Is the raw data acquisition layer for all research skills.

## When to Use

- You need to fetch content from a specific URL
- A page requires JavaScript rendering to display its content
- You need to extract structured data from multiple pages
- Real-time information needs to be retrieved from the web

## When Not to Use

- The information is available in indexed documents (use `research_search`)
- The user wants a summary of a topic they haven't specified URLs for
- The task is analyzing the local codebase

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `url` or `urls` | string/array | Yes | URL(s) to fetch |
| `mode` | enum | No (default: auto) | auto, text, html, screenshot |
| `js_render` | boolean | No (default: false) | Whether to use Playwright |

## Expected Outputs

| Output | Description |
|---|---|
| Clean text content | Extracted main content from the page |
| Code examples | Extracted code blocks if mode=auto |
| Screenshot | Full-page screenshot if mode=screenshot |

## Exact Workflow Steps

1. Try HTTP fetch first using `research_single_source` or `research_crawl_urls`
2. If response is incomplete (<2000 chars) or empty, fall back to Playwright via `research_browse_js`
3. Extract clean text content and code blocks
4. If requested, take a screenshot via `research_screenshot`
5. Optionally index into vector database via `research_index_latest`

## Required Checks

- [ ] Content was successfully extracted
- [ ] Fallback to Playwright was attempted if HTTP fetch failed
- [ ] Rate limiting was respected (1s between requests to same domain)

## Failure Modes

| Failure Condition | Response |
|---|---|
| HTTP 404 | Try with Playwright (some SPAs return 404 for JS-rendered content) |
| All methods fail | Report URL as unreachable |
| Content too large | Truncate and report |

## References

| Reference | Path |
|---|---|
| Web Scraper skill | `../web-scraper/SKILL.md` |
| Async Crawler skill | `../async-crawler/SKILL.md` |
| Playwright Architect skill | `../playwright-architect/SKILL.md` |
