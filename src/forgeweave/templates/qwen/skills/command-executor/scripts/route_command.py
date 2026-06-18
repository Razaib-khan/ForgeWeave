"""Route a /forge-* command to its registered skill pipeline."""

import argparse
import json
from pathlib import Path

DEFAULT_REGISTRY = {
    "forge-start": {"skill": "context-loader", "pipeline": ["context-loader"]},
    "forge-review": {"skill": "validation-engine", "pipeline": ["validation-engine"]},
    "forge-commit": {"skill": "planner", "pipeline": ["planner"]},
    "forge-test": {"skill": "test-generator", "pipeline": ["test-generator"]},
    "forge-research": {
        "skill": "deep-research",
        "pipeline": ["deep-research"],
        "subagents": [
            "research-planner",
            "research-agent",
            "research-validator",
            "research-synthesizer",
        ],
    },
    "forge-docs": {"skill": "code-builder", "pipeline": ["code-builder"]},
    "forge-plan": {"skill": "planner", "pipeline": ["planner"]},
    "forge-debug": {"skill": "debugger", "pipeline": ["debugger"]},
    "forge-refactor": {"skill": "refactor-engine", "pipeline": ["refactor-engine"]},
    "forge-arch": {"skill": "architecture-designer", "pipeline": ["architecture-designer"]},
}


def load_registry(path: Path | None) -> dict:
    if path and path.exists():
        return json.loads(path.read_text())
    return DEFAULT_REGISTRY


def resolve_command(command: str, registry: dict) -> dict | None:
    return registry.get(command)


def main():
    parser = argparse.ArgumentParser(description="Command router")
    parser.add_argument("command", nargs="?", help="The /forge-* command to resolve")
    parser.add_argument("--registry", type=Path, help="Path to command registry JSON")
    parser.add_argument("--list", action="store_true", help="List all registered commands")
    args = parser.parse_args()

    registry = load_registry(args.registry)

    if args.list:
        print("Registered commands:")
        for cmd, info in sorted(registry.items()):
            print(f"  /{cmd} → {info['skill']} ({', '.join(info['pipeline'])})")
        return

    if not args.command:
        parser.print_help()
        return

    resolved = resolve_command(args.command, registry)
    if resolved:
        print(json.dumps(resolved, indent=2))
    else:
        print(f"Command '{args.command}' not found. Use --list to see available commands.")
        import sys

        sys.exit(1)


if __name__ == "__main__":
    main()
