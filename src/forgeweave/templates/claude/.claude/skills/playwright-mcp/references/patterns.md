# Playwright MCP — Copy-Paste Workflow Patterns

Ready-to-use recipes for common agent automation tasks.

---

## Pattern 1: Login and Save Auth State

Use once, then load `--storage-state` on every subsequent run.

```
browser_navigate { url: "https://app.example.com/login" }
browser_snapshot
  → textbox "Email" [ref=e3]
  → textbox "Password" [ref=e5]
  → button "Sign in" [ref=e7]
browser_type { ref: "e3", text: "alice@example.com" }
browser_type { ref: "e5", text: "s3cr3t" }
browser_click { ref: "e7" }
browser_snapshot
  → heading "Dashboard" [level=1]   ← verify login succeeded
browser_storage_state               → saved to auth-state.json
```

Next run: load with `--storage-state=./auth-state.json` — skip login entirely.

---

## Pattern 2: Multi-Field Form Submission

```
browser_navigate { url: "https://app.example.com/signup" }
browser_snapshot
browser_fill_form {
  fields: [
    { ref: "e3", value: "Alice Smith" },
    { ref: "e5", value: "alice@example.com" },
    { ref: "e7", value: "s3cr3t" },
    { ref: "e9", value: "Software Engineer" }
  ]
}
browser_select { ref: "e11", value: "us" }       → country dropdown
browser_check  { ref: "e13" }                    → terms checkbox
browser_click  { ref: "e15" }                    → submit button
browser_wait_for { text: "Account created" }
browser_snapshot                                 → verify success state
```

---

## Pattern 3: API Mocking

Requires `--caps=network`.

```
→ Set up mock before navigation
browser_route {
  pattern: "**/api/users",
  body: '[{"id":1,"name":"Alice","role":"admin"}]',
  contentType: "application/json"
}

→ Optional: simulate error state
browser_route {
  pattern: "**/api/payments",
  status: 503,
  body: '{"error":"Service unavailable"}'
}

browser_navigate { url: "https://app.example.com/users" }
browser_snapshot                               → verify page shows mocked data

→ Remove mock when done
browser_unroute { pattern: "**/api/users" }
```

---

## Pattern 4: Debug a Broken Page

```
browser_navigate { url: "https://broken-app.example.com" }

→ Step 1: read JS errors first
browser_console_messages { level: "error" }
  → {"level":"error","text":"Uncaught ReferenceError: $ is not defined","url":"..."}

→ Step 2: visual snapshot
browser_take_screenshot

→ Step 3: network errors
browser_network_requests { filter: "api/" }
  → {"url":"...api/config","status":401}   ← auth problem found

→ Step 4: if still unclear, start a trace
browser_start_tracing
[reproduce the failure]
browser_stop_tracing
→ Share trace.zip for full timeline
```

---

## Pattern 5: Storage State Manipulation

Requires `--caps=storage`.

```
→ Simulate logged-out user without navigating away
browser_cookie_clear
browser_reload
browser_snapshot
  → heading "Sign in"   ← confirm logout triggered

→ Reset onboarding flow
browser_localstorage_set { key: "onboarding_done", value: "false" }
browser_reload
browser_snapshot
  → heading "Welcome! Let's get started"

→ Inspect current session
browser_cookie_list
browser_localstorage_list
```

---

## Pattern 6: Generate Playwright Test Code

Requires `--caps=testing`.

```
browser_navigate { url: "https://demo.playwright.dev/todomvc" }
browser_snapshot
  → textbox "What needs to be done?" [ref=e5]

browser_type { ref: "e5", text: "Buy groceries", submit: true }
browser_verify_text_visible { text: "Buy groceries" }
  → ✓ Text visible: "Buy groceries"

browser_generate_locator { ref: "e5" }
  → page.getByPlaceholder('What needs to be done?')
```

