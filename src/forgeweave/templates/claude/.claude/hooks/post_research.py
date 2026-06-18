#!/usr/bin/env python3
"""ForgeWeave post_research hook — saves final report, updates memory store."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    summary = {
        "hook": "post_research",
        "timestamp": datetime.now().isoformat(),
        "report_path": input_data.get("report_path", ""),
        "plan_path": input_data.get("plan_path", ""),
    }

    summary_path = Path("research/.research_summary.jsonl")
    with open(summary_path, "a") as f:
        f.write(json.dumps(summary) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
