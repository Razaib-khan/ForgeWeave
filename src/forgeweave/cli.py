"""ForgeWeave CLI — `forge` command entry point.

Usage:
    forge init [--tui <name>] [project_dir]
    forge doctor
    forge mcp [--verbose]
    forge --version
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path


def cmd_init(args: argparse.Namespace) -> None:
    """Initialize ForgeWeave in a project directory."""
    # Import here to avoid slow startup when running other commands
    from forgeweave.server import forge_init

    tui = args.tui
    if not tui:
        print("Select a TUI:")
        choices = ["opencode", "claude", "gemini", "qwen"]
        for i, name in enumerate(choices, 1):
            print(f"  {i}. {name}")
        try:
            sel = input("Enter number (default: 1): ").strip()
            tui = choices[int(sel) - 1] if sel else "opencode"
        except (ValueError, IndexError):
            tui = "opencode"

    project_dir = args.project_dir or os.environ.get("FORGE_PROJECT_DIR") or str(Path.cwd())
    result = forge_init(
        tui=tui,
        project_dir=project_dir,
        overwrite=args.overwrite,
    )
    if result["status"] == "ok":
        print(f"ForgeWeave initialized in {project_dir}")
        print(f"  TUI: {result['tui']}")
        print(f"  Files created: {len(result['files_created'])}")
        for f in result["files_created"][:10]:
            print(f"    {f}")
        if len(result["files_created"]) > 10:
            print(f"    ... and {len(result['files_created']) - 10} more")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


def cmd_doctor(args: argparse.Namespace) -> None:
    """Check the ForgeWeave environment."""
    okay = True

    # Check Python version
    py_version = sys.version_info
    print(f"Python: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 14):
        print("  WARNING: ForgeWeave requires Python 3.14+")
        okay = False

    # Check package installation
    try:
        import forgeweave

        print(f"ForgeWeave: {forgeweave.__version__}")
    except ImportError:
        print("ForgeWeave: NOT INSTALLED")
        okay = False

    # Check templates
    templates_dir = Path(__file__).resolve().parent / "templates"
    if templates_dir.exists():
        tuis = [d.name for d in templates_dir.iterdir() if d.is_dir()]
        print(f"Templates: {', '.join(tuis)}")
    else:
        print("Templates: NOT FOUND")
        okay = False

    # Check optional dependencies
    try:
        import fastmcp

        print(f"FastMCP: {fastmcp.__version__ if hasattr(fastmcp, '__version__') else 'installed'}")
    except ImportError:
        print("FastMCP: NOT INSTALLED (required for MCP server)")

    if importlib.util.find_spec("playwright"):
        print("Playwright: installed")
    else:
        print("Playwright: NOT INSTALLED (optional, needed for JS rendering)")

    if okay:
        print("All checks passed.")
    else:
        sys.exit(1)


def cmd_mcp(args: argparse.Namespace) -> None:
    """Start the ForgeWeave MCP server."""
    from forgeweave.server import main as server_main

    server_main(verbose=args.verbose)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="forge",
        description="ForgeWeave — agent orchestration framework",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"forgeweave {__import__('forgeweave').__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # forge init
    init_p = sub.add_parser("init", help="Initialize ForgeWeave in a project")
    init_p.add_argument(
        "--tui",
        choices=["opencode", "claude", "gemini", "qwen"],
        help="Target TUI adapter (prompts interactively if omitted)",
    )
    init_p.add_argument(
        "project_dir",
        nargs="?",
        default="",
        help="Project directory (default: CWD or FORGE_PROJECT_DIR)",
    )
    init_p.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    init_p.set_defaults(func=cmd_init)

    # forge doctor
    doc_p = sub.add_parser("doctor", help="Check ForgeWeave environment")
    doc_p.set_defaults(func=cmd_doctor)

    # forge mcp
    mcp_p = sub.add_parser("mcp", help="Start ForgeWeave MCP server")
    mcp_p.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    mcp_p.set_defaults(func=cmd_mcp)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
