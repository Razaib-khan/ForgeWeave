"""Test that all forgeweave modules import correctly."""

import sys
from pathlib import Path

# This allows running directly from the source directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def test_core_imports():
    import forgeweave

    assert forgeweave.__version__ == "2.0.0"

    # New slim modules
    from forgeweave import cli, server

    assert cli is not None
    assert server is not None
    assert hasattr(server, "forge_init")


def test_cli_commands():
    from forgeweave.cli import main

    assert hasattr(main, "__call__")
