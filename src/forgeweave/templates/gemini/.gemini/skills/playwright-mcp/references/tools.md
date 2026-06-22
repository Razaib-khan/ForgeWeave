# Playwright MCP — Full Tool Reference

All tools available by capability group. `ref` values come from `browser_snapshot` output.

---

## Core Tools (Always Available)

### Navigation

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_navigate` | `url` (required), `sleep` (ms) | Add `sleep` only for known slow-loading pages |
| `browser_reload` | — | Refreshes current page |
| `browser_go_back` | — | Browser back |
| `browser_go_forward` | — | Browser forward |

### Snapshot & Screenshot

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_snapshot` | — | Returns accessibility tree with refs. Use before every interaction. |
| `browser_take_screenshot` | `ref`, `fullPage`, `scale`, `omitBackground` | Returns PNG. Use sparingly — token-heavy. |

### Interaction

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_click` | `ref` (required) | Clicks element by ref |
| `browser_type` | `ref`, `text`, `submit` | Types text; `submit: true` presses Enter after |
| `browser_fill_text_field` | `ref`, `value` | Fills a single field |
| `browser_fill_form` | `fields: [{ref, value}]` | Fills multiple fields in one call — preferred |
| `browser_select` | `ref`, `value` | Selects dropdown option |
| `browser_check` | `ref` | Checks a checkbox |
| `browser_uncheck` | `ref` | Unchecks a checkbox |
| `browser_hover` | `ref` | Hovers over element |
| `browser_keydown` | `key` | Keyboard press e.g. `"Enter"`, `"Tab"`, `"Escape"` |

### Waiting

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_wait_for` | `text` or `textGone` | Waits for text to appear or disappear |

### Tabs

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_tab_open` | `url` | Opens new tab |
| `browser_tab_close` | `index` | Closes tab by index |
| `browser_tab_list` | — | Lists open tabs |

### Dialogs

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_dialog_accept` | `text` (optional) | Accepts alert/confirm/prompt; optionally provides prompt text |
| `browser_dialog_dismiss` | — | Dismisses/cancels dialog |

### Console

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_console_messages` | `level` (`error`, `warning`, `info`, `debug`) | Reads browser console output |
| `browser_console_clear` | — | Clears console |

### Code Execution

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_run_code` | `code` | Runs async Playwright code `(page) => { ... }` |
| `browser_evaluate` | `expression`, `ref` (optional) | Evaluates JS expression on page or element |

---

## Network Capability (`--caps=network`)

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_network_requests` | `filter`, `includeBody`, `includeHeaders`, `includeStatic` | Lists requests since page load |
| `browser_route` | `pattern`, `body`, `contentType`, `status`, `headers`, `removeHeaders` | Intercepts requests and returns custom responses |
| `browser_route_list` | — | Lists active routes |
| `browser_unroute` | `pattern` | Removes route; omit pattern to remove all |

---

## Storage Capability (`--caps=storage`)

### Cookies

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_cookie_list` | `domain`, `path` | Lists cookies |
| `browser_cookie_get` | `name` | Gets specific cookie |
| `browser_cookie_set` | `name`, `value`, `domain`, `path`, `expires`, `httpOnly`, `secure`, `sameSite` | Sets cookie |
| `browser_cookie_delete` | `name` | Deletes cookie |
| `browser_cookie_clear` | — | Deletes all cookies |

### localStorage

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_localstorage_list` | — | Lists all keys/values |
| `browser_localstorage_get` | `key` | Gets value |
| `browser_localstorage_set` | `key`, `value` | Sets value |
| `browser_localstorage_delete` | `key` | Deletes key |
| `browser_localstorage_clear` | — | Clears all localStorage |

### sessionStorage

Same interface as localStorage — replace `localstorage` with `sessionstorage` in tool names.

### Auth State Persistence

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_storage_state` | `path` (optional) | Saves cookies + localStorage to JSON file |
| `browser_set_storage_state` | `path` | Restores saved auth state |

---

## Testing Capability (`--caps=testing`)

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_verify_element_visible` | `role`, `name` | Asserts element is visible |
| `browser_verify_text_visible` | `text` | Asserts text is visible on page |
| `browser_verify_list_visible` | `items` | Asserts all list items are visible |
| `browser_verify_value` | `ref`, `value` | Asserts input field has value |
| `browser_generate_locator` | `ref` | Generates `page.getByRole(...)` style locator for use in `.spec.ts` |

---

## Vision Capability (`--caps=vision`)

Coordinate-based interaction for canvas/chart/custom-drawn UIs. Use only when elements are absent from the accessibility tree.

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_click` | `ref` + `x`, `y` coordinates | Click by coordinate on canvas/SVG |
| `browser_take_screenshot` | — | Take screenshot for visual inspection |

---

## PDF Capability (`--caps=pdf`)

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_pdf_save` | `filename` (optional) | Saves current page as PDF |

---

## DevTools Capability (`--caps=devtools`)

### Tracing

| Tool | Notes |
|------|-------|
| `browser_start_tracing` | Starts recording all actions, network, screenshots |
| `browser_stop_tracing` | Saves `.zip` trace file; view with `npx playwright show-trace <file>` |

### Video Recording

| Tool | Key Parameters | Notes |
|------|---------------|-------|
| `browser_start_video` | `filename`, `width`, `height` | Starts recording `.webm` video |
| `browser_stop_video` | — | Saves video file |
| `browser_video_chapter` | `title`, `description`, `duration` | Adds chapter marker to video |