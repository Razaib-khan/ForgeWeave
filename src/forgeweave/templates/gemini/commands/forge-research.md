---
description: "Execute the deep research pipeline via forge.research: topic → structured report"
agent: primary
subtask: false
---

# Forge Research

Triggers the `forge.research` tool which internally runs a 5-stage pipeline:
planner → parallel researchers → validator → synthesizer → structured output.

The caller only sees the finished report. All pipeline stages are internal.

## Usage: `/forge-research <topic> [--depth=<quick|standard|deep>] [--focus=<usage|architecture|comparison|general>]`

## Behavior

1. Calls `forge.research` with the topic and options
2. Returns a `job_id` immediately
3. Poll `forge.status(job_id)` to check progress
4. When complete, `forge.status` returns the report path and summary

## Internal Pipeline (hidden from caller)

| Stage | Component | What it does |
|---|---|---|
| Plan | Planner agent | Decompose topic into subtopics + seed URLs |
| Research | Research agents (×N parallel) | Crawl URLs, extract code examples |
| Validate | Validator agent | Cross-check claims, remove hallucinations |
| Synthesize | Synthesizer agent | Merge into final structured report |
| Output | Output writer | Format artifacts and report results |

## Rules

- All 5 stages run automatically — no manual intervention
- Sources must be official docs, API refs, usage guides only
- NO blog posts, NO changelogs, NO marketing pages
- Every claim must have a traceable source URL
- Use `forge.status(job_id)` to check progress

## Examples

```
/forge-research Next.js 16 caching --depth=deep
/forge-research Python 3.14 pattern matching --focus=usage
/forge-research React Server Components vs Server Actions --focus=comparison
```
