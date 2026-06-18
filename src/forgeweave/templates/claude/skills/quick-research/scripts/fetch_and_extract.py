"""Fetch a URL and extract clean text content."""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def fetch_url(url: str, timeout: int = 15) -> tuple[str | None, str | None]:
    try:
        import httpx
        resp = httpx.get(url, timeout=timeout, follow_redirects=True)
        resp.raise_for_status()
        return resp.text, None
    except ImportError:
        return None, "httpx not installed. Run: pip install httpx"
    except Exception as e:
        return None, str(e)


def extract_text(html: str) -> str:
    try:
        import trafilatura
        text = trafilatura.extract(html)
        return text or "<!-- extract failed -->"
    except ImportError:
        stripped = re.sub(r"<[^>]+>", " ", html)
        stripped = re.sub(r"\s+", " ", stripped).strip()
        return stripped[:5000]


def extract_code_blocks(text: str) -> list[str]:
    blocks = re.findall(r"```[\s\S]*?```", text)
    return blocks


def main():
    parser = argparse.ArgumentParser(description="Quick URL fetch and extract")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--output", "-o", type=Path, help="Save output to file")
    parser.add_argument("--code-only", action="store_true", help="Extract only code blocks")
    args = parser.parse_args()

    print(f"Fetching {args.url}...", file=sys.stderr)
    html, error = fetch_url(args.url)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    text = extract_text(html)
    if args.code_only:
        blocks = extract_code_blocks(text)
        output = "\n\n".join(blocks) if blocks else "<!-- no code blocks found -->"
    else:
        output = text

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
