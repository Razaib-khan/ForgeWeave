#!/usr/bin/env python3
"""ForgeWeave pre_research hook — creates job entry, validates constraints."""
import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())
    topic = input_data.get("topic", "")
    depth = input_data.get("depth", "standard")

    if not topic or len(topic.strip()) < 10:
        print(json.dumps({"decision": "block", "reason": "Topic too vague. Provide at least 10 characters."}), file=sys.stderr)
        sys.exit(2)

    research_dir = Path("research")
    research_dir.mkdir(exist_ok=True)

    job_entry = {
        "hook": "pre_research",
        "topic": topic,
        "depth": depth,
        "timestamp": datetime.now().isoformat(),
        "status": "initialized",
    }

    job_log = research_dir / ".job_log.jsonl"
    with open(job_log, "a") as f:
        f.write(json.dumps(job_entry) + "\n")

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
