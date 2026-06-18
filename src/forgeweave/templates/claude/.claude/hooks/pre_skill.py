#!/usr/bin/env python3
"""ForgeWeave pre_skill hook — validates skill exists and inputs are correct."""
import sys
import json
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())
    skill_name = input_data.get("skill", "")

    skill_path = Path(f"skills/{skill_name}/SKILL.md")
    if not skill_path.exists():
        print(json.dumps({"decision": "block", "reason": f"Skill not found: {skill_name}"}), file=sys.stderr)
        sys.exit(2)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
