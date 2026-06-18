#!/usr/bin/env python3
"""Gemini hook: format code after writes."""
import sys
import json
import subprocess
from pathlib import Path

def main():
    data = json.loads(sys.stdin.read())
    path = Path(data.get("tool_input", {}).get("path", ""))
    if path.suffix == ".py":
        try:
            subprocess.run(["ruff", "format", str(path)], capture_output=True, timeout=10)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
