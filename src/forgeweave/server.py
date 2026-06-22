"""ForgeWeave — Project scaffolding utilities.

The forge MCP server has been deprecated. ForgeWeave now provides only
project scaffolding (forge init) and template distribution. All agent
orchestration, research, and web interaction rely on TUI-native features
(plugins, hooks, subagents) and the Playwright MCP server.
"""

import json
import logging
import os
import re
import shutil
import sys
from pathlib import Path

# ── Logging ────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(name)s %(message)s",
    datefmt="%m/%d/%y %H:%M:%S",
    stream=sys.stderr,
)
log = logging.getLogger("forge")

# ── Meta ───────────────────────────────────────────────────────

FORGE_VERSION = "2.0.0"
SUPPORTED_TUIS = ["opencode", "claude", "gemini", "qwen"]

# ── Helpers ────────────────────────────────────────────────────


def _get_project_dir() -> Path:
    env_dir = os.environ.get("FORGE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir).resolve()
    return Path.cwd()


def _get_templates_dir() -> Path:
    """Find the templates directory within the installed package."""
    here = Path(__file__).resolve().parent
    candidate = here / "templates"
    if candidate.exists():
        return candidate
    # Fallback for development: check repo root
    for parent in here.parents:
        if (parent / "forgeweave" / "Templates").exists():
            return parent / "forgeweave" / "Templates"
    return candidate


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _get_tui() -> str:
    return os.environ.get("FORGE_TUI", "opencode")


# ── MCP Server Registry ────────────────────────────────────────

MCP_SERVER_DEFS: dict[str, dict] = {
    "playwright": {
        "label": "Playwright MCP",
        "package": "@playwright/mcp@latest",
        "mandatory": True,
        "needs_key": False,
        "cli_command": ["npx", "@playwright/mcp@latest"],
    },
    "firecrawl": {
        "label": "Firecrawl MCP",
        "package": "firecrawl-mcp",
        "description": "Web scraping and crawling",
        "mandatory": False,
        "needs_key": True,
        "key_var": "FIRECRAWL_API_KEY",
        "key_prompt": "Enter your Firecrawl API key (starts with fc-):",
        "cli_command": ["npx", "-y", "firecrawl-mcp"],
    },
    "github": {
        "label": "GitHub MCP",
        "package": "@modelcontextprotocol/server-github",
        "description": "GitHub repository and issue management",
        "mandatory": False,
        "needs_key": True,
        "key_var": "GITHUB_PERSONAL_ACCESS_TOKEN",
        "key_prompt": "Enter your GitHub Personal Access Token:",
        "cli_command": ["npx", "-y", "@modelcontextprotocol/server-github"],
    },
    "sqlite": {
        "label": "SQLite MCP",
        "package": "@modelcontextprotocol/server-sqlite",
        "description": "SQLite database management",
        "mandatory": False,
        "needs_key": False,
        "needs_db_path": True,
        "db_prompt": "Path to SQLite database file (default: ./dev.db):",
        "cli_command": ["npx", "-y", "@modelcontextprotocol/server-sqlite"],
    },
    "context7": {
        "label": "Context7 MCP",
        "package": "@upstash/context7-mcp",
        "description": "Library/framework documentation lookup",
        "mandatory": False,
        "needs_key": True,
        "key_var": "CONTEXT7_API_KEY",
        "key_prompt": "Enter your Context7 API key (optional, press Enter to skip):",
        "key_optional": True,
        "cli_command": ["npx", "-y", "@upstash/context7-mcp"],
    },
    "headroom": {
        "label": "Headroom MCP",
        "package": "headroom-ai",
        "description": "Context compression — 60-95% fewer tokens",
        "mandatory": True,
        "needs_key": False,
        "cli_command": ["npx", "-y", "headroom", "mcp", "serve"],
    },
}


def _opencode_mcp_block(name: str, command: list[str], env: dict | None = None) -> dict:
    block: dict = {
        "type": "local",
        "command": command,
        "enabled": True,
    }
    if env:
        block["env"] = env
    return block


def _claude_mcp_block(name: str, command: list[str], env: dict | None = None) -> dict:
    block: dict = {
        "command": command[0],
        "args": command[1:],
    }
    if env:
        block["env"] = env
    return block


def _gemini_mcp_block(name: str, command: list[str], env: dict | None = None) -> dict:
    # Gemini uses the same format as opencode
    return _opencode_mcp_block(name, command, env)


def _qwen_mcp_block(name: str, command: list[str], env: dict | None = None) -> dict:
    # Qwen uses the same format as Claude/VSCode
    return _claude_mcp_block(name, command, env)


_MCP_BLOCK_BUILDERS: dict[str, callable] = {
    "opencode": _opencode_mcp_block,
    "claude": _claude_mcp_block,
    "gemini": _gemini_mcp_block,
    "qwen": _qwen_mcp_block,
}

_MCP_CONFIG_FILES: dict[str, str] = {
    "opencode": "opencode.json",
    "claude": ".claude/settings.json",
    "gemini": ".gemini/settings.json",
    "qwen": "qwen-extension.json",
}

_MCP_CONFIG_KEYS: dict[str, str] = {
    "opencode": "mcp",
    "claude": "mcpServers",
    "gemini": "mcp",
    "qwen": "mcpServers",
}


def _get_mcp_server_config(tui: str, server_name: str, command: list[str], env: dict | None = None) -> dict:
    builder = _MCP_BLOCK_BUILDERS.get(tui, _opencode_mcp_block)
    return builder(server_name, command, env)


def _apply_mcp_configs(project_dir: Path, tui: str, mcp_configs: dict[str, dict]) -> list[str]:
    """Write selected MCP server configs into the project's TUI config file.

    Args:
        project_dir: Project root directory.
        tui: Target TUI name.
        mcp_configs: Dict of server_name -> {"command": [...], "env": {...} | None}

    Returns:
        List of config file paths that were modified (relative to project root).
    """
    config_rel = _MCP_CONFIG_FILES.get(tui, "opencode.json")
    config_key = _MCP_CONFIG_KEYS.get(tui, "mcp")
    config_path = project_dir / config_rel

    if not config_path.exists():
        log.warning("Config file not found: %s (MCP servers not written)", config_path)
        return []

    try:
        raw = config_path.read_text(encoding="utf-8")
        config = json.loads(raw)
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Failed to read config %s: %s", config_path, exc)
        return []

    if config_key not in config:
        config[config_key] = {}

    for server_name, cfg in mcp_configs.items():
        block = _get_mcp_server_config(
            tui=tui,
            server_name=server_name,
            command=cfg["command"],
            env=cfg.get("env"),
        )
        config[config_key][server_name] = block

    try:
        config_path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        log.info("MCP configs written to %s", config_path)
        return [str(config_path.relative_to(project_dir))]
    except OSError as exc:
        log.warning("Failed to write config %s: %s", config_path, exc)
        return []


# ── Dynamic AGENTS.md processing ──────────────────────────────

_SELECTED_MARKER = "✓"
_UNSELECTED_MARKER = "—"


def _process_agents_md(project_dir: Path, selected_servers: set[str]) -> list[str]:
    """Update AGENTS.md tables to reflect which MCP servers were actually selected.

    - Selected servers get a ✓ checkmark in the name column.
    - Unselected optional servers get a — dash (not configured).
    - The 'When to Use Each Server' table also reflects only available tools.

    Returns:
        List of relative paths changed (empty if AGENTS.md not found).
    """
    agents_path = project_dir / "AGENTS.md"
    if not agents_path.exists():
        return []

    try:
        raw = agents_path.read_text(encoding="utf-8")
    except OSError:
        return []

    lines = raw.splitlines(keepends=True)
    modified = False

    # ── Phase 1: Process "Available MCP Servers" table ──────────
    # Lines look like:
    # | `firecrawl` (Firecrawl MCP) | ... | ... |
    # We add ✓ or — after the server name in the first column.

    for i, line in enumerate(lines):
        # Match table rows: | `name` (Label MCP) ...
        stripped = line.strip()
        if not stripped.startswith("| `"):
            continue
        # Extract the server name from `backtick` in first cell
        if "`" not in stripped:
            continue
        first_backtick = stripped.index("`")
        second_backtick = stripped.index("`", first_backtick + 1)
        server_name = stripped[first_backtick + 1 : second_backtick]

        if server_name not in MCP_SERVER_DEFS:
            continue

        defn = MCP_SERVER_DEFS[server_name]

        # Only process optional servers (Playwright is always there)
        if defn["mandatory"]:
            continue

        if server_name in selected_servers:
            # Add ✓ if not already there
            marker = f" *{_SELECTED_MARKER}*"
            if marker not in line:
                # Insert after the closing `) or after the name
                old = f"` ({defn['label']})"
                new = f"` ({defn['label']}) {marker}"
                if old in line:
                    lines[i] = line.replace(old, new)
                    modified = True
        else:
            # Mark as not configured
            marker = f" *{_UNSELECTED_MARKER}*"
            if marker not in line:
                old = f"` ({defn['label']})"
                new = f"` ({defn['label']}) {marker}"
                if old in line:
                    lines[i] = line.replace(old, new)
                    modified = True

    # ── Phase 2: Process "When to Use Each Server" table ────────
    # Remove or mark rows for unselected research tools.
    # Key: server name → tool name prefix in the "Tool" column
    server_tool_prefixes = {
        "firecrawl": "Firecrawl MCP:",
        "github": "GitHub MCP:",
        "sqlite": "SQLite MCP:",
        "context7": "Context7 MCP:",
    }

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("| "):
            continue
        # Check if this row references a specific MCP server's tool
        for srv_name, prefix in server_tool_prefixes.items():
            if prefix in stripped:
                if srv_name in selected_servers:
                    # Ensure it doesn't have a strikethrough or disable marker
                    pass  # leave as-is
                else:
                    # Add "(not configured)" note
                    if "(not configured)" not in stripped:
                        lines[i] = line.rstrip("\n") + " *(not configured)*\n"
                        modified = True
                break

    if not modified:
        return []

    try:
        agents_path.write_text("".join(lines), encoding="utf-8")
        log.info("AGENTS.md updated for selected MCP servers: %s", selected_servers)
        return ["AGENTS.md"]
    except OSError:
        return []


# ── forge init (project scaffolding) ───────────────────────────


def forge_init(
    tui: str = "opencode",
    project_dir: str = "",
    overwrite: bool = False,
    mcp_configs: dict[str, dict] | None = None,
) -> dict:
    """Initialize ForgeWeave in a TUI project.

    Copies template files (agents, commands, hooks, skills, config)
    from the forgeweave Templates directory into the project.

    Args:
        tui: Target TUI — 'opencode', 'claude', 'gemini', or 'qwen'.
        project_dir: Project directory path. Defaults to FORGE_PROJECT_DIR env or CWD.
        overwrite: Overwrite existing files if True.
        mcp_configs: Optional MCP server configs to write (server_name -> {"command": [...], "env": ...}).
                      Defaults to just Playwright MCP.
    """
    proj = Path(project_dir).resolve() if project_dir else _get_project_dir()

    if tui not in SUPPORTED_TUIS:
        return {
            "status": "error",
            "error": f"Unsupported TUI: {tui}. Must be one of {SUPPORTED_TUIS}",
        }

    if not proj.exists():
        return {"status": "error", "error": f"Project directory not found: {proj}"}

    templates_dir = _get_templates_dir()
    src = templates_dir / tui
    if not src.exists():
        return {"status": "error", "error": f"Template not found for TUI '{tui}' at {src}"}

    # Check for existing forgeweave init
    forge_flag = proj / ".forge" / ".forgeweave"
    if forge_flag.exists() and not overwrite:
        return {
            "status": "error",
            "error": "ForgeWeave already initialized. Set overwrite=true to reinitialize.",
        }

    files_created = []

    # Copy template folder contents into project
    for item in src.iterdir():
        dst = proj / item.name
        if dst.exists() and not overwrite:
            continue
        if item.is_dir():
            shutil.copytree(item, dst, dirs_exist_ok=overwrite)
        else:
            shutil.copy2(item, dst)
        files_created.append(str(dst.relative_to(proj)))

    # Write forge marker
    forge_dir = proj / ".forge"
    forge_dir.mkdir(exist_ok=True)
    forge_flag.write_text(f"forgeweave-{FORGE_VERSION}")
    files_created.append(".forge/.forgeweave")

    # Apply MCP server configs (include mandatory Playwright + Headroom + user-selected optional ones)
    default_mcp = {
        "playwright": {
            "command": MCP_SERVER_DEFS["playwright"]["cli_command"],
        },
        "headroom": {
            "command": MCP_SERVER_DEFS["headroom"]["cli_command"],
        },
    }
    merged = {**default_mcp, **(mcp_configs or {})}
    mcp_files = _apply_mcp_configs(proj, tui, merged)
    files_created.extend(mcp_files)

    # Update AGENTS.md to reflect actually selected MCP servers
    selected_servers = set(merged.keys())
    agents_updated = _process_agents_md(proj, selected_servers)
    files_created.extend(agents_updated)

    log.info(f"ForgeWeave initialized in {proj} (TUI: {tui}, {len(files_created)} files)")
    return {
        "status": "ok",
        "project_dir": str(proj),
        "tui": tui,
        "files_created": sorted(files_created),
        "error": None,
    }
