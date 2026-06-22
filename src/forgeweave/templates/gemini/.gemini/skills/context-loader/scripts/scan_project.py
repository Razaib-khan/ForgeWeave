"""Scan project structure and identify ForgeWeave components."""

import argparse
from pathlib import Path


def scan_project(root: Path) -> dict:
    result = {
        "root": str(root),
        "has_agents_md": (root / "AGENTS.md").exists(),
        "has_agent_spec": (root / "AGENT_SPEC.md").exists(),
        "has_research_instructions": (root / "RESEARCH_INSTRUCTIONS.md").exists(),
        "tui_dirs": {},
        "skill_count": 0,
    }

    for tui in ["opencode", "claude", "gemini", "qwen"]:
        tui_dir = root / f".{tui}"
        if tui_dir.exists():
            agents = list(tui_dir.glob("agents/*.md")) + list(tui_dir.glob("agents/*.yaml"))
            commands = list(tui_dir.glob("commands/*.md")) + list(tui_dir.glob("commands/*.toml"))
            skills = list(tui_dir.glob("skills/*/SKILL.md"))
            result["tui_dirs"][tui] = {
                "agents": len(agents),
                "commands": len(commands),
                "skills": len(skills),
            }
            result["skill_count"] += len(skills)

    return result


def main():
    parser = argparse.ArgumentParser(description="Scan ForgeWeave project")
    parser.add_argument("--dir", type=Path, default=Path.cwd(), help="Project root")
    args = parser.parse_args()

    info = scan_project(args.dir)
    print(f"Project root: {info['root']}")
    print(f"AGENTS.md: {'✓' if info['has_agents_md'] else '✗'}")
    print(f"AGENT_SPEC.md: {'✓' if info['has_agent_spec'] else '✗'}")

    for tui, data in info["tui_dirs"].items():
        if data:
            print(f"\n.{tui}/")
            print(f"  Agents: {data['agents']}")
            print(f"  Commands: {data['commands']}")
            print(f"  Skills: {data['skills']}")

    print(f"\nTotal skills: {info['skill_count']}")


if __name__ == "__main__":
    main()
