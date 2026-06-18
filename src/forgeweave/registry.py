"""Command registry — maps /forge-* commands to handlers.

Handlers can be:
  - "tool": routes to a forge.* tool
  - "skill": routes to forge.execute_skill
  - "bash": runs a shell command
"""
import json
from pathlib import Path

DEFAULT_REGISTRY = {
    "version": "1.0.0",
    "commands": {
        "forge-start": {
            "description": "Load project overview and context",
            "handler": "tool",
            "tool": "forge.load_context",
            "hooks": ["pre_command", "post_command"],
        },
        "forge-research": {
            "description": "Execute deep research pipeline",
            "handler": "tool",
            "tool": "forge.research",
            "hooks": ["pre_command", "research_iteration", "research_complete", "post_command"],
        },
        "forge-review": {
            "description": "Review staged changes",
            "handler": "skill",
            "skill": "validation-engine",
            "hooks": ["pre_command", "post_command"],
        },
        "forge-commit": {
            "description": "Commit with forge context",
            "handler": "bash",
            "script": "git commit",
            "hooks": ["pre_command", "post_command"],
        },
        "forge-test": {
            "description": "Run tests with forge wrappers",
            "handler": "bash",
            "script": "pytest",
            "hooks": ["pre_command", "post_command"],
        },
        "forge-docs": {
            "description": "Generate or update documentation",
            "handler": "skill",
            "skill": "agent-spawner",
            "hooks": ["pre_command", "post_command"],
        },
    },
}


def load_registry(project_dir: Path) -> dict:
    path = project_dir / ".forge" / "command_registry.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return DEFAULT_REGISTRY


def save_registry(project_dir: Path, registry: dict) -> None:
    path = project_dir / ".forge" / "command_registry.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(registry, f, indent=2)
