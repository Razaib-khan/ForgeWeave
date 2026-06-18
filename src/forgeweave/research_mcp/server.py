"""FastMCP server that exposes Deep Research tools.

Skill used: fastmcp-architect
Pattern: FastMCP instance with @mcp.tool decorators, type-annotated functions
         with docstrings, Pydantic return types for automatic schema generation,
         if __name__ == "__main__": mcp.run() entry point
"""

import logging
import sys
from pathlib import Path

from fastmcp import FastMCP

from forgeweave.research_mcp.browser import browser_scrape, browser_screenshot
from forgeweave.research_mcp.cache import cache_stats, cached_fetch
from forgeweave.research_mcp.crawler import Crawler
from forgeweave.research_mcp.documents import extract_document
from forgeweave.research_mcp.models import ExtractedContent, DocumentMetadata, ResearchReport, ResearchSummary
from forgeweave.research_mcp.scraper import extract_main_content, fetch_page, parse_html
from forgeweave.research_mcp.vectors import (
    collection_stats,
    delete_documents,
    index_document,
    index_documents,
    search_documents,
    warmup,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(message)s",
    datefmt="%m/%d/%y %H:%M:%S",
    stream=sys.stderr,
)

log = logging.getLogger("research-mcp")

mcp = FastMCP("Deep Research")

log.info("Initializing ChromaDB...")
warmup()
log.info("Server initialized — 10 tools + 1 deprecated (research_deep_research)")


@mcp.tool
async def research_single_source(url: str, mode: str = "main_text") -> ExtractedContent:
    """Fetch a single URL and extract clean readable content.

    Args:
        url: The web page URL to fetch.
        mode: Extraction mode — 'main_text' (clean article), 'full_html', 'links', or 'tables'.
    """
    import httpx
    log.info(f"Fetching single source: {url} (mode={mode})")
    headers = {
        "User-Agent": "ResearchBot/1.0",
        "Accept": "text/html,application/xhtml+xml",
    }
    async with httpx.AsyncClient(headers=headers, timeout=30.0, follow_redirects=True) as client:
        html = await fetch_page(url, client)
    if not html:
        log.warning(f"Empty response from {url}")
        return ExtractedContent(url=url, error="empty response or 404")

    if mode == "main_text":
        result = extract_main_content(html, url)
        if result:
            log.info(f"Extracted {len(result.text or '')} chars from {url}")
        else:
            log.warning(f"Extraction failed for {url}")
        return result or ExtractedContent(url=url, error="content extraction failed")

    soup = parse_html(html)
    if mode == "links":
        from urllib.parse import urljoin
        links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
        log.info(f"Found {len(links)} links on {url}")
        return ExtractedContent(url=url, text="\n".join(links))
    if mode == "tables":
        rows = []
        for table in soup.find_all("table"):
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                rows.append(" | ".join(cells))
        log.info(f"Extracted {len(rows)} table rows from {url}")
        return ExtractedContent(url=url, text="\n".join(rows))

    log.info(f"Returning {len(html)} chars of raw HTML from {url}")
    return ExtractedContent(url=url, text=html)


@mcp.tool
async def research_crawl_urls(
    urls: list[str],
    max_concurrency: int = 5,
    rate_limit: float = 1.0,
) -> str:
    """Crawl multiple URLs concurrently with polite rate limiting, then extract content.

    Args:
        urls: List of URLs to crawl.
        max_concurrency: Maximum concurrent requests (default 5).
        rate_limit: Minimum seconds between requests per domain (default 1.0).
    """
    log.info(f"Crawling {len(urls)} URLs (concurrency={max_concurrency}, rate={rate_limit}s)")
    async with Crawler(max_concurrency=max_concurrency, rate_limit=rate_limit) as crawler:
        raw_results = await crawler.crawl_many(urls)

    ok_count = sum(1 for v in raw_results.values() if not v.startswith("ERROR"))
    log.info(f"Crawl complete — {ok_count}/{len(urls)} OK, {len(urls)-ok_count} failed")

    report_lines = [f"Crawled {len(urls)} URLs ({len(raw_results)} results):"]
    for url, content in raw_results.items():
        if content.startswith("ERROR"):
            report_lines.append(f"  FAIL {url}: {content}")
        else:
            title = "?"
            try:
                soup = parse_html(content)
                t = soup.title
                title = t.get_text(strip=True) if t else "untitled"
            except Exception:
                pass
            report_lines.append(f"  OK   {url} — {title} ({len(content)} chars)")
    return "\n".join(report_lines)


