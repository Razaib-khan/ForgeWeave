#!/usr/bin/env python3
"""ForgeWeave pre_command hook — runs before /forge-* commands.

Loads context, validates command exists in registry, prepares environment.
Exit 0 = allow, Exit 2 = block with stderr.
"""

import sys
import json
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    command = input_data.get("command", "")
    if not command.startswith("/forge-"):
        print(json.dumps({"decision": "approve"}))
        sys.exit(0)

    # Verify command exists in registry
    registry_path = Path(".forge/command_registry.json")
    if not registry_path.exists():
        print(
            json.dumps(
                {"decision": "block", "reason": "Forge not initialized — run forge.init first"}
            ),
            file=sys.stderr,
        )
        sys.exit(2)

    with open(registry_path) as f:
        registry = json.load(f)

    cmd_name = command.split()[0].lstrip("/")
    if cmd_name not in registry.get("commands", {}):
        available = list(registry.get("commands", {}).keys())
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": f"Unknown command: {cmd_name}. Available: {available}",
                }
            ),
            file=sys.stderr,
        )
        sys.exit(2)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
