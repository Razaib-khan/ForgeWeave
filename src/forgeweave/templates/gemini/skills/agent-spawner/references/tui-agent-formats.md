# Agent Format Reference per TUI

## OpenCode (.md)
Frontmatter: `description`, `mode`, `temperature`, `permissions`, `model`
Filename: `agents/<agent-id>.md` (filename = agent name)
Invocation: `@<agent-id>`

## Claude Code (.md)
Frontmatter: `name`, `description`, `model`, `permissions`
Filename: `agents/<agent-id>.md` (name field = agent name)
Invocation: `/agents` then select, or `@<agent-id>`

## Gemini CLI (.md)
Frontmatter: `name`, `description`, `tools`, `memory`
Filename: `agents/<agent-id>.md` (name field = agent name)
Invocation: `@<agent-id>`

## Qwen Code (.yaml)
Frontmatter: `name`, `description`, `mode`, `temperature`, `permissions`, `model`
Filename: `agents/<agent-id>.yaml` (name field = agent name)
Extension config: `qwen-extension.json` with `"agents": "agents"` key
Invocation: `@<agent-id>`