@mcp.tool
async def research_browse_js(url: str, screenshot: bool = False) -> str:
    """Fetch a JavaScript-rendered page using Playwright headless browser.

    Args:
        url: The URL to render.
        screenshot: If True, capture a full-page screenshot (base64 encoded).
    """
    log.info(f"Browsing JS-rendered page: {url} (screenshot={screenshot})")
    result = await browser_scrape(url, screenshot=screenshot)
    if "error" in result:
        log.warning(f"Browser error for {url}: {result['error']}")
        return f"Error browsing {url}: {result['error']}"
    lines = [f"Title: {result.get('title', '')}", f"URL: {url}", "", "Body text:"]
    text = result.get("text", "")
    lines.append(text[:5000] if len(text) > 5000 else text)
    if screenshot and result.get("screenshot"):
        lines.append("")
        lines.append(f"[Screenshot available: {len(result['screenshot'])} bytes base64]")
    log.info(f"Browser scrape of {url} returned {len(text)} chars")
    return "\n".join(lines)


@mcp.tool
async def research_screenshot(url: str) -> str:
    """Take a full-page screenshot of a URL.

    Args:
        url: The URL to screenshot.
    """
    log.info(f"Taking screenshot of {url}")
    result = await browser_screenshot(url)
    if "error" in result:
        log.warning(f"Screenshot error for {url}: {result['error']}")
        return f"Error: {result['error']}"
    b64_len = len(result.get("screenshot_base64", ""))
    log.info(f"Screenshot of {url} — {b64_len} bytes base64")
    return f"[Screenshot of {url}] — Title: {result.get('title', '')} — Base64 ({b64_len} bytes)"


@mcp.tool
async def research_extract_document(filepath: str) -> str:
    """Extract text from a PDF, DOCX, or other document file.

    Args:
        filepath: Path to the document file.
    """
    path = Path(filepath)
    if not path.exists():
        return f"Error: file not found: {filepath}"
    log.info(f"Extracting document: {filepath}")
    try:
        result = extract_document(filepath)
        text = result.get("text", "")
        if len(text) > 10000:
            text = text[:10000] + "\n\n...[truncated]"
        meta = result.get("metadata", {})
        meta_str = f"Metadata: {meta}" if meta else ""
        log.info(f"Extracted {len(result.get('text', ''))} chars from {path.name}")
        return f"Document: {path.name}\n{meta_str}\n\n{text}"
    except ValueError as e:
        log.error(f"Document extraction failed: {e}")
        return f"Error: {e}"
    except Exception as e:
        log.error(f"Document extraction error: {e}")
        return f"Error extracting document: {e}"


@mcp.tool
async def research_index_latest(
    url: str,
    title: str = "",
    date: str = "",
) -> str:
    """Fetch a URL, extract its content, and index it into the vector database.

    Args:
        url: URL to fetch and index.
        title: Optional title override.
        date: Optional date string (YYYY-MM-DD).
    """
    import httpx
    log.info(f"Indexing: {url}")
    headers = {
        "User-Agent": "ResearchBot/1.0",
        "Accept": "text/html,application/xhtml+xml",
    }
    async with httpx.AsyncClient(headers=headers, timeout=30.0, follow_redirects=True) as client:
        html = await fetch_page(url, client)

    if not html:
        log.warning(f"Failed to fetch {url}")
        return f"Failed to fetch {url}"
    content = extract_main_content(html, url)
    if not content or not content.text:
        log.warning(f"Failed to extract content from {url}")
        return f"Failed to extract content from {url}"

    doc_title = title or content.title or url
    index_document(
        url=url,
        title=doc_title,
        text=content.text,
        source=url.split("/")[2],
        date=date or content.date or "",
    )
    stats = collection_stats()
    log.info(f"Indexed '{doc_title}' ({len(content.text)} chars). DB now has {stats['count']} docs")
    return f"Indexed: {doc_title} ({len(content.text)} chars). Total documents: {stats['count']}"


