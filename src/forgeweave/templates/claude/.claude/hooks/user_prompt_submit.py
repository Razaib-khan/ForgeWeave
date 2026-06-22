#!/usr/bin/env python3
"""Claude native hook — injects project context before every user prompt."""

import sys
import json
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())
    prompt = input_data.get("prompt", "")

    # If prompt starts with /forge-, let the TUI command system handle it
    if prompt.strip().startswith("/forge-"):
        print(json.dumps({"decision": "approve", "context": ""}))
        sys.exit(0)

    # Inject project context for all natural-language prompts
    context_parts = ["[ForgeWeave Context]"]

    agents_dir = Path("agents")
    if agents_dir.exists():
        agent_files = list(agents_dir.glob("*.md")) + list(agents_dir.glob("*.yaml"))
        if agent_files:
            context_parts.append(f"Agents available: {len(agent_files)}")

    skills_dir = Path("skills")
    if skills_dir.exists():
        skill_dirs = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        if skill_dirs:
            context_parts.append(f"Skills available: {len(skill_dirs)}")

    commands_path = Path(".forge/command_registry.json")
    if commands_path.exists():
        with open(commands_path) as f:
            registry = json.load(f)
        commands = list(registry.get("commands", {}).keys())
        if commands:
            context_parts.append(f"Commands: /forge-{' /forge-'.join(commands)}")

    context = "\n".join(context_parts) if len(context_parts) > 1 else ""
    print(json.dumps({"decision": "approve", "context": context}))
    sys.exit(0)


if __name__ == "__main__":
    main()
