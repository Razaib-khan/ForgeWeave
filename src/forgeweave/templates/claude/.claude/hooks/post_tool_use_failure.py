#!/usr/bin/env python3
"""Claude native hook — logs tool failures for debugging."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    error_log = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": input_data.get("tool_name", ""),
        "error": input_data.get("error", "unknown"),
        "session_id": input_data.get("session_id", ""),
    }

    log_path = Path(".forge/logs/tool_failures.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(error_log) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
