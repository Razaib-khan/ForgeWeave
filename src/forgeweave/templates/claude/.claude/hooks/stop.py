#!/usr/bin/env python3
"""Claude native hook — stop handler (noop in CLI mode)."""

import sys
import json


def main():
    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
