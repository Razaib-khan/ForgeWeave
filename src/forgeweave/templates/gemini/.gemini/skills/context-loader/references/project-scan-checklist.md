# Project Scan Checklist

When loading context for a ForgeWeave project, check these files in order:

## 1. AGENTS.md
Format: YAML with `agents[]` list
Purpose: Tells you what agents are registered and available
Key fields: `id`, `path`, `enabled`

## 2. AGENT_SPEC.md
Purpose: Agent lifecycle, initialization rules, behavioral constraints
Key sections: Lifecycle, Initialization, Rules

## 3. RESEARCH_INSTRUCTIONS.md
Purpose: Research methodology (usage-focused, no blogs)
Key rules: Source types, output format, sub-agent protocol

## 4. TUI Config
- OpenCode: `.opencode/opencode.json` — MCP servers, instructions chain
- Claude: `.claude/` — project CLAUDE.md
- Gemini: `.gemini/` — project config
- Qwen: `.qwen/` — extension config

## 5. Skills (.opencode/skills/*/SKILL.md)
Each describes a repeatable workflow with scripts, refs, examples
