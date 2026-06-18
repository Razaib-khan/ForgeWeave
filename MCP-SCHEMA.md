# ForgeWeave MCP Schema v1.0

Design principle: **Expose capabilities. Hide orchestration.**
All 12 forge.* tools live in a single FastMCP server. Internal pipeline stages (planner, researchers, validator, synthesizer) are implementation details and never exposed.

---

## Tool 1: `forge.init`

Initializes ForgeWeave in a TUI project: copies template files, sets up AGENTS.md, skills, agents, commands, hooks.

**Input:**

```json
{
  "tui": "opencode | claude | gemini | qwen",
  "project_dir": "/path/to/project",
  "forge_version": "1.0.0",
  "overwrite": false
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `tui` | enum | Yes | Must be one of: opencode, claude, gemini, qwen |
| `project_dir` | string | Yes | Must be existing directory |
| `forge_version` | string | No | Default: "1.0.0", semver format |
| `overwrite` | boolean | No | Default: false |

**Output:**

```json
{
  "status": "ok | error",
  "project_dir": "/path/to/project",
  "tui": "opencode",
  "files_created": ["AGENTS.md", ".opencode/hooks/...", "skills/...", "agents/...", "commands/..."],
  "error": null
}
```

| Field | Type | Description |
|---|---|---|
| `status` | string | "ok" or "error" |
| `files_created` | string[] | List of created file paths |
| `error` | string? | Error message if failed |

**Error codes:**
- `INVALID_TUI` — tui not one of the 4 supported values
- `DIR_NOT_FOUND` — project_dir does not exist
- `INIT_FAILED` — file creation failed
- `ALREADY_INITIALIZED` — forgeweave already present and overwrite=false

---

## Tool 2: `forge.execute_command`

Routes a `/forge-*` command through the command registry, resolves it to a skill + optional agent workflow, and executes it.

**Input:**

```json
{
  "command": "/forge-research",
  "args": "Next.js 16 caching --depth=deep",
  "context": {},
  "job_id": null
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `command` | string | Yes | Must start with `/forge-` |
| `args` | string | No | Raw argument string |
| `context` | object | No | Optional execution context snapshot |
| `job_id` | string? | No | Reuse existing job (resume) |

**Output:**

```json
{
  "status": "ok | error | job_started",
  "job_id": "job_abc123",
  "result": {},
  "error": null
}
```

| Field | Type | Description |
|---|---|---|
| `status` | string | "ok" if synchronous, "job_started" if long-running |
| `job_id` | string | Unique job identifier for polling via forge.status |
| `result` | object | Structured result |

**Error codes:**
- `UNKNOWN_COMMAND` — command not in registry
- `INVALID_ARGS` — argument parsing failed
- `EXECUTION_FAILED` — skill/agent execution failed

---

## Tool 3: `forge.execute_skill`

Loads a skill by name, reads its SKILL.md, validates inputs, executes the skill's workflow (scripts + agent instructions), and returns structured output.

**Input:**

```json
{
  "skill": "deep-research",
  "params": {
    "topic": "Next.js 16 caching",
    "depth": "deep",
    "focus": "usage"
  },
  "context": {}
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `skill` | string | Yes | Must match a skill_id in skills/ |
| `params` | object | Yes | Validated against SKILL.md Inputs |
| `context` | object | No | Execution context |

**Output:**

```json
{
  "status": "ok | error | job_started",
  "job_id": "job_def456",
  "skill": "deep-research",
  "output": {},
  "artifacts": ["research/nextjs-caching-report.md"],
  "error": null
}
```

| Field | Type | Description |
|---|---|---|
| `status` | string | "ok" or "job_started" for long-running skills |
| `job_id` | string | For polling via forge.status |
| `output` | object | Structured skill output |
| `artifacts` | string[] | Paths to generated files |

**Error codes:**
- `SKILL_NOT_FOUND` — skill_id does not exist
- `INVALID_PARAMS` — params fail input validation
- `DEPENDENCY_MISSING` — required sub-skill or tool not available
- `EXECUTION_FAILED` — script/agent failure

---

## Tool 4: `forge.create_agent`

Generates an agent definition file (`.md` for opencode/claude/gemini, `.yaml` for qwen) in the TUI's agents/ directory.

**Input:**

```json
{
  "agent_id": "code-reviewer",
  "role": "Reviews code for quality, security, and style",
  "tools": ["forge.execute_skill", "forge.validate"],
  "skills": ["validation-engine", "debugger"],
  "constraints": "Read-only unless explicit permission",
  "temperature": 0.2
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `agent_id` | string | Yes | kebab-case, unique per project |
| `role` | string | Yes | Max 200 chars |
| `tools` | string[] | No | List of MCP tools the agent can use |
| `skills` | string[] | No | Skills the agent can invoke |
| `constraints` | string | No | Behavioral constraints |
| `temperature` | number | No | 0.0-1.0, default 0.3 |

**Output:**

```json
{
  "status": "ok | error",
  "agent_id": "code-reviewer",
  "tui": "opencode",
  "file_path": "agents/code-reviewer.md",
  "registered": true,
  "error": null
}
```

**Error codes:**
- `DUPLICATE_ID` — agent_id already exists
- `INVALID_FORMAT` — agent_id must be kebab-case
- `WRITE_FAILED` — file creation failed

---

## Tool 5: `forge.research`

Full deep-research pipeline. Internally runs planner → parallel research workers → validator → synthesizer → structured output. The caller only interacts with this single tool.

**Input:**

```json
{
  "topic": "Next.js 16 caching",
  "depth": "standard",
  "focus": "usage",
  "constraints": "Official docs only, no blogs",
  "max_sources": 20
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `topic` | string | Yes | Non-empty, max 500 chars |
| `depth` | enum | No | quick, standard, deep. Default: standard |
| `focus` | enum | No | usage, architecture, comparison, general. Default: usage |
| `constraints` | string | No | Additional rules |
| `max_sources` | integer | No | 1-100, default 20 |

**Output:**

```json
{
  "status": "job_started | ok | error",
  "job_id": "research_abc123",
  "plan": "research/nextjs16-plan.md",
  "report": "research/nextjs16-report.md",
  "summary": {
    "sources_used": 12,
    "subtopics": 4,
    "total_chars": 45000,
    "pipeline_stages": ["plan", "research", "validate", "synthesize", "output"],
    "completed_at": "2026-06-18T12:00:00Z"
  },
  "error": null
}
```

| Field | Type | Description |
|---|---|---|
| `status` | string | Always "job_started" initially; poll via forge.status |
| `job_id` | string | Poll with forge.status(job_id) |
| `plan` | string? | Path to plan file (when complete) |
| `report` | string? | Path to final report (when complete) |
| `summary` | object? | Pipeline summary (when complete) |

**Error codes:**
- `TOPIC_TOO_VAGUE` — topic rejected by planner for insufficient specificity
- `NO_SOURCES_FOUND` — all seed URLs failed
- `PIPELINE_FAILED` — internal stage failure
- `JOB_NOT_FOUND` — invalid job_id on status poll

---

## Tool 6: `forge.search`

Lightweight on-demand search for quick lookups during execution. Not a full research pipeline — single-step fetch-and-extract from authoritative sources.

**Input:**

```json
{
  "query": "React 19 use() hook syntax",
  "max_results": 5,
  "source_filter": "react.dev|developer.mozilla.org"
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `query` | string | Yes | Non-empty, max 300 chars |
| `max_results` | integer | No | 1-10, default 5 |
| `source_filter` | string | No | Comma-separated domain whitelist |

**Output:**

```json
{
  "status": "ok | error",
  "query": "React 19 use() hook syntax",
  "results": [
    {
      "url": "https://react.dev/reference/react/use",
      "title": "use - React",
      "snippet": "use is a React API that lets you read the value of a resource like a Promise or context.",
      "source": "react.dev"
    }
  ],
  "error": null
}
```

**Error codes:**
- `QUERY_TOO_SHORT` — query too vague
- `FETCH_FAILED` — all sources unreachable
- `NO_RESULTS` — zero matching results

---

## Tool 7: `forge.load_context`

Reads the entire project state into a structured snapshot: AGENTS.md, all skills, all agents, all commands, and hook configuration.

**Input:**

```json
{
  "project_dir": "/path/to/project"
}
```

| Field | Type | Required |
|---|---|---|
| `project_dir` | string | Yes |

**Output:**

```json
{
  "status": "ok | error",
  "forge": {
    "version": "1.0.0",
    "tui": "opencode",
    "initialized": true
  },
  "agents": [
    {
      "id": "research-planner",
      "path": "agents/research-planner.md",
      "enabled": true
    }
  ],
  "skills": [
    {
      "id": "deep-research",
      "version": "1.0.0",
      "path": "skills/deep-research/SKILL.md"
    }
  ],
  "commands": ["forge-start", "forge-research", "forge-review", "forge-commit", "forge-test", "forge-docs"],
  "hooks": ["pre_command", "post_command", "pre_skill", "post_skill"],
  "error": null
}
```

**Error codes:**
- `NOT_INITIALIZED` — project not a ForgeWeave project
- `DIR_NOT_FOUND` — project_dir does not exist

---

## Tool 8: `forge.validate`

Validation layer that checks outputs for compliance with AGENTS.md rules, structural correctness, and safety constraints. Used by other tools internally and available for explicit calls.

**Input:**

```json
{
  "target": "research/nextjs16-report.md",
  "rules": [
    "every_claim_has_source",
    "no_blog_sources",
    "structure_complete"
  ]
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `target` | string | Yes | File path or content string |
| `rules` | string[] | Yes | Rule IDs to check |

**Rules catalog:**

| Rule ID | What it does |
|---|---|
| `every_claim_has_source` | Every factual claim has `[source](url)` |
| `no_blog_sources` | Rejects URLs from blog/changelog domains |
| `structure_complete` | Checks required sections exist |
| `no_secrets` | Scans for API keys, passwords, tokens |
| `valid_frontmatter` | YAML frontmatter is valid |
| `agent_id_matches` | Agent file agent_id matches filename |

**Output:**

```json
{
  "status": "pass | fail | error",
  "checks": [
    {
      "rule": "every_claim_has_source",
      "passed": true,
      "details": "23 claims, 23 sources"
    },
    {
      "rule": "no_blog_sources",
      "passed": true,
      "details": "All 12 sources are from official docs"
    }
  ],
  "failed": 0,
  "error": null
}
```

**Error codes:**
- `TARGET_NOT_FOUND` — file does not exist
- `UNKNOWN_RULE` — rule_id not in catalog
- `PARSE_ERROR` — could not parse target

---

## Tool 9: `forge.memory_write`

Stores key/value data in the persistent SQLite state database. Used internally by hooks, skills, and research pipeline to cache intermediate results.

**Input:**

```json
{
  "key": "research:nextjs16:validated_output",
  "value": {
    "subtopics": ["cacheLife", "cacheTag", "updateTag"],
    "claims": 23,
    "sources": 12
  },
  "namespace": "research",
  "ttl_seconds": 86400
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `key` | string | Yes | Namespace:key format, max 256 chars |
| `value` | any | Yes | JSON-serializable |
| `namespace` | string | No | Default: "default" |
| `ttl_seconds` | integer | No | Time-to-live, 0 = forever |

**Output:**

```json
{
  "status": "ok | error",
  "key": "research:nextjs16:validated_output",
  "size_bytes": 256,
  "expires_at": "2026-06-19T12:00:00Z",
  "error": null
}
```

**Error codes:**
- `KEY_TOO_LONG` — key exceeds 256 chars
- `STORAGE_FULL` — DB storage limit reached
- `WRITE_FAILED` — SQLite write error

---

## Tool 10: `forge.memory_read`

Retrieves stored values from the SQLite state database by key or namespace.

**Input:**

```json
{
  "key": "research:nextjs16:validated_output",
  "namespace": "research"
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `key` | string | No | Exact key lookup |
| `namespace` | string | No | List all keys in namespace if key omitted |

**Output:**

```json
{
  "status": "ok | not_found | error",
  "key": "research:nextjs16:validated_output",
  "value": {},
  "created_at": "2026-06-18T12:00:00Z",
  "expires_at": "2026-06-19T12:00:00Z",
  "error": null
}
```

**Error codes:**
- `NOT_FOUND` — key does not exist or expired
- `EXPIRED` — key existed but TTL elapsed

---

## Tool 11: `forge.status`

Single status system for all long-running operations: research jobs, skill executions, agent creation, and future workflow jobs.

**Input:**

```json
{
  "job_id": "research_abc123"
}
```

| Field | Type | Required |
|---|---|---|
| `job_id` | string | Yes |

**Output:**

```json
{
  "status": "running | completed | failed | not_found",
  "job_id": "research_abc123",
  "type": "research",
  "stage": "synthesize",
  "progress_pct": 80,
  "message": "Synthesizing findings from 4 subtopics...",
  "result": null,
  "error": null,
  "created_at": "2026-06-18T11:00:00Z",
  "updated_at": "2026-06-18T11:45:00Z"
}
```

| Field | Type | Description |
|---|---|---|
| `status` | string | running, completed, failed, not_found |
| `type` | string | research, skill_execution, agent_creation, workflow |
| `stage` | string? | Internal stage name |
| `progress_pct` | integer | 0-100 |
| `message` | string | Human-readable status |
| `result` | object? | Final result (only when completed) |

**Error codes:**
- `JOB_NOT_FOUND` — invalid job_id
- `EXPIRED` — job completed > 7 days ago, purged

---

## Tool 12: `forge.capabilities`

Returns the complete list of available tools, skills, agents, and commands. Used by TUIs at startup to understand what ForgeWeave can do.

**Input:**

```json
{
  "project_dir": null
}
```

| Field | Type | Required |
|---|---|---|
| `project_dir` | string? | No. If null, returns server-level capabilities. If set, returns project-specific. |

**Output:**

```json
{
  "status": "ok | error",
  "server_version": "1.0.0",
  "tools": [
    {
      "name": "forge.init",
      "description": "Initialize ForgeWeave in a TUI project",
      "category": "setup"
    }
  ],
  "project": {
    "initialized": true,
    "tui": "opencode",
    "skills": ["deep-research", "planner", ...],
    "agents": ["research-planner", ...],
    "commands": ["forge-start", ...],
    "hooks": ["pre_command", ...]
  },
  "error": null
}
```

**Tool categories:**

| Category | Tools |
|---|---|
| `setup` | forge.init |
| `execution` | forge.execute_command, forge.execute_skill |
| `research` | forge.research, forge.search |
| `context` | forge.load_context |
| `quality` | forge.validate |
| `memory` | forge.memory_read, forge.memory_write |
| `meta` | forge.status, forge.capabilities, forge.create_agent |

---

## Internal Components (Not Exposed via MCP)

| Component | Purpose | Called By |
|---|---|---|
| Planner | Decompose topic into subtopics + seed URLs | forge.research (internal) |
| Research Workers | Crawl URLs, extract content per subtopic | forge.research (internal) |
| Validator | Cross-check claims, remove hallucinations | forge.research (internal) |
| Synthesizer | Merge into final structured report | forge.research (internal) |
| SQLite DB | Job state, memory, traces | All forge.* tools |
| Skills | Logic layer with SKILL.md + scripts | forge.execute_skill |
| Agents | Worker definitions (files on disk) | forge.create_agent |
| Hooks | Lifecycle observers | forge.execute_command (runtime) |
| Research MCP tools | Data plane: fetch, crawl, extract, index | Internal pipeline scripts |

---

## SQLite Schema

```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,            -- research, skill_execution, agent_creation, workflow
    status TEXT NOT NULL,          -- running, completed, failed
    stage TEXT,                    -- current internal stage
    progress_pct INTEGER DEFAULT 0,
    message TEXT,
    input_json TEXT,               -- original input
    result_json TEXT,              -- structured result
    error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE memory (
    key TEXT PRIMARY KEY,
    value_json TEXT NOT NULL,
    namespace TEXT NOT NULL DEFAULT 'default',
    size_bytes INTEGER,
    created_at TEXT NOT NULL,
    expires_at TEXT
);

CREATE TABLE traces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    event_type TEXT NOT NULL,      -- stage_start, stage_end, tool_call, hook_fire
    event_data TEXT,               -- JSON payload
    timestamp TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_type ON jobs(type);
CREATE INDEX idx_memory_namespace ON memory(namespace);
CREATE INDEX idx_traces_job ON traces(job_id);
```