@mcp.tool
async def research_search(query: str, n_results: int = 5, source_filter: str | None = None) -> str:
    """Search indexed documents by semantic meaning.

    Args:
        query: Natural language search query.
        n_results: Number of results to return (default 5, max 20).
        source_filter: Optional source domain filter (e.g., 'arxiv.org').
    """
    log.info(f"Searching: '{query}' (n={n_results}, source_filter={source_filter})")
    where = None
    if source_filter:
        where = {"source": source_filter}

    results = search_documents(query, n_results=min(n_results, 20), where=where)
    if not results:
        log.info("Search returned no results")
        return "No matching documents found."

    log.info(f"Search returned {len(results)} results")
    lines = [f"Search results for: {query}", ""]
    for i, r in enumerate(results, 1):
        meta = r.get("metadata", {}) or {}
        title = meta.get("title", "untitled")
        source = meta.get("source", "?")
        text = r.get("text", "")[:300]
        lines.append(f"{i}. [{source}] {title}")
        lines.append(f"   {text}...")
        lines.append("")
    return "\n".join(lines)


@mcp.tool
async def research_synthesize(
    query: str,
    n_sources: int = 5,
    source_filter: str | None = None,
) -> ResearchReport:
    """Search indexed documents and return them grouped by relevance.

    The agent running the TUI handles synthesis/reasoning on the returned sources.

    Args:
        query: Research question or topic.
        n_sources: Number of source documents to return (default 5).
        source_filter: Optional source domain filter (e.g., 'arxiv.org').
    """
    log.info(f"Synthesizing sources for: '{query}' (n={n_sources})")
    where = None
    if source_filter:
        where = {"source": source_filter}

    results = search_documents(query, n_results=n_sources, where=where)
    if not results:
        log.info("No sources found for synthesis")
        return ResearchReport(
            query=query,
            summary=ResearchSummary(title="No Sources Found", key_findings=[], confidence=0.0),
            sources=[],
            total_sources_used=0,
        )

    sources_meta = []
    for r in results:
        meta = r.get("metadata", {}) or {}
        sources_meta.append(DocumentMetadata(
            doc_id=r.get("doc_id", ""),
            url=meta.get("url", ""),
            title=meta.get("title", "untitled"),
            source=meta.get("source", ""),
            text_preview=r.get("text", "")[:1000],
        ))

    log.info(f"Gathered {len(sources_meta)} sources for synthesis")
    return ResearchReport(
        query=query,
        summary=ResearchSummary(
            title="Sources gathered",
            key_findings=[f"Found {len(sources_meta)} relevant sources"],
            confidence=1.0,
            sources_used=[s.url for s in sources_meta],
        ),
        sources=sources_meta,
        total_sources_used=len(sources_meta),
    )


