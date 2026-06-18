"""Validate research outputs for source traceability and structure."""
import argparse
import re
import sys
from pathlib import Path


def extract_claims(markdown: str) -> list[dict]:
    claims = []
    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("```"):
            has_source = bool(re.search(r"https?://[^\s)]+", stripped))
            claims.append({"line": i + 1, "text": stripped[:100], "has_source": has_source})
    return claims


def check_file(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    claims = extract_claims(content)
    total = len(claims)
    with_source = sum(1 for c in claims if c["has_source"])
    without_source = [c for c in claims if not c["has_source"]]
    return {
        "file": str(path),
        "total_claims": total,
        "with_source": with_source,
        "without_source_count": len(without_source),
        "unsupported": without_source[:10],
        "source_ratio": with_source / total if total > 0 else 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate research outputs")
    parser.add_argument("files", nargs="+", type=Path, help="Research markdown files to validate")
    parser.add_argument("--threshold", type=float, default=0.8, help="Minimum source ratio (default: 0.8)")
    args = parser.parse_args()

    all_pass = True
    for f in args.files:
        if not f.exists():
            print(f"FAIL: {f} not found", file=sys.stderr)
            all_pass = False
            continue
        result = check_file(f)
        status = "PASS" if result["source_ratio"] >= args.threshold else "FAIL"
        print(f"[{status}] {f.name}: {result['with_source']}/{result['total_claims']} claims sourced ({result['source_ratio']:.0%})")
        if result["source_ratio"] < args.threshold:
            print(f"  First {len(result['unsupported'])} unsupported claims:")
            for c in result["unsupported"]:
                print(f"    Line {c['line']}: {c['text']}")
            all_pass = False

    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
