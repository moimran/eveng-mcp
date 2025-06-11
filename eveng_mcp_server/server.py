"""Main MCP server implementation for EVE-NG integration."""

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Sequence
from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions
from mcp.types import Resource, Tool, Prompt

from .config import get_config, configure_logging, get_logger
from .core import get_eveng_client, EVENGConnectionError
from .tools import register_tools
from .resources import register_resources
from .prompts import register_prompts


class EVENGMCPServer:
    """Main EVE-NG MCP Server class."""

    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("EVENGMCPServer")

        # Get EVE-NG client
        self.eveng_client = get_eveng_client()

        # Create lifespan context manager
        @asynccontextmanager
        async def lifespan(mcp: FastMCP):
            # Startup
            await self.startup()
            try:
                yield
            finally:
                # Shutdown
                await self.shutdown()

        # Initialize FastMCP server with lifespan
        self.mcp = FastMCP(
            name=self.config.mcp.name,
            version=self.config.mcp.version,
            lifespan=lifespan
        )

        # Register tools, resources, and prompts
        self._register_components()

    def _register_components(self) -> None:
        """Register tools, resources, and prompts."""
        self.logger.info("Registering MCP components")

        # Register tools
        register_tools(self.mcp, self.eveng_client)

        # Register resources
        register_resources(self.mcp, self.eveng_client)

        # Register prompts
        register_prompts(self.mcp, self.eveng_client)

        self.logger.info("Successfully registered all MCP components")
    
    async def startup(self) -> None:
        """Server startup handler."""
        self.logger.info("Starting EVE-NG MCP Server")
        
        try:
            # Test EVE-NG connection
            self.logger.info("Testing EVE-NG connection")
            if await self.eveng_client.test_connection():
                self.logger.info("EVE-NG connection test successful")
            else:
                self.logger.warning("EVE-NG connection test failed - server will continue but some features may not work")
        
        except Exception as e:
            self.logger.error(f"Error during startup: {e}")
            # Don't fail startup if EVE-NG is not available
            self.logger.warning("Continuing startup without EVE-NG connection")
        
        self.logger.info("EVE-NG MCP Server started successfully")
    
    async def shutdown(self) -> None:
        """Server shutdown handler."""
        self.logger.info("Shutting down EVE-NG MCP Server")
        
        try:
            # Disconnect from EVE-NG
            await self.eveng_client.disconnect()
            self.logger.info("Disconnected from EVE-NG server")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
        
        self.logger.info("EVE-NG MCP Server shutdown complete")
    
    def run_stdio(self) -> None:
        """Run the server with stdio transport."""
        self.logger.info("Starting MCP server with stdio transport")
        self.mcp.run(transport="stdio")

    def run_sse(self, host: str = None, port: int = None) -> None:
        """Run the server with SSE transport."""
        host = host or self.config.mcp.host
        port = port or self.config.mcp.port

        self.logger.info(f"Starting MCP server with SSE transport on {host}:{port}")

        # Update settings for SSE
        self.mcp.settings.host = host
        self.mcp.settings.port = port

        self.mcp.run(transport="sse")


def create_server() -> EVENGMCPServer:
    """Create and configure the EVE-NG MCP server."""
    # Configure logging
    configure_logging()
    
    # Create server instance
    server = EVENGMCPServer()
    
    return server


def main() -> None:
    """Main entry point for the server."""
    config = get_config()
    server = create_server()

    if config.mcp.transport == "stdio":
        server.run_stdio()
    else:
        server.run_sse()


if __name__ == "__main__":
    main()
