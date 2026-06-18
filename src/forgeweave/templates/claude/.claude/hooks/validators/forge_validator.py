#!/usr/bin/env python3
"""ForgeWeave PostToolUse validator — enforces code quality and structure rules."""
import sys
import json
import subprocess
from pathlib import Path


def validate_python(path: Path) -> list[str]:
    errors = []
    try:
        result = subprocess.run(
            ["ruff", "check", "--quiet", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0 and result.stdout.strip():
            errors.append(f"Ruff: {result.stdout.strip()}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return errors


def validate_markdown(path: Path) -> list[str]:
    errors = []
    content = path.read_text(encoding="utf-8")
    if content.count("```") % 2 != 0:
        errors.append("Markdown: Unmatched code fences")
    if path.name.endswith(".md") and not content.startswith("---"):
        errors.append("Markdown: Missing YAML frontmatter")
    return errors


def validate_agent_file(path: Path) -> list[str]:
    errors = []
    content = path.read_text(encoding="utf-8")
    if "agent_id:" not in content and "---" not in content.split("\n")[0]:
        errors.append(f"Agent file: {path.name} missing agent_id frontmatter")
    return errors


def main():
    input_data = json.loads(sys.stdin.read())
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    path_str = tool_input.get("path", tool_input.get("file_path", ""))
    if not path_str:
        print(json.dumps({"decision": "approve"}))
        sys.exit(0)

    path = Path(path_str)
    if not path.exists():
        print(json.dumps({"decision": "approve"}))
        sys.exit(0)

    errors = []
    if path.suffix == ".py":
        errors.extend(validate_python(path))
    elif path.suffix == ".md":
        errors.extend(validate_markdown(path))
    if path.parent.name == "agents":
        errors.extend(validate_agent_file(path))

    if errors:
        print(json.dumps({
            "decision": "block",
            "reason": "Validation errors:\n" + "\n".join(errors),
        }))
        sys.exit(0)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
