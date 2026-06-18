"""Scaffold a new skill bundle with SKILL.md skeleton and directory structure."""
import argparse
from pathlib import Path


SKILL_SKELETON = """---
skill_id: {skill_id}
name: {name}
version: 1.0.0
description: {description}
author: ForgeWeave Core
tui_compatibility:
  - opencode
  - claude
  - gemini
  - qwen
tags:
  - generated
---

# {name}

## Purpose

<!-- 2-4 sentences describing what problem this skill solves and when to invoke it -->

## When to Use

<!-- Numbered list of exact, testable conditions that trigger this skill -->

## When Not to Use

<!-- Edge cases where this skill looks relevant but should not be used -->

## Inputs

<!-- Table: name, type, required/optional, description -->

## Expected Outputs

<!-- What the skill produces — files, console output, side effects -->

## Exact Workflow Steps

### Step 1: ...
### Step 2: ...

## Required Checks

- [ ] Check 1
- [ ] Check 2

## Failure Modes

| Failure Condition | Response |
|---|---|

## Examples

### Example 1: ...

## References

| Reference | Path |
|---|---|
"""


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new skill bundle")
    parser.add_argument("skill_id", help="Kebab-case skill ID (e.g., 'my-skill')")
    parser.add_argument("--name", help="Human-readable name (default: same as skill_id)")
    parser.add_argument("--description", "-d", default="Generated skill", help="One-line description")
    parser.add_argument("--output", "-o", type=Path, default=Path.cwd(), help="Parent output directory")
    args = parser.parse_args()

    name = args.name or args.skill_id.replace("-", " ").title()
    skill_dir = args.output / args.skill_id
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    for sub in ["scripts", "references", "templates", "examples", "evals"]:
        (skill_dir / sub).mkdir(exist_ok=True)

    # Write SKILL.md
    skill_path = skill_dir / "SKILL.md"
    content = SKILL_SKELETON.format(
        skill_id=args.skill_id,
        name=name,
        description=args.description,
    )
    skill_path.write_text(content.strip())

    print(f"Skill bundle created at {skill_dir}")
    print(f"  SKILL.md — edit this with the 10 required sections")
    print(f"  scripts/ — add automation scripts")
    print(f"  references/ — add knowledge base docs")
    print(f"  templates/ — add scaffolding templates")
    print(f"  examples/ — add worked examples")
    print(f"  evals/ — add validation tests")


if __name__ == "__main__":
    main()