@mcp.tool
async def research_deep_research(
    topic: str,
    urls: list[str] | None = None,
    max_concurrency: int = 3,
    rate_limit: float = 1.5,
) -> ResearchReport | dict:
    """[DEPRECATED] Use forge.research instead.

    This tool bundles pipeline logic into a single MCP tool, which
    violates the ForgeWeave design principle: "Expose capabilities,
    hide orchestration." Use forge.research (from the forge-mcp server)
    which runs the full 5-stage pipeline but exposes a clean interface.

    Args:
        topic: The research topic or question.
        urls: Seed URLs to crawl and analyze.
        max_concurrency: Maximum concurrent requests (default 3).
        rate_limit: Minimum seconds between requests per domain (default 1.5).
    """
    log.warning(f"[DEPRECATED] research_deep_research called for '{topic}'. Use forge.research instead.")
    if not urls:
        return {"status": "deprecated", "message": "This tool is deprecated. Use forge.research (from forge-mcp server) for all research needs.", "replacement": "forge.research"}
    log.info(f"=== DEEP RESEARCH STARTED ===")
    log.info(f"Topic: {topic}")
    log.info(f"Seed URLs: {len(urls)}")
    log.info(f"Concurrency: {max_concurrency}, Rate limit: {rate_limit}s")

    all_content: list[dict] = []

    async with Crawler(max_concurrency=max_concurrency, rate_limit=rate_limit) as crawler:
        log.info("Phase 1: Crawling seed URLs...")
        raw_results = await crawler.crawl_many(urls)

    for url, raw_html in raw_results.items():
        if raw_html.startswith("ERROR"):
            log.warning(f"  FAILED: {url} — {raw_html}")
            all_content.append({"url": url, "title": "", "text": "", "error": raw_html, "source": ""})
            continue

        content = extract_main_content(raw_html, url)
        if content and content.text:
            source = url.split("/")[2]
            title = content.title or url
            log.info(f"  EXTRACTED: {title} ({len(content.text)} chars)")
            index_document(
                url=url,
                title=title,
                text=content.text,
                source=source,
                date=content.date or "",
            )
            all_content.append({
                "url": url,
                "title": title,
                "text": content.text,
                "error": None,
                "source": source,
            })
        else:
            log.warning(f"  NO CONTENT: {url}")
            all_content.append({"url": url, "title": "", "text": "", "error": "extraction failed", "source": ""})

    total_chars = sum(len(c["text"]) for c in all_content)
    indexed_count = sum(1 for c in all_content if c["text"])
    failed_count = sum(1 for c in all_content if c["error"])

    log.info(f"Phase 2: Complete")
    log.info(f"  Total URLs: {len(urls)}")
    log.info(f"  Successfully indexed: {indexed_count}")
    log.info(f"  Failed: {failed_count}")
    log.info(f"  Total content: {total_chars} chars")

    stats = collection_stats()
    log.info(f"  Vector DB now has {stats['count']} documents")

    source_docs = [
        DocumentMetadata(
            doc_id="",
            url=c["url"],
            title=c["title"] or "untitled",
            source=c["source"],
            text_preview=(c["text"] or "")[:1000],
        )
        for c in all_content
    ]

    log.info(f"=== DEEP RESEARCH COMPLETE ===")

    return ResearchReport(
        query=topic,
        summary=ResearchSummary(
            title=f"Deep Research: {topic}",
            key_findings=[
                f"Crawled {len(urls)} URLs, successfully indexed {indexed_count}",
                f"Total content extracted: {total_chars} characters",
                f"Vector database contains {stats['count']} documents",
            ],
            confidence=1.0,
            sources_used=[c["url"] for c in all_content if c["text"]],
        ),
        sources=source_docs,
        total_sources_used=indexed_count,
    )


@mcp.tool
async def research_vector_stats() -> str:
    """Show statistics about the vector database (document count, cache usage)."""
    vs = collection_stats()
    cs = cache_stats()
    return (
        f"Vector store: {vs['count']} documents in '{vs['name']}'\n"
        f"HTTP cache: {cs['http']['count']} entries ({cs['http']['volume_mb']} MB, "
        f"{cs['http']['hits']} hits / {cs['http']['misses']} misses)\n"
        f"LLM cache: {cs['llm']['count']} entries ({cs['llm']['volume_mb']} MB, "
        f"{cs['llm']['hits']} hits / {cs['llm']['misses']} misses)"
    )


@mcp.tool
async def research_clear_cache() -> str:
    """Clear HTTP and LLM caches to force fresh fetches and recomputation."""
    from forgeweave.research_mcp.cache import http_cache, llm_cache
    http_count = len(http_cache)
    llm_count = len(llm_cache)
    http_cache.clear()
    llm_cache.clear()
    log.info(f"Cleared {http_count} HTTP + {llm_count} LLM cache entries")
    return f"Cleared {http_count} HTTP cache entries and {llm_count} LLM cache entries."


@mcp.resource("research://stats")
def stats_resource() -> str:
    """Current research database statistics."""
    vs = collection_stats()
    return f"Documents indexed: {vs['count']}"


def main(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.getLogger().setLevel(level)
    log.setLevel(level)
    log.info("MCP server ready on transport 'stdio'")
    mcp.run()


if __name__ == "__main__":
    main()
