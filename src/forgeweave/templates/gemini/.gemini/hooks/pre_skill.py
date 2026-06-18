#!/usr/bin/env python3
"""Gemini hook: inject forge context before agent starts."""
import sys
import json
from pathlib import Path

def main():
    ctx = ["[ForgeWeave Project Context]"]
    for d in ["agents", "skills", "commands"]:
        p = Path(d)
        if p.exists():
            items = [x.name for x in p.iterdir() if x.is_dir() or x.suffix in (".md", ".yaml")]
            ctx.append(f"- {d}: {', '.join(items[:5])}{'...' if len(items) > 5 else ''}")
    print(json.dumps({"decision": "allow", "systemMessage": "\n".join(ctx)}))
    sys.exit(0)

if __name__ == "__main__":
    main()
