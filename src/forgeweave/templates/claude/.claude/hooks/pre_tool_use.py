#!/usr/bin/env python3
"""Claude native hook — routes PreToolUse to ForgeWeave security guard.

Blocks dangerous commands and sensitive file operations.
"""

import sys
import json
import re


DANGEROUS_PATTERNS = [
    (r"rm\s+.*-[rR]f", "Recursive force-delete blocked"),
    (r"sudo\s+rm", "Sudo delete blocked"),
    (r"chmod\s+777", "World-writable permissions blocked"),
    (r">\s*/etc/", "System file overwrite blocked"),
    (r"\|\s*(sh|bash|zsh)\s*$", "Pipe-to-shell execution blocked"),
    (r":(){ :\|:& };:", "Fork bomb blocked"),
    (r"mkfs|dd\s+if=/dev/zero", "Filesystem destruction blocked"),
]


def main():
    input_data = json.loads(sys.stdin.read())
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Block dangerous bash commands
    if tool_name == "bash":
        command = tool_input.get("command", "")
        for pattern, reason in DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                print(json.dumps({"decision": "block", "reason": f"Security Policy: {reason}"}))
                sys.exit(0)

    # Block .env file access
    if tool_name in ("str_replace_editor", "Read", "Write"):
        path = tool_input.get("path", tool_input.get("file_path", ""))
        if ".env" in path or "secrets" in path.lower() or "credentials" in path.lower():
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": "Security Policy: Sensitive file access blocked",
                    }
                )
            )
            sys.exit(0)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
