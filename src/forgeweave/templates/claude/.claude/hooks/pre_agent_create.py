#!/usr/bin/env python3
"""ForgeWeave pre_agent_create hook — validates agent schema, prevents duplicates."""

import sys
import json
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())
    agent_id = input_data.get("agent_id", "")

    if not agent_id or not agent_id.replace("-", "").isalnum():
        print(
            json.dumps({"decision": "block", "reason": "agent_id must be kebab-case alphanumeric"}),
            file=sys.stderr,
        )
        sys.exit(2)

    # Check for duplicates across all TUI agent dirs
    for pattern in ["agents/*.md", "agents/*.yaml", "agents/**/*.md"]:
        for f in Path(".").glob(pattern):
            if f.stem == agent_id:
                print(
                    json.dumps({"decision": "block", "reason": f"Duplicate agent_id: {agent_id}"}),
                    file=sys.stderr,
                )
                sys.exit(2)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
