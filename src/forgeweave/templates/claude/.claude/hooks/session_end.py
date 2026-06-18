#!/usr/bin/env python3
"""Claude native hook — saves session memory on exit."""
import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    session_record = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_end",
        "session_id": input_data.get("session_id", ""),
    }

    log_path = Path(".forge/logs/sessions.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(session_record) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
