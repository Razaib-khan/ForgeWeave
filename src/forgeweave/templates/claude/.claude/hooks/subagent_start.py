#!/usr/bin/env python3
"""Claude native hook — logs subagent spawns for traceability."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    trace = {
        "timestamp": datetime.now().isoformat(),
        "event": "subagent_start",
        "subagent_id": input_data.get("subagent_id", ""),
        "parent_session": input_data.get("session_id", ""),
    }

    log_path = Path(".forge/logs/subagent_traces.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(trace) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
