"""Main entry point for EVE-NG MCP Server."""

import asyncio
from eveng_mcp_server.server import main

if __name__ == "__main__":
    asyncio.run(main())
