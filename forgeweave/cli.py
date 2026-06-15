import argparse
from pathlib import Path
from shutil import copytree, copy2

from InquirerPy import inquirer

from forgeweave import __version__

forge_root = Path(__file__).resolve().parent.parent
templates_root = forge_root / "forgeweave" / "Templates"


def init_forge():
    choice = inquirer.select(
        message="Select the TUI you are using:",
        choices=["opencode", "claude", "gemini", "qwen"],
    ).execute()

    print(f"Initializing Forge for {choice}")

    template_dir = templates_root / choice
    target_dir = Path.cwd() / f".{choice}"
    copytree(template_dir, target_dir, dirs_exist_ok=True)

    opencode_json = forge_root / "opencode.json"
    if opencode_json.exists():
        copy2(opencode_json, Path.cwd() / "opencode.json")

    print("Forge project initialized successfully!")


def build_parser():
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
    subparsers.add_parser("init", help="Initialize a ForgeWeave project")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        init_forge()
    else:
        parser.print_help()
