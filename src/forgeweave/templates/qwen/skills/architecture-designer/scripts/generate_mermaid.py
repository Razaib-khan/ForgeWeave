"""Generate Mermaid.js architecture diagrams from module descriptions."""
import argparse
from pathlib import Path


def generate_diagram(modules: list[dict]) -> str:
    lines = ["graph TD"]
    for mod in modules:
        mod_id = mod.get("id", "").replace(" ", "_").replace("-", "_")
        label = mod.get("name", mod_id)
        lines.append(f"    {mod_id}[\"{label}\"]")

        for dep in mod.get("depends_on", []):
            dep_id = dep.replace(" ", "_").replace("-", "_")
            lines.append(f"    {dep_id} --> {mod_id}")

        for child in mod.get("contains", []):
            child_id = child.replace(" ", "_").replace("-", "_")
            lines.append(f"    {mod_id} --- {child_id}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid architecture diagrams")
    parser.add_argument("--modules", type=Path, required=True, help="JSON file with module definitions")
    parser.add_argument("--output", "-o", type=Path, default=Path("architecture.md"), help="Output file")
    args = parser.parse_args()

    import json
    modules = json.loads(args.modules.read_text())
    diagram = generate_diagram(modules)

    output = f"# Architecture Diagram\n\n```mermaid\n{diagram}\n```\n"
    args.output.write_text(output)
    print(f"Diagram saved to {args.output}")
    print(diagram)


if __name__ == "__main__":
    main()
