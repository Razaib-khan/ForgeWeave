"""Generate agent definition files for each TUI from a role description."""
import argparse
from pathlib import Path


TUI_TEMPLATES = {
    "opencode": """---
description: "{description}"
mode: subagent
temperature: 0.2
permissions:
  read: allow
  edit: {edit}
  write: {write}
  glob: allow
  grep: allow
---

# {role_name} Agent

{rules}
""",
    "claude": """---
name: {agent_id}
description: "{description}"
model: us.anthropic.claude-3-5-haiku-20241022-v1:0
permissions:
  read: allow
  edit: {edit}
  write: {write}
---

# {role_name} Agent

{rules}
""",
    "gemini": """---
name: {agent_id}
description: "{description}"
tools:
  read: allow
  edit: {edit}
  write: {write}
memory: false
---

# {role_name} Agent

{rules}
""",
    "qwen": """name: {agent_id}
description: "{description}"
mode: subagent
temperature: 0.2
permissions:
  read: allow
  edit: {edit}
  write: {write}
model: qwen-max

---
{role_name} Agent

{rules}
""",
}


def generate_agent(
    agent_id: str,
    role_name: str,
    description: str,
    rules: str,
    tui: str,
    edit_permission: str = "ask",
    write_permission: str = "ask",
) -> str:
    template = TUI_TEMPLATES.get(tui)
    if not template:
        raise ValueError(f"Unknown TUI: {tui}. Valid: {', '.join(TUI_TEMPLATES.keys())}")
    return template.format(
        agent_id=agent_id,
        role_name=role_name,
        description=description,
        rules=rules.strip(),
        edit=edit_permission,
        write=write_permission,
    )


def main():
    parser = argparse.ArgumentParser(description="Generate agent definition file")
    parser.add_argument("agent_id", help="Agent ID (kebab-case, becomes filename)")
    parser.add_argument("--role", required=True, help="Human-readable role name")
    parser.add_argument("--description", "-d", required=True, help="One-line description")
    parser.add_argument("--rules", required=True, help="Agent instructions/system prompt")
    parser.add_argument("--tui", choices=list(TUI_TEMPLATES.keys()), default="opencode", help="Target TUI")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output directory (agents/)")
    parser.add_argument("--edit", choices=["allow", "deny", "ask"], default="ask")
    parser.add_argument("--write", choices=["allow", "deny", "ask"], default="ask")
    args = parser.parse_args()

    content = generate_agent(
        args.agent_id,
        args.role,
        args.description,
        args.rules,
        args.tui,
        args.edit,
        args.write,
    )

    ext = ".yaml" if args.tui == "qwen" else ".md"
    output_path = args.output / f"{args.agent_id}{ext}"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    print(f"Agent created: {output_path}")


if __name__ == "__main__":
    main()
