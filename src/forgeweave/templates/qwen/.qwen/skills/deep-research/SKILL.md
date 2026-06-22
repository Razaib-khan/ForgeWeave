---
skill_id: deep-research
name: Deep Research
version: 1.0.0
description: Multi-stage research pipeline that decomposes a topic, gathers structured information, validates it, and synthesizes a final report. Supports formatted/unformatted output and skill/no-skill generation modes.
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - research
  - pipeline
  - synthesis
---

# Deep Research

## Purpose

Execute a multi-stage research pipeline that decomposes a vague topic into structured subtopics, gathers usage-focused information from authoritative sources via parallel agents, validates claims for consistency, produces a synthesis-grade report, and converts raw findings into a reusable industry-grade skill. This is invoked internally by the deep-research skill — never call the pipeline stages directly.

## When to Use

- A comprehensive, multi-faceted report is needed covering 3+ subtopics
- The topic requires crawling multiple authoritative sources (docs, API refs, guides)
- The output must be structured, validated, and free of hallucination
- The question cannot be answered by a single source or quick lookup

## When Not to Use

- A quick factual answer is needed — use websearch instead
- Only one source needs to be checked — use the MCP data plane tools directly
- The topic is a simple how-to question — answer directly
- Real-time data is needed (stock prices, live scores) — use web-research

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `topic` | string | Yes | The research topic or question |
| `depth` | enum | No (default: standard) | quick, standard, deep |
| `focus` | enum | No (default: usage) | usage, architecture, comparison, general |
| `constraints` | string | No | Additional rules from AGENTS.md or user |
| `output_mode` | enum | No (default: formatted) | formatted, unformatted |
| `skill_mode` | enum | No (default: skill) | skill, no-skill |

## Expected Outputs

| Output | Condition | Description |
|---|---|---|
| `research/<slug>-plan.md` | Always | Structured plan with subtopics, questions, seed URLs |
| `research/<slug>-raw/` | Always | One file per subtopic from parallel research agents |
| `research/<slug>-validated.md` | Always | Cross-checked, deduplicated, hallucination-filtered |
| `research/<slug>-report.md` | `formatted` mode | Final synthesis with all findings, code examples, sources |
| `.opencode/skills/<topic>/SKILL.md` | `skill` mode | Reusable skill generated from findings |

## Internal Workflow

### Stage 1: Plan
Internal planner agent decomposes topic into 3-7 subtopics with questions and seed URLs from authoritative sources only. For JS-rendered content, Playwright MCP tools (`browser_navigate`, `browser_snapshot`) are available for interactive browsing during URL discovery.

### Stage 2: Research (Parallel)
Internal research agents run concurrently — one per subtopic. Each crawls seed URLs, extracts code examples, API signatures, and edge cases. For JS-rendered pages, agents use Playwright MCP tools (`browser_navigate`, `browser_snapshot`).

### Stage 3: Validate
Internal validator cross-checks all subtopic outputs: removes unsupported claims, flags contradictions, deduplicates findings.

### Stage 4: Synthesize
Internal synthesizer merges validated research into a final report with sections: Overview, Getting Started, Core Content, Advanced Patterns, Migration Guide, Best Practices, Edge Cases, Sources.

### Stage 5: Output
Internal output writer saves research results based on output mode:
- `formatted` (default): Produces a structured report at `research/<slug>-report.md` with sections: Overview, Getting Started, Core Content, Advanced Patterns, Migration Guide, Best Practices, Edge Cases, Sources
- `unformatted`: Saves raw scraped data as individual markdown files in `research/<slug>-raw/` with minimal processing

Raw data is always saved to `research/<slug>-raw/` regardless of mode.

### Stage 6: Skill Conversion (conditional)
AI uses the skill-builder skill to convert the raw findings into a reusable SKILL.md file — **only when `skill` mode is selected**:
- Reads all `research/<slug>-raw/*.md` files
- Identifies reusable patterns, APIs, and best practices
- Writes a structured SKILL.md with frontmatter, workflow steps, gotchas, and references
- Places the skill in `.opencode/skills/<topic-slug>/` for future coding use
- Reports the skill path to the user

## Required Checks

- [ ] Planner ran first (never skip)
- [ ] Research agents ran in parallel
- [ ] Validator ran after all research completed
- [ ] Every claim has a source URL
- [ ] No blog posts or changelogs used as sources

## Failure Modes

| Failure Condition | Response |
|---|---|
| Planner produces <3 subtopics | Respawn with "produce at least 3" |
| All seed URLs return 404 | Report "all sources unavailable" |
| Validator flags >50% claims as unsupported | Re-run research with better URLs |
| Pipeline exceeds max iterations | Stop and return partial results |

## Examples

### Example 1: Full research with skill (default)
Trigger: `/forge-research Next.js 16 caching --depth=deep`
Result: `research/nextjs16-report.md` + `.opencode/skills/nextjs16/SKILL.md`

### Example 2: Raw output only, no skill
Trigger: `/forge-research Next.js 16 caching unformatted no-skill`
Result: `research/nextjs16-raw/*.md` (raw files only)

### Example 3: Formatted report, no skill
Trigger: `/forge-research Python 3.14 pattern matching formed no-skill`
Result: `research/python314-report.md` (structured report only)

## References

| Reference | Path |
|---|---|
| RESEARCH_INSTRUCTIONS.md | `./RESEARCH_INSTRUCTIONS.md` |
