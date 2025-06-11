"""Resources module for EVE-NG MCP Server."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from .dynamic import register_dynamic_resources
from .static import register_static_resources


def register_resources(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register all MCP resources."""

    # Register dynamic resources (real-time data)
    register_dynamic_resources(mcp, eveng_client)

    # Register static resources (documentation, examples)
    register_static_resources(mcp, eveng_client)


__all__ = [
    "register_resources"
]