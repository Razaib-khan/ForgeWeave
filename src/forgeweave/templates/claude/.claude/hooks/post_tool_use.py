#!/usr/bin/env python3
"""Claude native hook — logs all tool usage post-execution."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": input_data.get("tool_name", ""),
        "status": "success",
        "session_id": input_data.get("session_id", ""),
    }

    log_path = Path(".forge/logs/tool_usage.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
