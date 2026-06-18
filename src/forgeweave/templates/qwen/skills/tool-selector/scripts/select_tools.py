"""Map a task description to required tools and MCP actions.

Includes both the forge.* control plane tools and the research_* data plane tools.
"""
import argparse
import json
from pathlib import Path


TOOL_REGISTRY = {
    # Control plane: forge.* tools
    "forge_init": {"mcp": "forge.init", "description": "Initialize ForgeWeave in a project"},
    "forge_exec_command": {"mcp": "forge.execute_command", "description": "Route /forge-* command"},
    "forge_exec_skill": {"mcp": "forge.execute_skill", "description": "Execute a skill by name"},
    "forge_create_agent": {"mcp": "forge.create_agent", "description": "Create agent definition file"},
    "forge_research": {"mcp": "forge.research", "description": "Full deep-research pipeline"},
    "forge_search": {"mcp": "forge.search", "description": "Lightweight web lookup"},
    "forge_load_context": {"mcp": "forge.load_context", "description": "Load project state snapshot"},
    "forge_validate": {"mcp": "forge.validate", "description": "Validate outputs against rules"},
    "forge_memory_read": {"mcp": "forge.memory_read", "description": "Read from persistent memory"},
    "forge_memory_write": {"mcp": "forge.memory_write", "description": "Write to persistent memory"},
    "forge_status": {"mcp": "forge.status", "description": "Poll job status"},
    "forge_capabilities": {"mcp": "forge.capabilities", "description": "List available tools and skills"},
    # Data plane: research_* tools
    "fetch_url": {"mcp": "research_single_source", "description": "Fetch a single URL"},
    "crawl": {"mcp": "research_crawl_urls", "description": "Crawl multiple URLs"},
    "browse_js": {"mcp": "research_browse_js", "description": "Fetch JS-rendered page"},
    "screenshot": {"mcp": "research_screenshot", "description": "Full-page screenshot"},
    "extract_doc": {"mcp": "research_extract_document", "description": "Extract PDF/DOCX"},
    "index_doc": {"mcp": "research_index_latest", "description": "Index into vector DB"},
    "search": {"mcp": "research_search", "description": "Semantic search"},
    "synthesize": {"mcp": "research_synthesize", "description": "Search + group sources"},
    # Local tools
    "read_file": {"local": True, "description": "Read file from disk"},
    "write_file": {"local": True, "description": "Write file to disk"},
    "edit_file": {"local": True, "description": "Edit file on disk"},
    "run_command": {"local": True, "description": "Execute shell command"},
}

TASK_TOOL_MAP = {
    "init": ["forge_init"],
    "command": ["forge_exec_command"],
    "skill_exec": ["forge_exec_skill", "forge_load_context"],
    "agent_create": ["forge_create_agent"],
    "research": ["forge_research", "forge_status", "forge_memory_write", "crawl", "fetch_url", "browse_js", "search", "synthesize"],
    "quick_search": ["forge_search"],
    "validate": ["forge_validate"],
    "memory": ["forge_memory_read", "forge_memory_write"],
    "web_scrape": ["fetch_url", "browse_js", "screenshot"],
    "code_review": ["read_file", "forge_validate", "search"],
    "code_generation": ["read_file", "write_file", "edit_file"],
    "testing": ["read_file", "run_command"],
    "debugging": ["read_file", "run_command", "search", "forge_memory_read"],
    "documentation": ["read_file", "write_file", "fetch_url", "forge_research"],
    "architecture": ["read_file", "write_file", "forge_exec_skill"],
    "context": ["forge_load_context"],
    "capabilities": ["forge_capabilities"],
    "status": ["forge_status"],
}


def main():
    parser = argparse.ArgumentParser(description="Tool selector")
    parser.add_argument("task_type", choices=list(TASK_TOOL_MAP.keys()), help="Type of task")
    parser.add_argument("--detail", action="store_true", help="Show tool details")
    args = parser.parse_args()

    tool_names = TASK_TOOL_MAP[args.task_type]
    if args.detail:
        result = {name: TOOL_REGISTRY[name] for name in tool_names}
        print(json.dumps(result, indent=2))
    else:
        for name in tool_names:
            print(name)


if __name__ == "__main__":
    main()
