---
skill_id: deep-research
name: Deep Research
version: 1.0.0
description: Multi-stage research pipeline that decomposes a topic, gathers structured information, validates it, and synthesizes a final report
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

Execute a multi-stage research pipeline that decomposes a vague topic into structured subtopics, gathers usage-focused information from authoritative sources via parallel agents, validates claims for consistency, and produces a synthesis-grade report. This is invoked internally by `forge.research` — never call the pipeline stages directly.

## When to Use

- A comprehensive, multi-faceted report is needed covering 3+ subtopics
- The topic requires crawling multiple authoritative sources (docs, API refs, guides)
- The output must be structured, validated, and free of hallucination
- The question cannot be answered by a single source or quick lookup

## When Not to Use

- A quick factual answer is needed — use `forge.search` instead
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

## Expected Outputs

| Output | Description |
|---|---|
| `research/<slug>-plan.md` | Structured plan with subtopics, questions, seed URLs |
| `research/<slug>-raw/` | One file per subtopic from parallel research agents |
| `research/<slug>-validated.md` | Cross-checked, deduplicated, hallucination-filtered |
| `research/<slug>-report.md` | Final synthesis with all findings, code examples, sources |

## Internal Workflow (Executed by forge.research)

### Stage 1: Plan
Internal planner agent decomposes topic into 3-7 subtopics with questions and seed URLs from authoritative sources only.

### Stage 2: Research (Parallel)
Internal research agents run concurrently — one per subtopic. Each crawls seed URLs, extracts code examples, API signatures, and edge cases.

### Stage 3: Validate
Internal validator cross-checks all subtopic outputs: removes unsupported claims, flags contradictions, deduplicates findings.

### Stage 4: Synthesize
Internal synthesizer merges validated research into a final report with sections: Overview, Getting Started, Core Content, Advanced Patterns, Migration Guide, Best Practices, Edge Cases, Sources.

### Stage 5: Output
Internal output writer verifies all artifacts exist and reports results via `forge.status`.

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

### Example: Next.js 16 caching APIs
1. `forge.research({topic: "Next.js 16 caching", depth: "deep", focus: "usage"})`
2. Pipeline internally: planner → 3 parallel researchers → validator → synthesizer
3. Final output: `research/nextjs16-report.md` with before/after code examples

## References

| Reference | Path |
|---|---|
| MCP Schema | `./MCP-SCHEMA.md` |
| RESEARCH_INSTRUCTIONS.md | `./RESEARCH_INSTRUCTIONS.md` |
| Internal agents | `./agents/internal/` |
