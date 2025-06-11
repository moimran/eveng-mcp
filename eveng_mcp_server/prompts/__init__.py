"""Prompts module for EVE-NG MCP Server."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from .workflows import register_workflow_prompts


def register_prompts(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register all MCP prompts."""

    # Register workflow prompts for guided operations
    register_workflow_prompts(mcp, eveng_client)


__all__ = [
    "register_prompts"
]