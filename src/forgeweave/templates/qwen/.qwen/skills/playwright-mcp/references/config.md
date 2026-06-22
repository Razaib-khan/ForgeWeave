# Playwright MCP — Configuration Reference

---

## Minimal Config (Fastest, Fewest Tokens)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

---

## Full Config with All Capabilities

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--caps=network,storage,testing,pdf,devtools,vision"
      ]
    }
  }
}
```

---

## Preset Configs by Workflow

### Dev / Exploration (Visible Browser, Persistent Profile)

```json
{
  "command": "npx",
  "args": [
    "@playwright/mcp@latest",
    "--browser=chromium",
    "--caps=network,storage,testing,pdf,devtools",
    "--user-data-dir=./playwright-dev-profile",
    "--output-dir=./mcp-output"
  ]
}
```

### CI / Headless (Pre-authenticated, Auto-trace)

```json
{
  "command": "npx",
  "args": [
    "@playwright/mcp@latest",
    "--headless",
    "--isolated",
    "--storage-state=./profiles/admin.json",
    "--caps=network,storage,testing,devtools",
    "--save-trace",
    "--output-dir=./mcp-artifacts"
  ]
}
```

### Multi-Role (Admin + User Simultaneously)

```json
{
  "mcpServers": {
    "playwright-admin": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--caps=storage",
        "--isolated",
        "--storage-state=./profiles/admin.json"
      ]
    },
    "playwright-user": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--caps=storage",
        "--isolated",
        "--storage-state=./profiles/user.json"
      ]
    }
  }
}
```

### HTTP Server Mode (Headless Server / No Display)

Start server:
```bash
npx @playwright/mcp@latest --port 8931
```

Connect via config:
```json
{
  "mcpServers": {
    "playwright": {
      "url": "http://localhost:8931/mcp"
    }
  }
}
```

### Extension Mode (Reuse Existing Chrome Session)

Install the Playwright MCP Bridge extension from the Chrome Web Store or load unpacked from GitHub.

```json
{
  "mcpServers": {
    "playwright-extension": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--extension"]
    }
  }
}
```

Best for: sites where you're already logged in (GitHub, cloud consoles) without rebuilding auth.

---

## JSON Config File (Advanced)

```bash
npx @playwright/mcp@latest --config ./playwright-mcp.config.json
```

```json
{
  "browser": "chromium",
  "headless": true,
  "device": "Desktop Chrome HiDPI",
  "viewportSize": "1440x900",
  "userDataDir": "./playwright-profile",
  "storageState": "./profiles/admin.json",
  "caps": ["network", "storage", "testing", "pdf", "devtools"],
  "proxy": {
    "server": "http://proxy.internal:8080",
    "bypass": "localhost,127.0.0.1"
  },
  "outputDir": "./mcp-output",
  "saveTrace": true,
  "saveSession": true
}
```

### Init Scripts (Run on Every Page Before Page Scripts)

```json
{
  "browser": {
    "initScript": ["./setup.js"]
  }
}
```

```js
// setup.js
window.isPlaywrightMCP = true;
```

### Init Page (Playwright Code at Startup)

```json
{
  "browser": {
    "initPage": ["./setup-page.ts"]
  }
}
```

```ts
// setup-page.ts
export default async ({ page }) => {
  await page.context().grantPermissions(['geolocation']);
  await page.context().setGeolocation({ latitude: 37.7749, longitude: -122.4194 });
};
```

---

## CLI Flags Quick Reference

| Flag | Description | Env Variable |
|------|-------------|--------------|
| `--browser` | `chrome` (default), `firefox`, `webkit`, `msedge` | `PLAYWRIGHT_MCP_BROWSER` |
| `--headless` | Run without visible window | `PLAYWRIGHT_MCP_HEADLESS` |
| `--caps` | Comma-separated capabilities | `PLAYWRIGHT_MCP_CAPS` |
| `--config` | Path to JSON config file | `PLAYWRIGHT_MCP_CONFIG` |
| `--isolated` | Fresh in-memory profile per run | `PLAYWRIGHT_MCP_ISOLATED` |
| `--extension` | Connect via Chrome extension | `PLAYWRIGHT_MCP_EXTENSION` |
| `--user-data-dir` | Path to custom browser profile | `PLAYWRIGHT_MCP_USER_DATA_DIR` |
| `--storage-state` | Load saved cookies/localStorage at start | `PLAYWRIGHT_MCP_STORAGE_STATE` |
| `--port` | Start HTTP transport on this port | `PLAYWRIGHT_MCP_PORT` |
| `--host` | Server hostname | `PLAYWRIGHT_MCP_HOST` |
| `--device` | Emulate device e.g. `"iPhone 15"` | `PLAYWRIGHT_MCP_DEVICE` |
| `--viewport-size` | e.g. `"1280x720"` | `PLAYWRIGHT_MCP_VIEWPORT_SIZE` |
| `--proxy-server` | Proxy URL | `PLAYWRIGHT_MCP_PROXY_SERVER` |
| `--proxy-bypass` | Bypass list for proxy | `PLAYWRIGHT_MCP_PROXY_BYPASS` |
| `--timeout-action` | Action timeout in ms (default 5000) | `PLAYWRIGHT_MCP_TIMEOUT_ACTION` |
| `--timeout-navigation` | Navigation timeout in ms (default 6000) | `PLAYWRIGHT_MCP_TIMEOUT_NAVIGATION` |
| `--output-dir` | Directory for screenshots, traces, video | `PLAYWRIGHT_MCP_OUTPUT_DIR` |
| `--save-trace` | Auto-save trace on session end | `PLAYWRIGHT_MCP_SAVE_SESSION` |
| `--save-video` | Auto-record video e.g. `"800x600"` | `PLAYWRIGHT_MCP_SAVE_VIDEO` |
| `--allowed-origins` | Whitelist origins the browser can visit | `PLAYWRIGHT_MCP_ALLOWED_ORIGINS` |
| `--blocked-origins` | Block specific origins | `PLAYWRIGHT_MCP_BLOCKED_ORIGINS` |
| `--grant-permissions` | Pre-grant browser permissions | `PLAYWRIGHT_MCP_GRANT_PERMISSIONS` |
| `--no-sandbox` | Disable Chrome sandbox (for Docker) | `PLAYWRIGHT_MCP_NO_SANDBOX` |
| `--secrets` | Path to dotenv secrets file | `PLAYWRIGHT_MCP_SECRETS_FILE` |
| `--vision` | Shortcut for `--caps=vision` | — |

---

## Browser Profile Locations (Default)

| Platform | Default Path |
|----------|-------------|
| macOS | `~/Library/Caches/ms-playwright/mcp-{channel}-profile` |
| Linux | `~/.cache/ms-playwright/mcp-{channel}-profile` |
| Windows | `%LOCALAPPDATA%\ms-playwright\mcp-{channel}-profile` |

Override with `--user-data-dir=./my-profile`.  
Use `--isolated` for completely fresh state per run (CI-safe).