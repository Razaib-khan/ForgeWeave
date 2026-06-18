"""Caching layer — diskcache for HTTP responses and LLM calls.

Skill used: cache-store
Pattern: diskcache size_limit + FanoutCache memoize + TTL
"""

import hashlib
import json
from collections.abc import Callable
from pathlib import Path

from diskcache import Cache, FanoutCache

HERE = Path(__file__).resolve().parent.parent
HTTP_CACHE_DIR = str(HERE / "cache" / "http")
LLM_CACHE_DIR = str(HERE / "cache" / "llm")

http_cache = Cache(HTTP_CACHE_DIR, size_limit=int(1e9))
llm_cache = FanoutCache(LLM_CACHE_DIR, size_limit=int(2e9))


def cache_key_http(url: str, **kwargs) -> str:
    raw = json.dumps({"url": url, **kwargs}, sort_keys=True)
    return f"http:{hashlib.sha256(raw.encode()).hexdigest()}"


def cached_fetch(url: str, fetch_fn: Callable[[], str], ttl: int = 3600) -> str:
    key = cache_key_http(url)
    if key in http_cache:
        return http_cache[key]
    result = fetch_fn()
    http_cache.set(key, result, expire=ttl)
    return result


def cache_key_llm(prompt: str, model: str, temperature: float = 0.0) -> str:
    raw = json.dumps({"prompt": prompt, "model": model, "temperature": temperature}, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def cached_llm_call(prompt: str, model: str, call_fn: Callable[[], str], ttl: int = 86400) -> str:
    key = cache_key_llm(prompt, model)
    if key in llm_cache:
        return llm_cache[key]
    result = call_fn()
    llm_cache.set(key, result, expire=ttl)
    return result


def cache_stats() -> dict:
    http_stats = http_cache.stats(enable=True)
    llm_stats = llm_cache.stats(enable=True)
    return {
        "http": {
            "volume_mb": round(http_cache.volume() / 1e6, 1),
            "hits": http_stats[0],
            "misses": http_stats[1],
            "count": len(http_cache),
        },
        "llm": {
            "volume_mb": round(llm_cache.volume() / 1e6, 1),
            "hits": llm_stats[0],
            "misses": llm_stats[1],
            "count": len(llm_cache),
        },
    }
