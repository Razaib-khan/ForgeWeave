"""Persist and retrieve key-value data across sessions."""

import argparse
import json
import os
import sys
from pathlib import Path


def get_cache_dir() -> Path:
    return Path(os.environ.get("FORGE_CACHE_DIR", Path.cwd() / ".forge" / "cache"))


def save(key: str, data: dict, namespace: str = "general"):
    cache_dir = get_cache_dir() / namespace
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{key}.json"
    path.write_text(json.dumps(data, indent=2))
    return str(path)


def load(key: str, namespace: str = "general") -> dict | None:
    path = get_cache_dir() / namespace / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    return None


def search(query: str, namespace: str = "general") -> list[dict]:
    results = []
    cache_dir = get_cache_dir() / namespace
    if not cache_dir.exists():
        return results
    for f in cache_dir.glob("*.json"):
        if query.lower() in f.stem.lower():
            data = json.loads(f.read_text())
            results.append({"key": f.stem, "data": data})
    return results


def clear(namespace: str | None = None):
    if namespace:
        path = get_cache_dir() / namespace
        if path.exists():
            import shutil

            shutil.rmtree(path)
    else:
        path = get_cache_dir()
        if path.exists():
            import shutil

            shutil.rmtree(path)


def main():
    parser = argparse.ArgumentParser(description="Memory/cache manager")
    parser.add_argument("action", choices=["save", "load", "search", "clear"])
    parser.add_argument("--key", help="Cache key")
    parser.add_argument("--data", help="JSON data to save")
    parser.add_argument("--namespace", default="general", help="Namespace")
    parser.add_argument("--query", help="Search query")
    args = parser.parse_args()

    if args.action == "save":
        if not args.key or not args.data:
            print("--key and --data required for save", file=sys.stderr)
            sys.exit(1)
        data = json.loads(args.data)
        path = save(args.key, data, args.namespace)
        print(f"Saved to {path}")

    elif args.action == "load":
        if not args.key:
            print("--key required for load", file=sys.stderr)
            sys.exit(1)
        data = load(args.key, args.namespace)
        if data:
            print(json.dumps(data, indent=2))
        else:
            print(f"Key '{args.key}' not found in namespace '{args.namespace}'")
            sys.exit(1)

    elif args.action == "search":
        results = search(args.query or "", args.namespace)
        if results:
            for r in results:
                print(f"  [{r['key']}] {json.dumps(r['data'])[:100]}")
        else:
            print("No results")

    elif args.action == "clear":
        clear(args.namespace)
        print(f"Cleared {'namespace: ' + args.namespace if args.namespace else 'all caches'}")


if __name__ == "__main__":
    main()
