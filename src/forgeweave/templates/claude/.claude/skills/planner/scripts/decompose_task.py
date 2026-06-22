"""Decompose a task into ordered, actionable steps."""

import argparse
import json
from pathlib import Path


def decompose(goal: str) -> dict:
    return {
        "goal": goal,
        "steps": [],
        "dependencies": [],
        "risks": [],
        "complexity": "unknown",
        "status": "draft",
    }


def validate_plan(plan: dict) -> list[str]:
    errors = []
    if not plan.get("steps"):
        errors.append("Plan must have at least 1 step")
    seen = set()
    for i, step in enumerate(plan.get("steps", [])):
        if not step.get("action"):
            errors.append(f"Step {i} missing 'action'")
        desc = step.get("action", "")
        if desc in seen:
            errors.append(f"Duplicate step: {desc}")
        seen.add(desc)
    return errors


def save_plan(plan: dict, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"# Execution Plan: {plan['goal']}\n\n"
        f"**Complexity:** {plan['complexity']}  \n\n"
        f"## Steps\n"
        + "\n".join(
            f"{i + 1}. **{s.get('action')}**"
            + (f" (uses: {', '.join(s.get('tools', []))})" if s.get("tools") else "")
            for i, s in enumerate(plan["steps"])
        )
        + "\n\n## Dependencies\n"
        + "\n".join(f"- {d}" for d in plan.get("dependencies", []))
        + "\n\n## Risks\n"
        + "\n".join(f"- {r}" for r in plan.get("risks", []))
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser(description="Task decomposer")
    parser.add_argument("goal", help="The goal to decompose")
    parser.add_argument("--output", "-o", type=Path, default=Path("plan.md"))
    args = parser.parse_args()

    plan = decompose(args.goal)
    save_plan(plan, args.output)
    print(f"Plan skeleton saved to {args.output}")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
