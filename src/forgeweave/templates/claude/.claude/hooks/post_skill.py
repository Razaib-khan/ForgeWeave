#!/usr/bin/env python3
"""ForgeWeave post_skill hook — stores result, generates trace."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    trace_entry = {
        "hook": "post_skill",
        "timestamp": datetime.now().isoformat(),
        "skill": input_data.get("skill", ""),
        "status": input_data.get("status", "completed"),
    }

    trace_path = Path(".forge/logs/skill_traces.jsonl")
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_path, "a") as f:
        f.write(json.dumps(trace_entry) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
