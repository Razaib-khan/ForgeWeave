"""Browser automation for JS-rendered pages — Playwright.

Skill used: playwright-architect
Pattern: async_playwright, headless Chromium, page.goto with wait_until,
         content extraction, screenshot capture, error handling
"""

from playwright.async_api import async_playwright


async def browser_scrape(url: str, screenshot: bool = False, timeout: int = 30000) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="ResearchBot/1.0 (research crawler; research@forgeweave.dev)",
            viewport={"width": 1280, "height": 720},
        )
        page = await context.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=timeout)
            title = await page.title()
            content = await page.content()
            text = await page.inner_text("body")

            base64_screenshot = None
            if screenshot:
                screenshot_bytes = await page.screenshot(full_page=True, type="png")
                import base64
                base64_screenshot = base64.b64encode(screenshot_bytes).decode()

            return {
                "url": url,
                "title": title,
                "text": text,
                "content": content,
                "screenshot": base64_screenshot,
            }
        except Exception as e:
            return {"url": url, "error": str(e)}
        finally:
            await browser.close()


async def browser_screenshot(url: str, timeout: int = 30000) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        try:
            await page.goto(url, wait_until="networkidle", timeout=timeout)
            screenshot_bytes = await page.screenshot(full_page=True, type="png")
            import base64
            return {
                "url": url,
                "screenshot_base64": base64.b64encode(screenshot_bytes).decode(),
                "title": await page.title(),
            }
        finally:
            await browser.close()
