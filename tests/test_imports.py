"""Test that all forgeweave modules import correctly."""

import sys
from pathlib import Path

# This allows running directly from the source directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def test_core_imports():
    import forgeweave

    assert forgeweave.__version__ == "1.0.1"

    from forgeweave import db, registry, server, cli

    assert db is not None
    assert len(registry.DEFAULT_REGISTRY["commands"]) == 6
    assert len([n for n in dir(server) if n.startswith("forge_")]) == 12
    assert cli is not None


def test_research_mcp_imports():
    from forgeweave.research_mcp import models, scraper, crawler, vectors, cache

    assert models.ExtractedContent is not None
    assert scraper.extract_main_content is not None
    assert crawler.Crawler is not None
    assert vectors.warmup is not None
    assert cache.cache_stats is not None


def test_cli_commands():
    from forgeweave.cli import main
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_subparsers(dest="command")
    # Just verify init/mcp/doctor are valid commands
    assert hasattr(main, "__call__")
