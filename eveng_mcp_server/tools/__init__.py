"""Tools module for EVE-NG MCP Server."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from .connection import register_connection_tools
from .lab_management import register_lab_tools
from .node_management import register_node_tools
from .network_management import register_network_tools


def register_tools(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register all MCP tools."""

    # Connection management tools
    register_connection_tools(mcp, eveng_client)

    # Lab management tools
    register_lab_tools(mcp, eveng_client)

    # Node management tools
    register_node_tools(mcp, eveng_client)

    # Network management tools
    register_network_tools(mcp, eveng_client)


__all__ = [
    "register_tools"
]