"""Web page fetching and content extraction — httpx + BeautifulSoup + trafilatura.

Skill used: web-scraper
Pattern: httpx AsyncClient with timeouts, retry with tenacity,
         trafilatura for clean text + metadata, BeautifulSoup for structural parse
"""

import json

import httpx
import trafilatura
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from forgeweave.research_mcp.models import ExtractedContent

HEADERS = {
    "User-Agent": "ResearchBot/1.0 (research crawler; research@forgeweave.dev)",
    "Accept": "text/html,application/xhtml+xml",
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def fetch_page(url: str, client: httpx.AsyncClient | None = None) -> str:
    close_client = client is None
    if client is None:
        client = httpx.AsyncClient(headers=HEADERS, timeout=30.0, follow_redirects=True)
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return ""
        raise
    finally:
        if close_client:
            await client.aclose()


def extract_main_content(html: str, url: str = "") -> ExtractedContent | None:
    meta_json = trafilatura.extract(
        html,
        url=url,
        output_format="json",
        with_metadata=True,
        include_comments=False,
        include_tables=True,
        include_images=False,
    )
    if meta_json is None:
        return None
    meta = json.loads(meta_json) if isinstance(meta_json, str) else meta_json
    data = meta.get("text", "")
    return ExtractedContent(
        url=url,
        title=meta.get("title") or "",
        author=meta.get("author") or "",
        date=meta.get("date") or "",
        text=data,
        source=url.split("/")[2] if url else None,
    )


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def extract_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    from urllib.parse import urljoin

    links = []
    for a in soup.find_all("a", href=True):
        absolute = urljoin(base_url, a["href"])
        links.append(absolute)
    return links


def extract_tables(soup: BeautifulSoup) -> list[list[list[str]]]:
    tables = []
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append(cells)
        tables.append(rows)
    return tables


async def scrape_url(url: str, mode: str = "main_text") -> ExtractedContent:
    async with httpx.AsyncClient(headers=HEADERS, timeout=30.0, follow_redirects=True) as client:
        html = await fetch_page(url, client)

    if not html:
        return ExtractedContent(url=url, error="empty response")

    if mode == "main_text":
        result = extract_main_content(html, url)
        return result or ExtractedContent(url=url, error="extraction failed")
    elif mode == "full_html":
        return ExtractedContent(url=url, text=html)
    elif mode == "links":
        soup = parse_html(html)
        links = extract_links(soup, url)
        return ExtractedContent(url=url, text="\n".join(links))
    elif mode == "tables":
        soup = parse_html(html)
        tables = extract_tables(soup)
        text_blocks = []
        for table in tables:
            for row in table:
                text_blocks.append(" | ".join(row))
        return ExtractedContent(url=url, text="\n".join(text_blocks))
    return ExtractedContent(url=url, error=f"unknown mode: {mode}")


async def scrape_urls(urls: list[str], mode: str = "main_text") -> dict[str, ExtractedContent]:
    results = {}
    async with httpx.AsyncClient(headers=HEADERS, timeout=30.0, follow_redirects=True) as client:
        for url in urls:
            try:
                html = await fetch_page(url, client)
                if not html:
                    results[url] = ExtractedContent(url=url, error="empty response")
                    continue
                extracted = extract_main_content(html, url)
                results[url] = extracted or ExtractedContent(url=url, error="extraction failed")
            except Exception as e:
                results[url] = ExtractedContent(url=url, error=str(e))
    return results
