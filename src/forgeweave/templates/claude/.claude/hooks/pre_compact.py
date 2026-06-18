#!/usr/bin/env python3
"""ForgeWeave pre_compact hook — preserves critical context before compaction."""
import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "event": "pre_compact",
        "session_id": input_data.get("session_id", ""),
        "context_size": input_data.get("context_size", 0),
    }

    log_path = Path(".forge/logs/compactions.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(snapshot) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
