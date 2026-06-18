#!/usr/bin/env python3
"""ForgeWeave pre_file_write hook — checks protected paths, validates permissions."""
import sys
import json
from pathlib import Path


PROTECTED_PATHS = [
    ".claude/settings.json",
    ".forge/",
    "AGENTS.md",
    ".env",
    ".env.*",
]

SENSITIVE_PATTERNS = [
    "api_key", "apikey", "API_KEY",
    "password", "PASSWORD",
    "secret", "SECRET",
    "token", "TOKEN",
    "ssh-rsa", "ssh-ed25519",
    "BEGIN PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
]


def main():
    input_data = json.loads(sys.stdin.read())
    path = input_data.get("path", "")

    for protected in PROTECTED_PATHS:
        if protected.endswith("/") and path.startswith(protected):
            print(json.dumps({"decision": "block", "reason": f"Cannot write to protected path: {protected}"}), file=sys.stderr)
            sys.exit(2)
        if path == protected:
            print(json.dumps({"decision": "block", "reason": f"Cannot write to protected file: {protected}"}), file=sys.stderr)
            sys.exit(2)

    content = input_data.get("content", input_data.get("new_string", ""))
    for pattern in SENSITIVE_PATTERNS:
        if pattern in content:
            print(json.dumps({"decision": "block", "reason": f"Sensitive content detected ({pattern})"}), file=sys.stderr)
            sys.exit(2)

    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
