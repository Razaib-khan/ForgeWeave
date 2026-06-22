---
name: playwright-mcp
description: |
  Complete guide for using Playwright MCP to automate browsers inside AI agent workflows. Use this skill whenever the agent needs to: navigate web pages, fill forms, click elements, take screenshots, mock API responses, manage cookies/localStorage, save auth state, generate Playwright test code, record video/traces, export PDFs, or handle any browser interaction. Triggers on phrases like "open browser", "automate this flow", "test this page", "fill this form", "screenshot this site", "mock the API", "save login state", "generate playwright test", "browser automation", "interact with the site", or any task requiring real browser control. Even if the user mentions just a URL and a goal, this skill applies.
---

# Playwright MCP — AI Agent Browser Automation

Playwright MCP is a **Model Context Protocol server** that lets AI agents control real browsers through structured accessibility snapshots. Refs like `e5`, `e12` give deterministic handles to every interactive element — no pixel-guessing, no brittle CSS selectors.

> **Read `references/tools.md`** for the full tool catalogue before choosing an approach.  
> **Read `references/config.md`** for CLI flags, capabilities, and JSON config options.  
> **Read `references/patterns.md`** for copy-paste workflow recipes.

---

## Core Mental Model

```
browser_navigate → browser_snapshot → interact via refs → browser_snapshot (verify)
```

Every action follows this cycle. The snapshot is the ground truth. Never assume page state — always re-snapshot after an action.

---

## Decision Tree: What to Use

### 1. Snapshot vs Vision Mode

| Situation | Use |
|-----------|-----|
| Standard web app — forms, buttons, links, tables | **Snapshot (default)** |
| Canvas, SVG, chart, game UI, custom drawn widget | **Vision mode** (`--caps=vision`) |
| Verifying visual layout, pixel correctness | **Screenshot** + snapshot together |

**Rule:** Snapshots for 90%+ of tasks. Vision only for elements absent from the accessibility tree.

### 2. Which Capability to Enable

Enable only what you need — each capability adds tokens to every interaction:

| Need | Add to `--caps=` |
|------|-----------------|
| Mock API responses / intercept network | `network` |
| Cookies, localStorage, auth state save/restore | `storage` |
| Verify elements, generate `.spec.ts` test code | `testing` |
| Canvas/chart coordinate-based clicking | `vision` |
| Export page as PDF | `pdf` |
| Video recording, tracing | `devtools` |

Minimal config (no capabilities) is fastest and cheapest on tokens.

### 3. Token Budget Awareness

A single `browser_navigate` on a content-rich page can return **thousands of tokens**. Across a multi-step session this compounds.

| Practice | Saves Tokens |
|----------|-------------|
| Enable only needed capabilities | High |
| Use `browser_snapshot` only when you need to verify or find a ref | High |
| Avoid `browser_take_screenshot` unless visual proof is required | Medium |
| Use `browser_fill_form` (one call) instead of multiple `browser_type` | Low |
| Stop tracing/video when not debugging | Medium |

---

## Standard Workflow Templates

### Login Flow

```
browser_navigate { url }
browser_snapshot                          → find email/password refs
browser_type { ref: "e3", text: email }
browser_type { ref: "e5", text: password }
browser_click { ref: "e7" }              → submit button
browser_snapshot                          → verify dashboard appeared
```

Save state after login so you never repeat it:
```
browser_storage_state                     → writes auth-state.json
```
Restore on next run: `--storage-state=./auth-state.json`

### Form Fill (Multi-Field)

```
browser_navigate { url }
browser_snapshot
browser_fill_form {
  fields: [
    { ref: "e3", value: "..." },
    { ref: "e5", value: "..." }
  ]
}
browser_click { ref: "e9" }              → submit
browser_snapshot                          → verify success message
```

### API Mocking

Requires `--caps=network`:
```
browser_route {
  pattern: "**/api/users",
  body: '[{"id":1,"name":"Alice"}]',
  contentType: "application/json"
}
browser_navigate { url }
browser_snapshot                          → page now uses mocked data
```

### Debugging a Broken Page

```
browser_navigate { url }
browser_console_messages { level: "error" }   → read JS errors first
browser_snapshot                              → inspect element tree
browser_take_screenshot                       → visual evidence
```

If the problem is complex, start a trace:
```
browser_start_tracing
[... reproduce the issue ...]
browser_stop_tracing                          → share trace.zip with team
```

### Generate Playwright Test Code

Requires `--caps=testing`. After completing an exploratory flow:
```
browser_generate_locator { ref: "e5" }
→ page.getByPlaceholder('What needs to be done?')
```
Use `browser_verify_text_visible`, `browser_verify_element_visible` to add assertions that translate to `expect()` calls.

---

## Common Pitfalls

| Mistake | Correct Approach |
|---------|-----------------|
| Acting on a stale ref after page re-render | Re-run `browser_snapshot` before each new interaction |
| Using vision mode on a standard form | Default to snapshot — forms are always in the accessibility tree |
| Taking screenshots repeatedly to "check" state | Use `browser_snapshot` — it's structured and token-cheaper |
| Opening storage/network capabilities you don't need | Only add capabilities matching the task |
| Forgetting `browser_wait_for` on dynamic pages | Wait for content to appear before snapshotting |
| Logging in on every agent run | Save `browser_storage_state` once, load with `--storage-state` |
| Multiple `browser_type` calls for one form | Use `browser_fill_form` — one call, fewer tokens |

---

## Refs: How They Work

After `browser_snapshot`, every interactive element has a `ref` like `e5`. These refs are:
- **Ephemeral** — valid only until the next page render
- **Deterministic** — clicking `e5` always hits the same element
- **Auto-waitable** — Playwright waits for the element to be ready before acting

Always re-snapshot when you suspect the page has changed.

---

## Quick Config Reference

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--caps=network,storage,testing"]
    }
  }
}
```

Key flags: `--headless`, `--browser=firefox`, `--device=iPhone 15`, `--isolated`, `--storage-state=./auth.json`, `--port 8931` (HTTP server mode).

Full options → `references/config.md`  
Full tool list → `references/tools.md`  
Copy-paste recipes → `references/patterns.md`