"""ForgeWeave MCP Server — run with: python -m forge_mcp.server [--verbose]"""

import sys
from forgeweave.server import main

if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    main(verbose=verbose)
