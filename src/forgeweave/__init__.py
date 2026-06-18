"""ForgeWeave — Framework-agnostic agent orchestration layer.

Exposes 12 high-level forge.* tools via MCP that form the execution interface.
Internal pipeline stages (planner, researchers, validator, synthesizer) are
implementation details and never exposed as separate tools.

Design principle: Expose capabilities. Hide orchestration.
"""

__version__ = "1.0.1"
__author__ = "ForgeWeave Core"
