# Tool Registry

This document lists all tools available through ForgeWeave, organized by plane.

## Control Plane: Forge MCP Tools

These are the primary tools agents should use. They handle orchestration, state, and pipeline execution.

| Tool | Category | Purpose |
|---|---|---|
| `forge.init` | Setup | Initialize ForgeWeave in a project |
| `forge.execute_command` | Routing | Route `/forge-*` commands through command registry |
| `forge.execute_skill` | Execution | Load SKILL.md + scripts, execute workflow |
| `forge.create_agent` | Generation | Write agent definition file to agents/ dir |
| `forge.research` | Pipeline | Full deep-research pipeline (plan → research → validate → synthesize → output) |
| `forge.search` | Lookup | Lightweight on-demand web search |
| `forge.load_context` | Introspection | Read project state into structured dict |
| `forge.validate` | Quality | Check outputs against validation rules |
| `forge.memory_read` | Persistence | Read from SQLite state DB |
| `forge.memory_write` | Persistence | Write to SQLite state DB |
| `forge.status` | Meta | Poll status of any long-running job |
| `forge.capabilities` | Meta | List available tools, skills, agents, commands |

## Data Plane: Research MCP Tools

These are the lower-level tools used internally by the research pipeline. Direct use is allowed for custom workflows.

| Tool | Purpose | When to Use |
|---|---|---|
| `research_single_source` | Fetch 1 URL | Single-page research, quick lookup |
| `research_crawl_urls` | Fetch N URLs | Multi-source research, data gathering |
| `research_browse_js` | JS-rendered page | SPAs, dynamic content, auth walls |
| `research_screenshot` | Full-page screenshot | Visual verification, archival |
| `research_extract_document` | PDF/DOCX | Paper research, report extraction |
| `research_index_latest` | URL → vector DB | Long-term knowledge base building |
| `research_search` | Semantic search | Finding previously indexed content |
| `research_synthesize` | Search + group | Aggregating findings by relevance |
| `research_vector_stats` | DB stats | Monitoring index health |
| `research_clear_cache` | Clear caches | Stale data, force refresh |

## Local Tools

Built-in tools available in all TUIs.

| Tool | Purpose |
|---|---|
| Read | Read file contents |
| Write | Write file to disk |
| Edit | Edit existing file |
| Bash | Run shell commands |
| Glob | Search files by pattern |
| Grep | Search file contents |
| Task | Spawn sub-agent |

## Tool Selection by Task

| Task Type | Recommended Tools |
|---|---|
| Initialize project | `forge.init` |
| Run /forge-* command | `forge.execute_command` |
| Execute a skill | `forge.execute_skill` + `forge.load_context` |
| Full research | `forge.research` + `forge.status` |
| Quick lookup | `forge.search` |
| Validate output | `forge.validate` |
| Read/write memory | `forge.memory_read` / `forge.memory_write` |
| Create an agent | `forge.create_agent` |
| Load project context | `forge.load_context` |
| List capabilities | `forge.capabilities` |
| Check job progress | `forge.status` |
