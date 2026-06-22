"""Fetch a URL with automatic Playwright fallback when HTTP fails."""

import argparse
import sys
from pathlib import Path


def fetch_http(url: str, timeout: int = 15) -> tuple[str | None, str | None]:
    try:
        import httpx

        resp = httpx.get(
            url,
            timeout=timeout,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; ForgeWeave/1.0)",
            },
        )
        resp.raise_for_status()
        text = resp.text
        if len(text) < 2000:
            return text, "content_too_short"
        return text, None
    except ImportError:
        return None, "httpx not installed"
    except Exception as e:
        return None, str(e)


def fetch_playwright(url: str) -> tuple[str | None, str | None]:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            content = page.content()
            browser.close()
            return content, None
    except ImportError:
        return None, "playwright not installed"
    except Exception as e:
        return None, str(e)


def extract_text(html: str) -> str:
    try:
        import trafilatura

        text = trafilatura.extract(html)
        return text or html[:5000]
    except ImportError:
        import re

        return re.sub(r"<[^>]+>", " ", html)[:5000]


def main():
    parser = argparse.ArgumentParser(description="Fetch URL with fallback")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--output", "-o", type=Path, help="Save to file")
    parser.add_argument("--playwright-first", action="store_true", help="Try Playwright first")
    args = parser.parse_args()

    if args.playwright_first:
        html, error = fetch_playwright(args.url)
        if error:
            print(f"Playwright failed: {error}", file=sys.stderr)
            html, error = fetch_http(args.url)
            if error:
                print(f"HTTP also failed: {error}", file=sys.stderr)
                sys.exit(1)
    else:
        html, error = fetch_http(args.url)
        if error:
            print(f"HTTP: {error}, trying Playwright...", file=sys.stderr)
            html, error = fetch_playwright(args.url)
            if error:
                print(f"Playwright also failed: {error}", file=sys.stderr)
                sys.exit(1)

    text = extract_text(html)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Saved {len(text)} chars to {args.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
