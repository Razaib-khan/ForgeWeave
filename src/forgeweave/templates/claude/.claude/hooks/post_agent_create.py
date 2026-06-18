#!/usr/bin/env python3
"""ForgeWeave post_agent_create hook — registers agent in index."""
import sys
import json
from datetime import datetime
from pathlib import Path


def main():
    input_data = json.loads(sys.stdin.read())

    agent_registry_path = Path("agents/.registry.json")
    registry = {}
    if agent_registry_path.exists():
        with open(agent_registry_path) as f:
            registry = json.load(f)

    registry[input_data.get("agent_id", "")] = {
        "path": input_data.get("file_path", ""),
        "created_at": datetime.now().isoformat(),
        "tui": input_data.get("tui", "claude"),
    }

    with open(agent_registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
