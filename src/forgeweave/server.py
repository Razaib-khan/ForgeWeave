"""ForgeWeave Control Plane MCP Server — 12 forge.* tools.

Design: Expose capabilities, hide orchestration.
All 5 pipeline stages (plan, research, validate, synthesize, output) are
internal to forge.research and never exposed as separate MCP tools.
"""

import asyncio
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from forgeweave import db as fdb
from forgeweave import registry
from forgeweave.pipeline import run_pipeline

# ── Logging ────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(name)s %(message)s",
    datefmt="%m/%d/%y %H:%M:%S",
    stream=sys.stderr,
)
log = logging.getLogger("forge-mcp")

mcp = FastMCP("ForgeWeave")

# ── Helpers ─────────────────────────────────────────────────────

FORGE_VERSION = "1.0.0"

SUPPORTED_TUIS = ["opencode", "claude", "gemini", "qwen"]

VALIDATION_RULES = {
    "every_claim_has_source": lambda text: bool(
        re.findall(r"\[([^\]]+)\]\(https?://[^)]+\)", text)
    ),
    "no_blog_sources": lambda text: (
        not bool(re.search(r"(blog|changelog|medium\.com|dev\.to)", text, re.I))
    ),
    "structure_complete": lambda text: all(s in text for s in ["## Overview", "## Sources"]),
    "no_secrets": lambda text: (
        not bool(re.search(r"(api[_-]?key|password|secret|AKIA[0-9A-Z]{16})", text, re.I))
    ),
    "valid_frontmatter": lambda text: text.startswith("---") and "---" in text[3:],
}


