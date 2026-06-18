"""Check research markdown for source traceability and structure."""
import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = ["overview", "sources", "core content"]


def check_file(file_path: Path) -> dict:
    issues = []
    if not file_path.exists():
        return {"file": str(file_path), "pass": False, "issues": ["File not found"]}

    content = file_path.read_text(encoding="utf-8")

    # Check sections
    found_sections = re.findall(r"^## (.+)$", content, re.MULTILINE)
    found_lower = [s.strip().lower() for s in found_sections]
    for req in REQUIRED_SECTIONS:
        if not any(req in s for s in found_lower):
            issues.append(f"Missing required section: {req}")

    # Check code blocks have language annotations
    code_blocks = re.findall(r"```(\w*)\n", content)
    for i, lang in enumerate(code_blocks):
        if not lang:
            issues.append(f"Code block {i+1} missing language annotation")

    # Check source URLs
    urls = re.findall(r"https?://[^\s)]+", content)
    if not urls:
        issues.append("No source URLs found in document")

    # Check for placeholders
    placeholders = re.findall(r"<!--.+?-->|TODO|FIXME", content)
    if placeholders:
        issues.append(f"Contains {len(placeholders)} placeholder(s) (TODOs, comments)")

    return {
        "file": str(file_path),
        "pass": len(issues) == 0,
        "issues": issues,
        "sections": len(found_sections),
        "code_blocks": len(code_blocks),
        "sources": len(urls),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate research outputs")
    parser.add_argument("files", nargs="+", type=Path, help="Files to validate")
    parser.add_argument("--strict", action="store_true", help="Fail on any warning")
    args = parser.parse_args()

    all_pass = True
    for f in args.files:
        result = check_file(f)
        status = "PASS" if result["pass"] else "FAIL"
        print(f"[{status}] {f.name}")
        if result["pass"]:
            print(f"       {result['sections']} sections, {result['code_blocks']} code blocks, {result['sources']} sources")
        else:
            for issue in result["issues"]:
                print(f"       ! {issue}")
            all_pass = False

    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
