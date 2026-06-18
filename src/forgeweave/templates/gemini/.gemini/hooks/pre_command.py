#!/usr/bin/env python3
"""Gemini hook: pre-command validation for /forge-* commands."""

import sys
import json
from pathlib import Path


def main():
    data = json.loads(sys.stdin.read())
    command = data.get("tool_input", {}).get("command", "")

    if command.strip().startswith("/forge-"):
        registry = Path(".forge/command_registry.json")
        if not registry.exists():
            print(json.dumps({"decision": "deny", "reason": "Forge not initialized"}))
            sys.exit(0)

        with open(registry) as f:
            reg = json.load(f)
        cmd_name = command.split()[0].lstrip("/")
        if cmd_name not in reg.get("commands", {}):
            print(json.dumps({"decision": "deny", "reason": f"Unknown: {cmd_name}"}))
            sys.exit(0)

    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
