"""Merge validated research files into a structured final report."""
import argparse
from pathlib import Path


SECTION_ORDER = [
    "overview",
    "getting started",
    "setup",
    "core content",
    "advanced patterns",
    "migration guide",
    "best practices",
    "edge cases",
    "sources",
]


def merge_sections(files: list[Path]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    for f in files:
        content = f.read_text(encoding="utf-8")
        current_section = "other"
        for line in content.split("\n"):
            if line.startswith("## "):
                current_section = line.strip("## ").strip().lower()
                sections.setdefault(current_section, [])
            else:
                sections.setdefault(current_section, []).append(line)
    return sections


def write_report(sections: dict[str, list[str]], output: Path, topic: str):
    lines = [f"# {topic}\n", "\n"]
    for section_name in SECTION_ORDER:
        matched = None
        for key in sections:
            if section_name in key:
                matched = key
                break
        if matched:
            lines.append(f"## {matched.title()}\n")
            lines.extend(sections[matched])
            lines.append("\n")
        else:
            lines.append(f"## {section_name.title()}\n")
            lines.append("<!-- TODO: Content from research -->\n\n")

    lines.append("## Sources\n")
    all_urls = set()
    for content_list in sections.values():
        for line in content_list:
            import re
            for url in re.findall(r"https?://[^\s)]+", line):
                all_urls.add(url.rstrip(".").rstrip(")"))
    for url in sorted(all_urls):
        lines.append(f"- {url}\n")

    output.write_text("".join(lines), encoding="utf-8")


def main():
    import re
    parser = argparse.ArgumentParser(description="Synthesize research report")
    parser.add_argument("--input", nargs="+", type=Path, help="Validated research files")
    parser.add_argument("--output", type=Path, required=True, help="Output report path")
    parser.add_argument("--topic", default="Research Report", help="Report topic")
    args = parser.parse_args()

    if args.input:
        sections = merge_sections(args.input)
    else:
        validated_dir = args.output.parent / f"{args.output.stem.replace('-report', '-validated')}.md"
        if validated_dir.exists():
            sections = merge_sections([validated_dir])
        else:
            sections = {}

    write_report(sections, args.output, args.topic)
    print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()
