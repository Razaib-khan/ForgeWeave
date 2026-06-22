"""ForgeWeave — Agent orchestration framework.

Provides project scaffolding (forge init), template distribution,
and AGENTS.md global rules. No custom MCP server — relies on
Playwright MCP for browser automation and TUI-native features
(plugins, hooks, subagents) for orchestration.

Design principle: Templates + Rules + Skills. No server.
"""

__version__ = "2.0.0"
__author__ = "ForgeWeave Core"
