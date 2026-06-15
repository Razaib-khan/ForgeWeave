"""CLI entry point and command definitions for ForgeWeave."""

import argparse
import sys
from pathlib import Path
from shutil import copytree, copy2
from typing import NoReturn

from forgeweave import __version__

forge_root = Path(__file__).resolve().parent.parent
templates_root = forge_root / "forgeweave" / "Templates"

VALID_TUIS = ["opencode", "claude", "gemini", "qwen"]


def resolve_tui(tui_arg: str | None) -> str:
    """Return a validated TUI name from an explicit argument or interactive prompt."""
    if tui_arg:
        if tui_arg not in VALID_TUIS:
            print(
                f"Error: invalid TUI '{tui_arg}'. Choose from: {', '.join(VALID_TUIS)}",
                file=sys.stderr,
            )
            sys.exit(1)
        return tui_arg

    try:
        from InquirerPy import inquirer

        result: str = inquirer.select(  # type: ignore[attr-defined]
            message="Select the TUI you are using:",
            choices=VALID_TUIS,
        ).execute()
        return result
    except Exception:
        print(
            "Error: interactive mode not available. Use: forge init --tui <tui-name>",
            file=sys.stderr,
        )
        print(f"Valid options: {', '.join(VALID_TUIS)}", file=sys.stderr)
        sys.exit(1)


def init_forge(tui: str) -> None:
    """Scaffold a ForgeWeave project for the given TUI in the current directory."""
    template_dir = templates_root / tui
    if not template_dir.is_dir():
        print(f"Error: template directory not found: {template_dir}", file=sys.stderr)
        sys.exit(1)

    target_dir = Path.cwd() / f".{tui}"
    copytree(template_dir, target_dir, dirs_exist_ok=True)

    dest_opencode = target_dir / "opencode.json"
    opencode_json = forge_root / "opencode.json"
    if opencode_json.exists() and opencode_json.resolve() != dest_opencode.resolve():
        copy2(opencode_json, dest_opencode)

    print("Forge project initialized successfully!")


def run_doctor() -> NoReturn:
    """
    Check the local environment and report any issues.

    Each check is printed with a status icon. The function exits with
    code 0 when all checks pass and code 1 otherwise.
    """
    checks: list[tuple[str, bool]] = []

    python_version = sys.version_info
    py_ok = python_version >= (3, 14)
    checks.append(
        (
            f"Python {python_version.major}.{python_version.minor}.{python_version.micro} "
            f"(requires >=3.14)",
            py_ok,
        )
    )

    template_ok = templates_root.is_dir()
    checks.append((f"Template directory exists ({templates_root})", template_ok))

    if template_ok:
        for tui in VALID_TUIS:
            exists = (templates_root / tui).is_dir()
            checks.append((f"  {tui}/ templates present", exists))

    all_pass = True
    for label, ok in checks:
        icon = "PASS" if ok else "FAIL"
        print(f"  [{icon}] {label}")
        if not ok:
            all_pass = False

    print()
    if all_pass:
        print("All checks passed. Your environment is ready.")
        sys.exit(0)
    else:
        print("Some checks failed. Review the details above.")
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser for the forge CLI."""
    parser = argparse.ArgumentParser(
        prog="forge",
        description="ForgeWeave — behavioral execution framework for AI agents",
        epilog="See https://github.com/Razaib-khan/forgeweave for more information.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a ForgeWeave project")
    init_parser.add_argument(
        "--tui",
        "-t",
        choices=VALID_TUIS,
        help=f"Target TUI. Choices: {', '.join(VALID_TUIS)}",
    )

    subparsers.add_parser("doctor", help="Check the local environment for issues")

    return parser


def main() -> None:
    """Parse CLI arguments and dispatch to the appropriate command handler."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        tui = resolve_tui(args.tui)
        init_forge(tui)
    elif args.command == "doctor":
        run_doctor()
    else:
        parser.print_help()
