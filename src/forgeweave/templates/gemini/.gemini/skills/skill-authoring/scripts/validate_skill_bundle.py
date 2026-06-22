#!/usr/bin/env python3
"""Validate a ForgeWeave skill bundle against SKILL_SPEC.md requirements.

Usage:
    python validate_skill_bundle.py <path-to-skill-directory>
"""

import argparse
import re
import sys
from pathlib import Path


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    skill_md = path / "SKILL.md"

    if not skill_md.exists():
        errors.append(f"SKILL.md not found at {skill_md}")
        return errors

    content = skill_md.read_text(encoding="utf-8")

    # Check frontmatter exists
    if not content.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter (---)")

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = parts[2].strip()
    else:
        errors.append("Invalid frontmatter: must be delimited by ---")
        return errors

    # Required frontmatter fields
    required_fields = ["skill_id", "name", "version", "description", "author", "tui_compatibility"]
    for field in required_fields:
        if f"{field}:" not in frontmatter:
            errors.append(f"Frontmatter missing required field: '{field}'")

    # Check dir name matches skill_id
    dir_name = path.name
    skill_id_match = re.search(r"skill_id:\s*(\S+)", frontmatter)
    if skill_id_match and skill_id_match.group(1) != dir_name:
        errors.append(
            f"Directory name '{dir_name}' does not match skill_id '{skill_id_match.group(1)}'"
        )

    # Required sections in order
    required_sections = [
        "Purpose",
        "When to Use",
        "When Not to Use",
        "Inputs",
        "Expected Outputs",
        "Exact Workflow Steps",
        "Required Checks",
        "Failure Modes",
        "Examples",
        "References",
    ]

    found_sections = []
    for section in required_sections:
        if f"## {section}" in body:
            found_sections.append(section)
        else:
            errors.append(f"Missing required section: '{section}'")

    # Check section order
    if found_sections:
        ordered = [s for s in required_sections if s in found_sections]
        if found_sections != ordered:
            errors.append(f"Sections out of order. Expected: {ordered}, Found: {found_sections}")

    # Check referenced scripts exist
    script_refs = re.findall(r"scripts/(\S+)", content)
    for ref in script_refs:
        ref_path = path / "scripts" / ref
        if not ref_path.exists():
            errors.append(f"Referenced script 'scripts/{ref}' not found")

    # Check referenced assets exist
    asset_refs = re.findall(r"assets/(\S+)", content)
    for ref in asset_refs:
        ref_path = path / "assets" / ref
        if not ref_path.exists():
            errors.append(f"Referenced asset 'assets/{ref}' not found")

    # Check description length
    desc_match = re.search(r"description:\s*(.+)", frontmatter)
    if desc_match and len(desc_match.group(1)) > 200:
        errors.append(f"Description is {len(desc_match.group(1))} chars (max 200)")

    # Check for placeholder text
    placeholders = re.findall(r"<[A-Z_]+>", body)
    if placeholders:
        errors.append(f"Placeholder text found: {placeholders}. Replace with real content.")

    # Check evals directory
    evals_dir = path / "evals"
    if evals_dir.is_dir() and not list(evals_dir.iterdir()):
        errors.append("evals/ directory exists but is empty — add at least one eval")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a ForgeWeave skill bundle")
    parser.add_argument("path", type=Path, help="Path to the skill directory")
    args = parser.parse_args()

    if not args.path.is_dir():
        print(f"Error: '{args.path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    errors = validate_skill(args.path)
    if errors:
        print(f"Found {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("Skill bundle is valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
