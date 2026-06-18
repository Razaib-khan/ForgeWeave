# Research Instructions

When performing research tasks, use the `deep-research` MCP server tools to gather data, then save all outputs to the `research/` directory.

## Starting the Server

```bash
forge mcp              # start with normal logging
forge mcp --verbose    # start with debug logging
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `research_single_source` | Fetch and extract clean content from a single URL |
| `research_crawl_urls` | Crawl multiple URLs concurrently with rate limiting |
| `research_browse_js` | Fetch a JavaScript-rendered page with Playwright |
| `research_screenshot` | Take a full-page screenshot of a URL |
| `research_extract_document` | Extract text from PDF, DOCX, etc. |
| `research_index_latest` | Fetch + extract + index a URL into the vector database |
| `research_search` | Semantic search across indexed documents |
| `research_synthesize` | Search and return grouped sources for the agent to analyze |
| `research_deep_research` | **Comprehensive research** — crawls all seed URLs, extracts, indexes, returns structured report |
| `research_vector_stats` | Show vector database statistics |
| `research_clear_cache` | Clear HTTP and LLM caches |

## Focus: Usage Over Features

Research must focus on **practical usage** — code examples, API patterns, best practices, and how to use tools at their full potential. Do NOT:

- ❌ List version histories or changelogs
- ❌ Describe what a feature is without showing how to use it
- ❌ Collect generic marketing descriptions
- ❌ Include unrelated historical context

Do:

- ✅ Show concrete code examples for every API
- ✅ Explain real-world usage patterns and when to use each
- ✅ Extract configuration examples with practical defaults
- ✅ Show migration patterns (before/after code)
- ✅ Include edge cases and common pitfalls
- ✅ Compare approaches and recommend the best one

## Workflow

1. **Plan** — identify which URLs cover usage docs, API references, and tutorials (not blog posts or changelogs)
2. **Crawl** — use `research_crawl_urls` or `research_single_source` to collect raw data from usage-focused pages
3. **Extract code** — pull out all code blocks, API signatures, configuration examples
4. **Analyze** — synthesize findings into a practical usage guide with patterns and recommendations
5. **Save** — save as `research/<topic>-<date>.md`

## Sub-Agent Research Protocol

For complex topics, research should be delegated to a sub-agent via the `task` tool with `subagent_type: "general"`. The sub-agent receives a highly specialized system prompt that enforces the usage-focused methodology.

**Progress reporting:** The sub-agent must report progress at each stage via chat messages:
1. **Starting** — "Research started on [topic]. Planning seed URLs..."
2. **Crawling** — "Crawling [N] URLs: [url1], [url2], ..."
3. **Extracting** — "Extracting code examples and patterns from [N] sources..."
4. **Synthesizing** — "Synthesizing [N] findings into usage guide..."
5. **Complete** — "Research complete. Report saved to [path]."

## Output Convention

- Save research reports as `research/<topic>-<date>.md`
- Structure reports as **practical usage guides**:
  - `# Title` — topic and scope
  - `## Overview` — 1-2 paragraph scope, **not** history
  - `## Installation/Setup` — how to get started
  - `## Core Usage` — code examples for each API with explanations
  - `## Advanced Patterns` — power-user techniques
  - `## Migration Guide` — before/after if applicable
  - `## Best Practices` — recommendations with rationale
  - `## Sources` — URLs used
- Screenshots saved to `research/screenshots/` if needed
- The `research/` directory is gitignored
