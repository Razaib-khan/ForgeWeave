#!/usr/bin/env python3
"""ForgeWeave post_file_write hook — formats code, logs change."""
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())
    path = Path(input_data.get("path", ""))

    change_log = Path(".forge/logs/file_changes.jsonl")
    change_log.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "hook": "post_file_write",
        "timestamp": datetime.now().isoformat(),
        "path": str(path),
    }

    with open(change_log, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Auto-format Python files
    if path.suffix == ".py":
        try:
            subprocess.run(["ruff", "format", str(path)], capture_output=True, timeout=10)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
