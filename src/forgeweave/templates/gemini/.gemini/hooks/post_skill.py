#!/usr/bin/env python3
"""Gemini hook: validate agent output quality."""

import sys
import json


def main():
    data = json.loads(sys.stdin.read())
    output = data.get("output", "")
    if len(output.strip()) < 20:
        print(
            json.dumps({"decision": "allow", "systemMessage": "Warning: Output seems too brief."})
        )
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
