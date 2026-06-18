#!/usr/bin/env python3
"""ForgeWeave research_complete hook — triggers final synthesis, marks job done."""

import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    completion = {
        "hook": "research_complete",
        "timestamp": datetime.now().isoformat(),
        "subtopics": input_data.get("subtopics", []),
        "sources_used": input_data.get("sources_used", 0),
        "total_chars": input_data.get("total_chars", 0),
        "status": "completed",
    }

    job_log = Path("research/.job_log.jsonl")
    job_log.parent.mkdir(exist_ok=True)
    with open(job_log, "a") as f:
        f.write(json.dumps(completion) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
