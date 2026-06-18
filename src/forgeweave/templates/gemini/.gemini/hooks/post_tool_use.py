#!/usr/bin/env python3
"""Gemini hook: record interactions for traceability."""
import sys
import json
from datetime import datetime
from pathlib import Path

def main():
    data = json.loads(sys.stdin.read())
    log = {
        "timestamp": datetime.now().isoformat(),
        "tool": data.get("tool_name", ""),
        "status": data.get("status", "ok"),
    }
    log_path = Path(".forge/logs/interactions.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(log) + "\n")
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
