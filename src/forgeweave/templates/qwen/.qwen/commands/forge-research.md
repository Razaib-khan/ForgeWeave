---
description: "Execute the deep research pipeline via the deep-research skill: topic → structured report"
subtask: false
---

# Forge Research

Triggers the deep-research skill which internally runs a 6-stage pipeline:
planner → parallel researchers → validator → synthesizer → raw output → skill conversion.

The caller only sees the finished report and skill path. All pipeline stages are internal.

## Usage: `/forge-research <topic> [--depth=<quick|standard|deep>] [--focus=<usage|architecture|comparison|general>] [formatted|unformatted] [skill|no-skill]`

## Behavior

1. Triggers the deep-research skill with the topic and options
2. Output format:
   - `formatted` (default): Produces a well-organized, structured markdown report with sections, code examples, and citations
   - `unformatted`: Produces raw scraped output only — one markdown file per source URL with minimal processing
3. Skill generation:
   - `skill` (default): Also generates a reusable SKILL.md in `.opencode/skills/<topic>/`
   - `no-skill`: Skips skill generation — report only
4. Progress is reported via chat messages during execution

## Internal Pipeline (hidden from caller)

| Stage | Component | What it does |
|---|---|---|
| Plan | Planner agent | Decompose topic into subtopics + seed URLs (uses Playwright MCP for JS-rendered pages) |
| Research | Research agents (×N parallel) | Crawl URLs, extract code examples (Playwright MCP for JS content) |
| Validate | Validator agent | Cross-check claims, remove hallucinations |
| Synthesize | Synthesizer agent | Merge into final structured report |
| Raw Output | Output writer | Save raw scraped data as `research/<slug>-raw/*.md` |
| Skill Conversion | Skill builder | Convert raw findings into industry-grade `.opencode/skills/<topic>/SKILL.md` |

## Rules

- All 6 stages run automatically — no manual intervention
- Sources must be official docs, API refs, usage guides only
- NO blog posts, NO changelogs, NO marketing pages
- Every claim must have a traceable source URL
- Progress is reported via chat messages during execution

## Examples

```
/forge-research Next.js 16 caching --depth=deep --focus=usage formed
/forge-research Next.js 16 caching unformatted no-skill
/forge-research Python 3.14 pattern matching formated no-skill
/forge-research React Server Components formated skill
```