Generated test `.spec.ts`:
```ts
await page.getByPlaceholder('What needs to be done?').fill('Buy groceries');
await page.getByPlaceholder('What needs to be done?').press('Enter');
await expect(page.getByText('Buy groceries')).toBeVisible();
```

---

## Pattern 7: Video Recording with Chapter Markers

Requires `--caps=devtools`.

```
browser_start_video { filename: "checkout-flow.webm", width: 1280, height: 720 }

browser_video_chapter { title: "Open cart", description: "User reviews items" }
browser_navigate { url: "https://shop.example.com/cart" }

browser_video_chapter { title: "Enter shipping", description: "Fill address form" }
browser_fill_form {
  fields: [
    { ref: "e3", value: "Alice Smith" },
    { ref: "e5", value: "123 Main St" }
  ]
}

browser_video_chapter { title: "Checkout", description: "Submit order" }
browser_click { ref: "e9" }
browser_wait_for { text: "Order confirmed" }

browser_stop_video
→ Video saved: /output/checkout-flow.webm
```

---

## Pattern 8: Multi-Tab Workflow

```
browser_navigate { url: "https://app.example.com/dashboard" }
browser_tab_list
  → Tab 0: https://app.example.com/dashboard

browser_tab_open { url: "https://app.example.com/reports" }
browser_snapshot                → now on Tab 1

→ Switch back to Tab 0
browser_tab_list
browser_navigate { url: "https://app.example.com/dashboard" }

browser_tab_close { index: 1 }  → close reports tab
```

---

## Pattern 9: Simulate Offline / Error States

Requires `--caps=network`.

```
→ Block all traffic (offline simulation)
browser_route { pattern: "**/*", status: 503, body: "Service unavailable" }
browser_reload
browser_snapshot                → offline/error page should appear

→ Block only images (test degraded experience)
browser_route { pattern: "**/*.{jpg,png,webp}", status: 404 }
browser_reload

→ Strip auth headers (test unauthenticated experience)
browser_route {
  pattern: "**/*",
  removeHeaders: ["cookie", "authorization"]
}

→ Remove routes when done
browser_unroute { }             → clears all routes
```

---

## Pattern 10: Iframe Interaction via Code Execution

When standard tools can't reach elements inside iframes:

```
browser_run_code {
  code: "async (page) => {
    const frame = page.frames().find(f => f.url().includes('payment-widget'));
    await frame.fill('#card-number', '4111111111111111');
    await frame.fill('#expiry', '12/26');
    await frame.click('#submit-payment');
  }"
}
browser_snapshot               → verify payment confirmed
```

---

## Pattern 11: Grant Permissions + Geolocation

```
browser_run_code {
  code: "async (page) => {
    await page.context().grantPermissions(['geolocation']);
    await page.context().setGeolocation({ latitude: 37.7749, longitude: -122.4194 });
  }"
}
browser_navigate { url: "https://maps-app.example.com" }
browser_snapshot               → verify location-aware UI loaded
```

Or set at startup via `initPage` config (see `references/config.md`).

---

## Pattern 12: PDF Export

Requires `--caps=pdf`.

```
browser_navigate { url: "https://app.example.com/invoice/42" }
browser_wait_for { textGone: "Loading..." }
browser_pdf_save { filename: "invoice-42.pdf" }
→ PDF saved to: /output/invoice-42.pdf
```

---

## Anti-Patterns to Avoid

```
✗ Taking a screenshot to "check" page state → use browser_snapshot instead
✗ Using vision mode on a standard login form → snapshot handles all form elements
✗ Running browser_snapshot after every single tool call → only snapshot when you need a ref or need to verify
✗ Keeping network/storage/devtools caps enabled when not needed → adds tokens per tool
✗ Logging in on every agent run → save auth state once, load it
✗ Using browser_type five times for one form → use browser_fill_form
✗ Not using browser_wait_for on async pages → elements may not be interactive yet
✗ Assuming a ref is still valid after navigation/re-render → always re-snapshot
```