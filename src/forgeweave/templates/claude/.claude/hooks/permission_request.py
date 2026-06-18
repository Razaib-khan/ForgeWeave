#!/usr/bin/env python3
"""Claude native hook — auto-approves read-only tool requests."""

import sys
import json

READ_ONLY_TOOLS = {"Read", "Glob", "Grep", "List"}


def main():
    input_data = json.loads(sys.stdin.read())
    tool_name = input_data.get("tool_name", "")

    if tool_name in READ_ONLY_TOOLS:
        print(json.dumps({"decision": "approve", "reason": "Read-only tool, auto-approved"}))
        sys.exit(0)

    # For write tools, let Claude's normal permission flow handle it
    print(json.dumps({"decision": "defer"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
