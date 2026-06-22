"""Detect the test framework used by a project."""

import argparse
from pathlib import Path


CONFIG_INDICATORS = {
    "pytest": [
        "pytest.ini",
        "pyproject.toml",
        "setup.cfg",
        "conftest.py",
    ],
    "vitest": [
        "vitest.config.ts",
        "vitest.config.js",
    ],
    "jest": [
        "jest.config.ts",
        "jest.config.js",
        "jest.config.mjs",
    ],
    "unittest": [],  # Python built-in, no config needed
    "node:test": [],  # Node.js built-in
}


def detect_framework(project_root: Path) -> str | None:
    for framework, indicators in CONFIG_INDICATORS.items():
        for indicator in indicators:
            if (project_root / indicator).exists():
                return framework
    # Check package.json for test scripts
    pkg_json = project_root / "package.json"
    if pkg_json.exists():
        import json

        try:
            pkg = json.loads(pkg_json.read_text())
            dev_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "vitest" in dev_deps:
                return "vitest"
            if "jest" in dev_deps:
                return "jest"
        except json.JSONDecodeError, KeyError:
            pass
    # Check Python
    if (project_root / "pyproject.toml").exists():
        return "pytest"
    return None


def main():
    parser = argparse.ArgumentParser(description="Detect test framework")
    parser.add_argument("--dir", type=Path, default=Path.cwd(), help="Project root")
    args = parser.parse_args()

    framework = detect_framework(args.dir)
    if framework:
        print(framework)
    else:
        print("unknown")
        import sys

        sys.exit(1)


if __name__ == "__main__":
    main()
