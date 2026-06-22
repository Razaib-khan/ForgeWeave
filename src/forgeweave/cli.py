"""ForgeWeave CLI — `forge` command entry point.

Usage:
    forge init [--tui <name>] [project_dir]
    forge doctor
    forge --version
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any


def _prompt_mcp_configs(tui: str) -> dict[str, dict[str, Any]]:
    """Interactive prompt for optional MCP servers using InquirerPy."""
    from forgeweave.server import MCP_SERVER_DEFS

    try:
        from InquirerPy import inquirer
    except ImportError:
        return {}

    mcp_configs: dict[str, dict[str, Any]] = {}

    optional_servers = {
        name: defn
        for name, defn in MCP_SERVER_DEFS.items()
        if not defn["mandatory"]
    }

    if not optional_servers:
        return mcp_configs

    print("\nOptional MCP Servers (Playwright MCP is included by default)")
    print("─" * 56)

    for server_name, defn in optional_servers.items():
        enable = inquirer.confirm(
            message=f"Enable {defn['label']}?",
            description=defn.get("description", ""),
            default=False,
        ).execute()

        if not enable:
            continue

        cmd = list(defn["cli_command"])
        env: dict[str, str] = {}

        if defn.get("needs_key"):
            key = inquirer.secret(
                message=defn["key_prompt"],
                long_instruction=f"Will be stored as {defn['key_var']} environment variable in config",
            ).execute()
            if key:
                env[defn["key_var"]] = key

        if defn.get("needs_db_path"):
            db_path = inquirer.text(
                message=defn["db_prompt"],
                default="./dev.db",
            ).execute()
            cmd.append(db_path)

        entry: dict[str, Any] = {"command": cmd}
        if env:
            entry["env"] = env
        mcp_configs[server_name] = entry

    return mcp_configs


def cmd_init(args: argparse.Namespace) -> None:
    """Initialize ForgeWeave in a project directory."""
    from forgeweave.server import forge_init

    tui = args.tui
    if not tui:
        try:
            from InquirerPy import inquirer

            tui = inquirer.select(
                message="Select a TUI:",
                choices=["opencode", "claude", "gemini", "qwen"],
            ).execute()
        except ImportError:
            tui = "opencode"

    project_dir = args.project_dir or os.environ.get("FORGE_PROJECT_DIR") or str(Path.cwd())

    # Prompt for optional MCP servers (skip if non-interactive)
    mcp_configs = _prompt_mcp_configs(tui) if sys.stdin.isatty() else {}

    result = forge_init(
        tui=tui,
        project_dir=project_dir,
        overwrite=args.overwrite,
        mcp_configs=mcp_configs,
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

    py_version = sys.version_info
    print(f"Python: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 14):
        print("  WARNING: ForgeWeave requires Python 3.14+")
        okay = False

    try:
        import forgeweave

        print(f"ForgeWeave: {forgeweave.__version__}")
    except ImportError:
        print("ForgeWeave: NOT INSTALLED")
        okay = False

    templates_dir = Path(__file__).resolve().parent / "templates"
    if templates_dir.exists():
        tuis = [d.name for d in templates_dir.iterdir() if d.is_dir()]
        print(f"Templates: {', '.join(tuis)}")
    else:
        print("Templates: NOT FOUND")
        okay = False

    # Check Playwright is installable
    try:
        import shutil

        npx_path = shutil.which("npx")
        if npx_path:
            print(f"npx: {npx_path}")
        else:
            print("npx: NOT FOUND (needed for Playwright MCP)")
            okay = False
    except Exception:
        print("npx: could not check")

    if okay:
        print("All checks passed.")
    else:
        sys.exit(1)


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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
