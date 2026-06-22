# Changelog

All notable changes to ForgeWeave are documented in this file.

<p align="center">
  <a href="https://keepachangelog.com/en/1.1.0/">
    <img src="https://img.shields.io/badge/format-Keep%20a%20Changelog-ff69b4?style=flat-square" alt="Keep a Changelog">
  </a>
  <a href="https://semver.org/spec/v2.0.0.html">
    <img src="https://img.shields.io/badge/versioning-SemVer-22b8cf?style=flat-square" alt="SemVer">
  </a>
</p>

---

## [2.0.0] — 2026-06-22

> Major refactor: removed the custom MCP server (`research_mcp` module) and replaced it with TUI-native scaffolding. ForgeWeave is now a pure scaffolding CLI — **Templates + Rules + Skills. No server.**

### Added

- Interactive MCP server selection via InquirerPy during `forge init`
- Dynamic AGENTS.md generation — marks selected MCP servers with ✓ and unselected with —
- 6 MCP server definitions: Playwright (mandatory), Headroom (mandatory), Firecrawl, GitHub, SQLite, Context7
- 4 TUI adapter templates: OpenCode, Claude Code, Gemini CLI, Qwen Code
- Per-server skills: `firecrawl-mcp`, `github-mcp`, `sqlite-mcp`, `context7-mcp`, `headroom-mcp`
- Deep-research skill with MCP auto-detection and automatic skill conversion from findings
- `forge doctor` command for environment verification
- Full template directories with agents, commands, hooks, and skills for all 4 TUIs

### Changed

- Removed `research_mcp` module (browser, cache, crawler, documents, models, scraper, vectors, server)
- Removed `db.py`, `pipeline.py`, `registry.py` modules
- Simplified core to 4 files: `__init__.py`, `__main__.py`, `cli.py`, `server.py`
- Templates now use correct TUI directory structure (e.g., `.claude/skills/` instead of `claude/skills/`)
- Python minimum version raised to 3.14

### Fixed

- Template path resolution now correctly locates TUI-specific config files
- Qwen extension config writes to `qwen-extension.json` instead of `qwencode.json`
- AGENTS.md tables dynamically reflect actually selected MCP servers

---

## [1.0.2] — 2026-06-18

### Added

- GitHub issue and PR templates
- Pre-commit configuration (ruff, mypy, trailing-whitespace)
- `PROJECT_CONTEXT.md` with architecture documentation
- Contributor docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`

### Fixed

- Corrected relative paths in spec documents

---

## [1.0.1] — 2026-06-15

### Added

- Agent, Skill, and Adapter specification documents (AGENT_SPEC.md, SKILL_SPEC.md, ADAPTER_SPEC.md)
- Project-level agent registration config (AGENTS.md)
- Basic `forge init` CLI command with TUI selector
- Research MCP module with browser automation, crawling, document processing, and vector embeddings

---

## [1.0.0] — 2026-06-10

### Added

- Initial project structure
- Python package with setuptools build
- uv dependency management
