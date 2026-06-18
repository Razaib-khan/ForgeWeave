#!/usr/bin/env python3
"""Claude native hook — logs subagent completion."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    trace = {
        "timestamp": datetime.now().isoformat(),
        "event": "subagent_stop",
        "subagent_id": input_data.get("subagent_id", ""),
        "status": input_data.get("status", "completed"),
    }

    log_path = Path(".forge/logs/subagent_traces.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(trace) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