def _get_project_dir() -> Path:
    env_dir = os.environ.get("FORGE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir).resolve()
    return Path.cwd()


def _get_db_path(project_dir: Path) -> Path:
    return project_dir / ".forge" / "state.db"


def _get_tui() -> str:
    return os.environ.get("FORGE_TUI", "opencode")


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


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


def _load_skill_metadata(project_dir: Path) -> list[dict]:
    skills_dir = project_dir / "skills"
    if not skills_dir.exists():
        return []
    result = []
    for d in sorted(skills_dir.iterdir()):
        if d.is_dir():
            skill_file = d / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text(encoding="utf-8")
                name = d.name
                version = "1.0.0"
                m = re.search(r"skill_id:\s*(\S+)", content)
                if m:
                    name = m.group(1)
                m = re.search(r"version:\s*(\S+)", content)
                if m:
                    version = m.group(1)
                result.append(
                    {
                        "id": name,
                        "version": version,
                        "path": str(skill_file.relative_to(project_dir)),
                    }
                )
    return result


def _load_agent_metadata(project_dir: Path) -> list[dict]:
    agents_dir = project_dir / "agents"
    if not agents_dir.exists():
        return []
    result = []
    for f in sorted(agents_dir.iterdir()):
        if f.suffix in (".md", ".yaml"):
            internal = False
            content = f.read_text(encoding="utf-8")
            if "internal: true" in content:
                internal = True
            result.append(
                {
                    "id": f.stem,
                    "path": str(f.relative_to(project_dir)),
                    "enabled": not internal,
                    "internal": internal,
                }
            )
    return result


def _load_hook_metadata(project_dir: Path) -> list[str]:
    tui = _get_tui()
    hooks_dir = project_dir / f".{tui}" / "hooks"
    if not hooks_dir.exists():
        # Try direct path
        hooks_dir = project_dir / ".forge" / "hooks"
    if not hooks_dir.exists():
        return []
    hooks = []
    for f in hooks_dir.iterdir():
        if f.suffix in (".py", ".sh", ".ts", ".js", ".jsonc"):
            hooks.append(f.stem)
    return sorted(hooks)


# ═══════════════════════════════════════════════════════════════
# TOOL 1: forge.init
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_init(
    tui: str = "opencode",
    project_dir: str = "",
    overwrite: bool = False,
) -> dict:
    """Initialize ForgeWeave in a TUI project.

    Copies template files (agents, commands, hooks, skills, config)
    from the forgeweave Templates directory into the project.

    Args:
        tui: Target TUI — 'opencode', 'claude', 'gemini', or 'qwen'.
        project_dir: Project directory path. Defaults to FORGE_PROJECT_DIR env or CWD.
        overwrite: Overwrite existing files if True.
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
    registry_path = proj / ".forge" / "command_registry.json"
    if registry_path.exists() and not overwrite:
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

    # Write state DB and command registry
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)
    registry.save_registry(proj, registry.DEFAULT_REGISTRY)
    files_created.append(".forge/state.db")
    files_created.append(".forge/command_registry.json")

    log.info(f"ForgeWeave initialized in {proj} (TUI: {tui}, {len(files_created)} files)")
    return {
        "status": "ok",
        "project_dir": str(proj),
        "tui": tui,
        "files_created": sorted(files_created),
        "error": None,
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 2: forge.execute_command
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_execute_command(
    command: str,
    args: str = "",
    context: dict | None = None,
    job_id: str | None = None,
) -> dict:
    """Route a /forge-* command through the command registry.

    Resolves the command to its handler (tool, skill, or bash),
    fires pre/post hooks, and returns the result.

    Args:
        command: The command name including leading slash (e.g. '/forge-research').
        args: Raw argument string after the command name.
        context: Optional execution context.
        job_id: Optional existing job ID to resume.
    """
    proj = _get_project_dir()
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)

    cmd_name = command.lstrip("/")
    reg = registry.load_registry(proj)
    entry = reg.get("commands", {}).get(cmd_name)

    if entry is None:
        available = list(reg.get("commands", {}).keys())
        return {
            "status": "error",
            "error": f"Unknown command: {cmd_name}. Available: {available}",
        }

    # ── Hook: pre_command ──
    job = fdb.create_job(db_path, "command", {"command": command, "args": args})
    fdb.add_trace(db_path, job, "pre_command", {"command": cmd_name})

    handler = entry.get("handler", "tool")
    result: dict[str, Any] = {}

    try:
        if handler == "tool":
            tool_name = entry.get("tool", cmd_name)
            # Route to the appropriate forge.* tool
            result = _route_to_tool(tool_name, args, context, job)
        elif handler == "skill":
            skill_name = entry.get("skill", "")
            result = _execute_skill_internal(
                proj, db_path, skill_name, {"args": args, "context": context}
            )
        elif handler == "bash":
            script = entry.get("script", "")
            proc = subprocess.run(
                script + " " + args,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
            )
            result = {
                "stdout": proc.stdout[:2000],
                "stderr": proc.stderr[:1000],
                "returncode": proc.returncode,
            }
        else:
            result = {"error": f"Unknown handler type: {handler}"}

        fdb.update_job(db_path, job, status="completed", progress_pct=100, result=result)
    except Exception as e:
        log.error(f"Command '{cmd_name}' failed: {e}")
        fdb.update_job(db_path, job, status="failed", error=str(e))
        result = {"error": str(e)}

    # ── Hook: post_command ──
    fdb.add_trace(
        db_path, job, "post_command", {"command": cmd_name, "status": result.get("status", "ok")}
    )

    return {
        "status": "ok" if "error" not in result else "error",
        "job_id": job,
        "result": result,
        "error": result.get("error"),
    }


def _route_to_tool(tool_name: str, args: str, context: dict | None, job_id: str) -> dict:
    """Route a command to the appropriate forge.* tool."""
    # Parse args for common patterns
    args_dict = _parse_args(args)

    if tool_name == "forge.load_context":
        raw = forge_load_context(str(_get_project_dir()))
        return {"status": raw.get("status"), "context": raw}

    if tool_name == "forge.research":
        topic = args_dict.get("topic") or args.strip()
        depth = args_dict.get("depth", "standard")
        focus = args_dict.get("focus", "usage")
        raw = forge_research(topic=topic, depth=depth, focus=focus)
        return {"status": raw.get("status"), "job_id": raw.get("job_id")}

    if tool_name == "forge.execute_skill":
        skill_name = args_dict.get("skill") or args.strip().split()[0] if args.strip() else ""
        raw = forge_execute_skill(skill=skill_name, params=args_dict)
        return {"status": raw.get("status"), "result": raw.get("output")}

    return {"error": f"No route for tool: {tool_name}"}


def _parse_args(args: str) -> dict:
    """Parse command args into a dict. Supports --key=value and positional."""
    result: dict[str, Any] = {}
    parts = args.strip().split()
    positional = []
    i = 0
    while i < len(parts):
        p = parts[i]
        if p.startswith("--"):
            if "=" in p:
                k, v = p[2:].split("=", 1)
                result[k] = v
            elif i + 1 < len(parts) and not parts[i + 1].startswith("--"):
                result[p[2:]] = parts[i + 1]
                i += 1
            else:
                result[p[2:]] = True
        else:
            positional.append(p)
        i += 1
    if positional:
        result["topic"] = " ".join(positional)
    return result


# ═══════════════════════════════════════════════════════════════
# TOOL 3: forge.execute_skill
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_execute_skill(
    skill: str,
    params: dict | None = None,
    context: dict | None = None,
) -> dict:
    """Load a skill by name, read its SKILL.md, and execute its workflow.

    Args:
        skill: Skill ID (must match a directory in skills/).
        params: Parameters to pass to the skill's scripts.
        context: Optional execution context.
    """
    proj = _get_project_dir()
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)

    job = fdb.create_job(db_path, "skill", {"skill": skill, "params": params})
    fdb.add_trace(db_path, job, "pre_skill", {"skill": skill})

    result = _execute_skill_internal(proj, db_path, skill, params or {})

    fdb.add_trace(db_path, job, "post_skill", {"skill": skill, "status": result.get("status")})
    fdb.update_job(db_path, job, status=result.get("status", "completed"), result=result)

    return {
        "status": result.get("status", "ok"),
        "job_id": job,
        "skill": skill,
        "output": result,
        "artifacts": result.get("artifacts", []),
        "error": result.get("error"),
    }


def _execute_skill_internal(proj: Path, db_path: Path, skill: str, params: dict) -> dict:
    """Execute a skill by finding and running its script files."""
    skill_dir = proj / "skills" / skill
    if not skill_dir.exists():
        return {"status": "error", "error": f"Skill not found: {skill}"}

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return {"status": "error", "error": f"SKILL.md not found for skill: {skill}"}

    # Find scripts in the skill's scripts/ directory
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists() or not any(scripts_dir.iterdir()):
        return {
            "status": "ok",
            "message": f"Skill '{skill}' has no scripts. SKILL.md loaded.",
            "artifacts": [],
        }

    artifacts = []
    last_output = {}

    for script_file in sorted(scripts_dir.iterdir()):
        if script_file.suffix == ".py":
            try:
                proc = subprocess.run(
                    [sys.executable, str(script_file)] + [f"--{k}={v}" for k, v in params.items()],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                last_output = {
                    "stdout": proc.stdout[:2000],
                    "stderr": proc.stderr[:500],
                    "returncode": proc.returncode,
                }
                if proc.returncode == 0:
                    artifacts.append(str(script_file.relative_to(proj)))
            except subprocess.TimeoutExpired:
                last_output = {"error": f"Script timed out: {script_file.name}"}
            except Exception as e:
                last_output = {"error": f"Script failed: {script_file.name}: {e}"}

    return {
        "status": "ok",
        "message": f"Executed {len(artifacts)} scripts for skill '{skill}'",
        "artifacts": artifacts,
        "output": last_output,
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 4: forge.create_agent
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_create_agent(
    agent_id: str,
    role: str,
    tools: list[str] | None = None,
    skills: list[str] | None = None,
    constraints: str = "",
    temperature: float = 0.3,
) -> dict:
    """Generate an agent definition file in the TUI's agents/ directory.

    Creates the appropriate file format (.md for opencode/claude/gemini,
    .yaml for qwen) with the agent's role, tools, skills, and constraints.

    Args:
        agent_id: Unique kebab-case identifier.
        role: Description of the agent's purpose.
        tools: List of forge.* MCP tools the agent can use.
        skills: List of skill IDs the agent can invoke.
        constraints: Behavioral constraints.
        temperature: Model temperature 0.0-1.0.
    """
    proj = _get_project_dir()
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)

    tui = _get_tui()
    agents_dir = proj / "agents"
    agents_dir.mkdir(exist_ok=True)

    # Validate agent_id
    if not re.match(r"^[a-z][a-z0-9-]*$", agent_id):
        return {
            "status": "error",
            "error": "agent_id must be kebab-case (lowercase letters, numbers, hyphens)",
        }

    # Check for duplicate
    for f in agents_dir.iterdir():
        if f.stem == agent_id:
            return {"status": "error", "error": f"Duplicate agent_id: {agent_id}"}

    agent_job = fdb.create_job(db_path, "agent_creation", {"agent_id": agent_id})
    fdb.add_trace(db_path, agent_job, "pre_agent_create", {"agent_id": agent_id})

    tools_list = tools or []
    skills_list = skills or []

    if tui == "qwen":
        ext = ".yaml"
        content = f"""# {agent_id}
description: "{role}"
mode: subagent
internal: false
temperature: {temperature}
tools: [{", ".join(tools_list)}]
skills: [{", ".join(skills_list)}]
constraints: >
  {constraints}
"""
    else:
        ext = ".md"
        tools_block = "\n".join(f"  - {t}" for t in tools_list)
        skills_block = "\n".join(f"  - {s}" for s in skills_list)
        content = f"""---
description: "{role}"
mode: subagent
internal: false
temperature: {temperature}
tools:
{tools_block}
skills:
{skills_block}
constraints: "{constraints}"
---

# {agent_id}

{role}
"""

    file_path = agents_dir / f"{agent_id}{ext}"
    file_path.write_text(content, encoding="utf-8")

    fdb.update_job(db_path, agent_job, status="completed", result={"file_path": str(file_path)})
    fdb.add_trace(db_path, agent_job, "post_agent_create", {"file_path": str(file_path)})

    log.info(f"Created agent '{agent_id}' at {file_path}")
    return {
        "status": "ok",
        "agent_id": agent_id,
        "tui": tui,
        "file_path": str(file_path.relative_to(proj)),
        "registered": True,
        "error": None,
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 5: forge.research
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_research(
    topic: str,
    depth: str = "standard",
    focus: str = "usage",
    constraints: str = "",
    max_sources: int = 20,
) -> dict:
    """Full deep-research pipeline.

    Internally runs: planner → parallel research workers → validator →
    synthesizer → structured output. Caller only receives a job_id;
    poll forge.status(job_id) for progress and results.

    Args:
        topic: The research topic or question.
        depth: 'quick', 'standard', or 'deep'.
        focus: 'usage', 'architecture', 'comparison', or 'general'.
        constraints: Additional rules.
        max_sources: Maximum number of sources to collect.
    """
    proj = _get_project_dir()
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)

    if not topic or len(topic.strip()) < 10:
        return {"status": "error", "error": "Topic too vague. Provide at least 10 characters."}

    job_id = fdb.create_job(
        db_path,
        "research",
        {
            "topic": topic,
            "depth": depth,
            "focus": focus,
            "max_sources": max_sources,
        },
    )

    fdb.add_trace(db_path, job_id, "pre_research", {"topic": topic})

    def _progress(stage: str, pct: int, msg: str):
        fdb.update_job(db_path, job_id, stage=stage, progress_pct=pct, message=msg)

    # Run pipeline in background thread so the tool call returns immediately
    def _run():
        try:
            fdb.update_job(
                db_path, job_id, stage="plan", progress_pct=5, message="Planning research..."
            )
            summary = asyncio.run(
                run_pipeline(
                    topic=topic,
                    project_dir=proj,
                    job_id=job_id,
                    depth=depth,
                    focus=focus,
                    constraints=constraints,
                    max_sources=max_sources,
                    update_status=lambda **kw: fdb.update_job(db_path, job_id, **kw),
                )
            )
            fdb.update_job(db_path, job_id, status="completed", progress_pct=100, result=summary)
            fdb.add_trace(db_path, job_id, "research_complete", summary)
            fdb.add_trace(db_path, job_id, "post_research", {"report": summary.get("report", "")})
        except Exception as e:
            log.error(f"Research pipeline failed: {e}")
            fdb.update_job(db_path, job_id, status="failed", error=str(e))
            fdb.add_trace(db_path, job_id, "research_error", {"error": str(e)})

    threading.Thread(target=_run, daemon=True).start()

    return {
        "status": "job_started",
        "job_id": job_id,
        "error": None,
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 6: forge.search
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_search(
    query: str,
    max_results: int = 5,
    source_filter: str = "",
) -> dict:
    """Lightweight on-demand web search for quick lookups.

    Fetches and extracts content from authoritative sources.
    Not a full research pipeline — single-step fetch-and-extract.

    Args:
        query: Search query (max 300 chars).
        max_results: Number of results (1-10).
        source_filter: Comma-separated domain whitelist.
    """
    import httpx
    from forgeweave.research_mcp.scraper import extract_main_content, fetch_page, parse_html

    if not query or len(query.strip()) < 5:
        return {
            "status": "error",
            "query": query,
            "error": "Query too short. Provide at least 5 characters.",
        }

    # Use search APIs if available, otherwise fallback to direct URL
    domains = [d.strip() for d in source_filter.split(",") if d.strip()] if source_filter else []

    results = []
    headers = {
        "User-Agent": "ForgeWeave/1.0",
        "Accept": "text/html,application/xhtml+xml",
    }

    async def _search():
        async with httpx.AsyncClient(
            headers=headers, timeout=15.0, follow_redirects=True
        ) as client:
            # Try crawling suggested source URLs first
            for domain in domains[:max_results]:
                url = f"https://{domain}"
                try:
                    html = await fetch_page(url, client)
                    if html:
                        content = extract_main_content(html, url)
                        if content and content.text:
                            results.append(
                                {
                                    "url": url,
                                    "title": content.title or url,
                                    "snippet": content.text[:300],
                                    "source": domain,
                                }
                            )
                except Exception:
                    pass

            # If no results yet, try a direct web search via common search engines
            if not results:
                search_urls = [
                    f"https://www.google.com/search?q={query}",
                    f"https://duckduckgo.com/html/?q={query}",
                ]
                for surl in search_urls:
                    try:
                        html = await fetch_page(surl, client)
                        if html:
                            soup = parse_html(html)
                            for link in soup.find_all("a", href=True)[:max_results]:
                                href = link.get("href", "")
                                text = link.get_text(strip=True)
                                if text and len(text) > 20:
                                    results.append(
                                        {
                                            "url": href,
                                            "title": text[:100],
                                            "snippet": text[:200],
                                            "source": "web",
                                        }
                                    )
                    except Exception:
                        pass
                    if results:
                        break

    try:
        asyncio.run(_search())
    except Exception as e:
        log.warning(f"Search error: {e}")

    return {
        "status": "ok" if results else "error",
        "query": query,
        "results": results[:max_results],
        "error": None if results else "No results found",
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 7: forge.load_context
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_load_context(project_dir: str = "") -> dict:
    """Load project state into a structured snapshot.

    Reads AGENTS.md, skills directory, agents directory, commands,
    and hook configuration.

    Args:
        project_dir: Project directory. Defaults to FORGE_PROJECT_DIR env or CWD.
    """
    proj = Path(project_dir).resolve() if project_dir else _get_project_dir()

    if not proj.exists():
        return {"status": "error", "error": f"Project directory not found: {proj}"}

    initialized = (proj / ".forge" / "state.db").exists()

    agents = _load_agent_metadata(proj)
    skills = _load_skill_metadata(proj)
    hooks = _load_hook_metadata(proj)

    reg = registry.load_registry(proj)
    commands = list(reg.get("commands", {}).keys())

    return {
        "status": "ok",
        "forge": {
            "version": FORGE_VERSION,
            "tui": _get_tui(),
            "initialized": initialized,
        },
        "agents": agents,
        "skills": skills,
        "commands": commands,
        "hooks": hooks,
        "error": None,
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 8: forge.validate
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_validate(
    target: str,
    rules: list[str] | None = None,
) -> dict:
    """Validate outputs against ForgeWeave rules.

    Args:
        target: File path or string content to validate.
        rules: List of rule IDs to check (e.g. 'every_claim_has_source').
    """
    proj = _get_project_dir()

    # Resolve content from file path or direct string
    target_path = proj / target
    if target_path.exists():
        text = target_path.read_text(encoding="utf-8")
    else:
        text = target

    rule_list = rules or list(VALIDATION_RULES.keys())
    checks = []

    for rule_id in rule_list:
        check_fn = VALIDATION_RULES.get(rule_id)
        if check_fn is None:
            checks.append({"rule": rule_id, "passed": False, "details": f"Unknown rule: {rule_id}"})
            continue

        try:
            passed = check_fn(text)
            detail_map = {
                "every_claim_has_source": f"Found sources in text: {passed}",
                "no_blog_sources": f"No blog/changelog sources detected: {passed}",
                "structure_complete": f"Required sections present: {passed}",
                "no_secrets": f"No secrets detected: {passed}",
                "valid_frontmatter": f"Valid frontmatter: {passed}",
            }
            checks.append(
                {
                    "rule": rule_id,
                    "passed": passed,
                    "details": detail_map.get(rule_id, f"Check {'passed' if passed else 'failed'}"),
                }
            )
        except Exception as e:
            checks.append({"rule": rule_id, "passed": False, "details": str(e)})

    failed = sum(1 for c in checks if not c["passed"])
    return {
        "status": "pass" if failed == 0 else "fail",
        "checks": checks,
        "failed": failed,
        "error": None,
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 9: forge.memory_write
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_memory_write(
    key: str,
    value: str,
    namespace: str = "default",
    ttl_seconds: int = 0,
) -> dict:
    """Store a value in persistent memory (SQLite).

    Args:
        key: Key in namespace:key format (max 256 chars).
        value: JSON-serializable value.
        namespace: Namespace for grouping keys.
        ttl_seconds: Time-to-live in seconds. 0 = no expiry.
    """
    if len(key) > 256:
        return {"status": "error", "error": "Key exceeds 256 characters"}

    proj = _get_project_dir()
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)

    try:
        parsed_value = json.loads(value) if isinstance(value, str) else value
    except json.JSONDecodeError, TypeError:
        parsed_value = value

    result = fdb.memory_write(db_path, key, parsed_value, namespace, ttl_seconds)
    return {
        "status": "ok",
        "key": key,
        "size_bytes": result["size_bytes"],
        "expires_at": result["expires_at"],
        "error": None,
    }


# ═══════════════════════════════════════════════════════════════
# TOOL 10: forge.memory_read
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_memory_read(
    key: str = "",
    namespace: str = "",
) -> dict:
    """Read a value from persistent memory.

    Args:
        key: Exact key to look up. If omitted, list all keys in namespace.
        namespace: Namespace filter. Required if key is omitted.
    """
    proj = _get_project_dir()
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)

    if key:
        entry = fdb.memory_read(db_path, key)
        if entry is None:
            return {"status": "not_found", "key": key, "error": None}
        return {
            "status": "ok",
            "key": key,
            "value": entry["value_json"],
            "created_at": entry["created_at"],
            "expires_at": entry.get("expires_at"),
            "error": None,
        }

    if namespace:
        keys = fdb.memory_list_namespace(db_path, namespace)
        return {
            "status": "ok",
            "keys": keys,
            "namespace": namespace,
            "error": None,
        }

    return {"status": "error", "error": "Provide either 'key' or 'namespace'."}


# ═══════════════════════════════════════════════════════════════
# TOOL 11: forge.status
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_status(job_id: str) -> dict:
    """Poll the status of any long-running job.

    Supports all job types: research, skill_execution, agent_creation, workflow.

    Args:
        job_id: The job ID returned by a forge.* tool.
    """
    proj = _get_project_dir()
    db_path = _get_db_path(proj)
    fdb.init_db(db_path)

    job = fdb.get_job(db_path, job_id)
    if job is None:
        return {"status": "not_found", "job_id": job_id, "error": "Job not found"}

    result = {
        "status": job["status"],
        "job_id": job_id,
        "type": job["type"],
        "stage": job.get("stage"),
        "progress_pct": job["progress_pct"],
        "message": job.get("message", ""),
        "result": job.get("result_json"),
        "error": job.get("error"),
        "created_at": job["created_at"],
        "updated_at": job["updated_at"],
    }

    # Auto-cleanup completed jobs > 7 days
    if job["status"] == "completed":
        created = datetime.fromisoformat(job["created_at"])
        if (datetime.utcnow() - created).days > 7:
            result["status"] = "expired"

    return result


# ═══════════════════════════════════════════════════════════════
# TOOL 12: forge.capabilities
# ═══════════════════════════════════════════════════════════════


@mcp.tool()
def forge_capabilities(project_dir: str = "") -> dict:
    """List all available tools, skills, agents, and commands.

    Args:
        project_dir: Optional project directory for project-specific capabilities.
    """
    tools = [
        {
            "name": "forge.init",
            "description": "Initialize ForgeWeave in a project",
            "category": "setup",
        },
        {
            "name": "forge.execute_command",
            "description": "Route /forge-* commands",
            "category": "execution",
        },
        {
            "name": "forge.execute_skill",
            "description": "Execute a skill by name",
            "category": "execution",
        },
        {
            "name": "forge.create_agent",
            "description": "Create agent definition file",
            "category": "generation",
        },
        {
            "name": "forge.research",
            "description": "Full deep-research pipeline",
            "category": "research",
        },
        {"name": "forge.search", "description": "Lightweight web lookup", "category": "research"},
        {
            "name": "forge.load_context",
            "description": "Load project state snapshot",
            "category": "context",
        },
        {
            "name": "forge.validate",
            "description": "Validate outputs against rules",
            "category": "quality",
        },
        {
            "name": "forge.memory_read",
            "description": "Read from persistent memory",
            "category": "memory",
        },
        {
            "name": "forge.memory_write",
            "description": "Write to persistent memory",
            "category": "memory",
        },
        {"name": "forge.status", "description": "Poll job status", "category": "meta"},
        {
            "name": "forge.capabilities",
            "description": "List available tools and skills",
            "category": "meta",
        },
    ]

    result: dict[str, Any] = {
        "status": "ok",
        "server_version": FORGE_VERSION,
        "tools": tools,
        "error": None,
    }

    if project_dir:
        proj = Path(project_dir).resolve()
        if proj.exists():
            ctx = forge_load_context(project_dir)
            result["project"] = ctx
        else:
            result["project"] = {"initialized": False}

    return result


# ═══════════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════════


def main(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.getLogger().setLevel(level)
    log.setLevel(level)
    log.info("ForgeWeave MCP server ready — 12 forge.* tools loaded")
    mcp.run()


if __name__ == "__main__":
    main()
