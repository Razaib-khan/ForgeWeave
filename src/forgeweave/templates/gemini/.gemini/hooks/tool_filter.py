#!/usr/bin/env python3
"""Gemini hook: prioritize forge.* tools for forgeweave operations."""
import sys
import json

def main():
    data = json.loads(sys.stdin.read())
    intent = data.get("intent", "")
    tools = data.get("available_tools", [])

    if any(kw in intent.lower() for kw in ["research", "skill", "agent", "memory", "validate", "init"]):
        forge_tools = [t for t in tools if t.startswith("forge.")]
        if forge_tools:
            print(json.dumps({"decision": "allow", "prioritized_tools": forge_tools}))
            sys.exit(0)

    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
