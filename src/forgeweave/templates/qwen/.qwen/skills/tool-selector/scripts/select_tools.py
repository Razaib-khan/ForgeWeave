"""Map a task description to required tools and MCP actions."""
import argparse
import json


TOOL_MAP = {
    "web_search": {"tool": "websearch", "description": "Search the web for information"},
    "fetch_page": {"tool": "webfetch", "description": "Fetch content from a URL"},
    "browse_js": {"tool": "playwright_mcp", "subtools": ["browser_navigate", "browser_snapshot"], "description": "Browse JS-rendered pages"},
    "screenshot": {"tool": "playwright_mcp", "subtools": ["browser_take_screenshot"], "description": "Full-page screenshot"},
}


def main():
    parser = argparse.ArgumentParser(description="Tool selector")
    parser.add_argument("task", choices=list(TOOL_MAP.keys()), help="Type of task")
    parser.add_argument("--detail", action="store_true", help="Show tool details")
    args = parser.parse_args()

    if args.detail:
        print(json.dumps(TOOL_MAP[args.task], indent=2))
    else:
        print(args.task)


if __name__ == "__main__":
    main()
