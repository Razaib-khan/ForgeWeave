#!/usr/bin/env python3
"""Gemini hook: save session state on exit."""
import sys
import json
from datetime import datetime
from pathlib import Path

def main():
    data = json.loads(sys.stdin.read())
    record = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_end",
        "session_id": data.get("session_id", ""),
    }
    log_path = Path(".forge/logs/sessions.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(record) + "\n")
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
