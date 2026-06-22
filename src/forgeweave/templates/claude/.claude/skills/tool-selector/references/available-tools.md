# Tool Registry

This document lists all tools available through ForgeWeave, organized by plane.

## Available Tools

### MCP Tools

| Tool | Purpose |
|---|---|
| `browser_navigate` | Load a URL in the browser |
| `browser_snapshot` | Capture page state as accessibility tree |
| `browser_click` | Click elements on the page |
| `browser_type` | Type text into fields |
| `browser_fill_form` | Fill multiple form fields |
| `browser_take_screenshot` | Take a screenshot |
| `browser_console_messages` | Read console output |
| `browser_network_requests` | Inspect network traffic |

### TUI Built-in Tools

| Tool | Purpose |
|---|---|
| `websearch` | Search the web |
| `webfetch` | Fetch content from a URL |
| `Read` | Read file contents |
| `Write` | Write file to disk |
| `Edit` | Edit existing file |
| `Bash` | Run shell commands |
| `Glob` | Search files by pattern |
| `Grep` | Search file contents |
| `Task` | Spawn sub-agent |

## Data Plane: Research MCP Tools

These are the lower-level tools used internally by the research pipeline. Direct use is allowed for custom workflows.

| Tool | Purpose | Use Case |
|---|---|---|
| `websearch` | Web search | Quick API lookups, error fixes, version checks |
| `webfetch` | URL fetch | Reading documentation, articles, raw content |
| `browser_navigate` | Load JS-rendered page | SPAs, dynamic content, auth-protected pages |
| `browser_snapshot` | Page state snapshot | Accessibility tree, interactive elements |
| `browser_take_screenshot` | Full-page screenshot | Visual verification, documentation |
| `browser_console_messages` | Console output | Debugging, error checking |
| `browser_network_requests` | Network traffic | API inspection, request tracking |

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

### Tool Selection by Task

| Task | Recommended Tools |
|---|---|
| Search the web | `websearch` |
| Read a URL | `webfetch` |
| Browse JS-rendered page | `browser_navigate` + `browser_snapshot` |
| Take a screenshot | `browser_take_screenshot` |
| Full research | `/forge-research` command |
| Quick lookup | `websearch` |
| Read/write files | `Read`, `Write`, `Edit` |
| Run commands | `Bash` |
| Search code | `Glob`, `Grep` |
| Spawn sub-agent | `Task` |
