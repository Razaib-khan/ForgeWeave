#!/usr/bin/env python3
"""ForgeWeave post_command hook — logs execution result, stores output in memory."""
import sys
import json
from datetime import datetime


def main():
    input_data = json.loads(sys.stdin.read())

    log_entry = {
        "hook": "post_command",
        "timestamp": datetime.now().isoformat(),
        "tool_name": input_data.get("tool_name", ""),
        "status": input_data.get("status", "completed"),
        "result_preview": json.dumps(input_data.get("result", {})).get("status", "ok"),
    }

    log_path = Path(".forge/logs/command_log.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    from pathlib import Path
    main()
