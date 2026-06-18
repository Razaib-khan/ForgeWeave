#!/usr/bin/env python3
"""ForgeWeave research_iteration hook — checks sufficiency, prevents infinite loops."""
import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())
    iteration = input_data.get("iteration", 0)
    subtopics_completed = input_data.get("subtopics_completed", 0)
    subtopics_total = input_data.get("subtopics_total", 1)

    if iteration > 10:
        print(json.dumps({"decision": "block", "reason": "Max iterations (10) reached. Stopping research."}), file=sys.stderr)
        sys.exit(2)

    progress = subtopics_completed / subtopics_total if subtopics_total > 0 else 0

    result = {
        "decision": "approve",
        "continue": progress < 1.0,
        "progress_pct": int(progress * 100),
    }

    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
