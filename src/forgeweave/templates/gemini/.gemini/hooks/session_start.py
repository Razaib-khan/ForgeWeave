#!/usr/bin/env python3
"""Gemini hook: load project state on session start."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    data = json.loads(sys.stdin.read())
    record = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_start",
        "session_id": data.get("session_id", ""),
    }
    log_path = Path(".forge/logs/sessions.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(record) + "\n")
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
