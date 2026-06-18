#!/usr/bin/env python3
"""Gemini hook: protect sensitive paths before file writes."""

import sys
import json

PROTECTED = [".gemini/settings.json", ".forge/", "AGENTS.md", ".env"]


def main():
    data = json.loads(sys.stdin.read())
    path = data.get("tool_input", {}).get("path", "")
    for protected in PROTECTED:
        if path == protected or path.startswith(protected):
            print(json.dumps({"decision": "deny", "reason": f"Protected: {protected}"}))
            sys.exit(0)
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
