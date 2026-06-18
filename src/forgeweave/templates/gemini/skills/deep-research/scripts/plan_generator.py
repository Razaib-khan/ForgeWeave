"""Generate a structured research plan from a topic string."""
import argparse
import json
import sys
from pathlib import Path


def slugify(text: str) -> str:
    return text.lower().replace(" ", "-").replace("/", "-")


def generate_plan(topic: str, depth: str = "standard", focus: str = "usage") -> dict:
    slug = slugify(topic)
    return {
        "topic": topic,
        "slug": slug,
        "depth": depth,
        "focus": focus,
        "subtopics": [],
        "execution_strategy": "parallel",
        "status": "draft",
    }


def validate_plan(plan: dict) -> list[str]:
    errors = []
    if len(plan.get("subtopics", [])) < 3:
        errors.append("Plan must have at least 3 subtopics")
    for i, st in enumerate(plan.get("subtopics", [])):
        if not st.get("name"):
            errors.append(f"Subtopics[{i}] missing 'name'")
        if not st.get("seed_urls"):
            errors.append(f"Subtopics[{i}] '{st.get('name')}' missing seed_urls")
        for url in st.get("seed_urls", []):
            if any(bad in url for bad in ["blog", "changelog", "release"]):
                errors.append(f"Subtopics[{i}] contains prohibited URL: {url}")
    return errors


def save_plan(plan: dict, output_dir: str = "research") -> str:
    path = Path(output_dir) / f"{plan['slug']}-plan.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Research Plan: {plan['topic']}\n\n"
        f"**Depth:** {plan['depth']}  \n"
        f"**Focus:** {plan['focus']}  \n"
        f"**Strategy:** {plan['execution_strategy']}  \n\n"
        f"```yaml\n{json.dumps(plan, indent=2)}\n```\n"
    )
    return str(path)


def main():
    parser = argparse.ArgumentParser(description="Generate research plan")
    parser.add_argument("topic", help="Research topic")
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--focus", choices=["usage", "architecture", "comparison", "general"], default="usage")
    parser.add_argument("--output", default="research", help="Output directory")
    parser.add_argument("--validate", metavar="PLAN_JSON", help="Validate an existing plan JSON file")
    args = parser.parse_args()

    if args.validate:
        plan = json.loads(Path(args.validate).read_text())
        errors = validate_plan(plan)
        if errors:
            print("Validation errors:", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            sys.exit(1)
        print("Plan is valid")
        return

    plan = generate_plan(args.topic, args.depth, args.focus)
    path = save_plan(plan, args.output)
    print(f"Plan skeleton saved to {path}")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
