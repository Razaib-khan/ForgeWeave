"""Concurrent polite web crawler — aiohttp + asyncio + rate limiting.

Skill used: async-crawler
Pattern: aiohttp ClientSession with TCPConnector limits, per-domain RateLimiter,
         asyncio.Semaphore for concurrency control, tenacity retry with backoff
"""

import asyncio
import time
from collections import defaultdict

import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

HEADERS = {
    "User-Agent": "ResearchBot/1.0 (research crawler; research@forgeweave.dev)",
    "Accept": "text/html,application/xhtml+xml",
}


class RateLimiter:
    def __init__(self, default_delay: float = 0.5):
        self.delays: dict[str, float] = defaultdict(lambda: default_delay)
        self.last_fetched: dict[str, float] = {}

    async def wait(self, domain: str) -> None:
        delay = self.delays[domain]
        last = self.last_fetched.get(domain, 0.0)
        elapsed = time.monotonic() - last
        if elapsed < delay:
            await asyncio.sleep(delay - elapsed)
        self.last_fetched[domain] = time.monotonic()

    def set_delay(self, domain: str, delay: float) -> None:
        self.delays[domain] = delay


class Crawler:
    def __init__(self, max_concurrency: int = 10, rate_limit: float = 0.5):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.rate_limiter = RateLimiter(default_delay=rate_limit)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10,
            ttl_dns_cache=300,
            force_close=False,
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=HEADERS,
            timeout=aiohttp.ClientTimeout(total=30, connect=10),
        )
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def _fetch(self, url: str) -> str:
        from urllib.parse import urlparse

        assert self.session is not None
        domain = urlparse(url).netloc
        async with self.semaphore:
            await self.rate_limiter.wait(domain)
            async with self.session.get(url) as resp:
                resp.raise_for_status()
                return await resp.text()

    async def _fetch_one(self, url: str) -> str:
        try:
            return await self._fetch(url)
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                return ""
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to fetch {url}: {e}") from e

    async def crawl_many(self, urls: list[str]) -> dict[str, str]:
        results: dict[str, str] = {}
        async with asyncio.TaskGroup() as tg:
            tasks = {url: tg.create_task(self._fetch_one(url)) for url in urls}
        for url, task in tasks.items():
            try:
                results[url] = task.result()
            except Exception as e:
                results[url] = f"ERROR: {e}"
        return results
