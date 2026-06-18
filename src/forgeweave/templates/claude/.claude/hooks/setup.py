#!/usr/bin/env python3
"""ForgeWeave setup hook — runs on repo init to prepare hook environment."""

import sys
import json
import subprocess
from pathlib import Path


def main():
    """Ensure hook dependencies are available."""
    try:
        subprocess.run(["python3", "--version"], capture_output=True, timeout=5)
    except FileNotFoundError, subprocess.TimeoutExpired:
        print("Error: Python 3 required for ForgeWeave hooks", file=sys.stderr)
        sys.exit(1)

    hooks_dir = Path(".claude/hooks")
    for hook_file in hooks_dir.rglob("*.py"):
        hook_file.chmod(0o755)

    validators_dir = hooks_dir / "validators"
    if validators_dir.exists():
        for v in validators_dir.rglob("*.py"):
            v.chmod(0o755)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
