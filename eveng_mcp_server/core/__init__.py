"""Core module for EVE-NG MCP Server."""

from .exceptions import (
    EVENGMCPError,
    EVENGConnectionError,
    EVENGAuthenticationError,
    EVENGAPIError,
    EVENGLabError,
    EVENGNodeError,
    EVENGNetworkError,
    EVENGConfigurationError,
    EVENGTimeoutError,
    MCPServerError,
    MCPToolError,
    MCPResourceError,
    handle_eveng_api_error
)

from .eveng_client import (
    EVENGClientWrapper,
    get_eveng_client
)

__all__ = [
    # Exceptions
    "EVENGMCPError",
    "EVENGConnectionError",
    "EVENGAuthenticationError",
    "EVENGAPIError",
    "EVENGLabError",
    "EVENGNodeError",
    "EVENGNetworkError",
    "EVENGConfigurationError",
    "EVENGTimeoutError",
    "MCPServerError",
    "MCPToolError",
    "MCPResourceError",
    "handle_eveng_api_error",

    # Client
    "EVENGClientWrapper",
    "get_eveng_client"
]