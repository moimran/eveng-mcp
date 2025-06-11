"""Custom exceptions for EVE-NG MCP Server."""

from typing import Optional, Dict, Any


class EVENGMCPError(Exception):
    """Base exception for EVE-NG MCP Server."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class EVENGConnectionError(EVENGMCPError):
    """Raised when connection to EVE-NG server fails."""
    pass


class EVENGAuthenticationError(EVENGMCPError):
    """Raised when authentication with EVE-NG server fails."""
    pass


class EVENGAPIError(EVENGMCPError):
    """Raised when EVE-NG API returns an error."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class EVENGLabError(EVENGMCPError):
    """Raised when lab operations fail."""
    pass


class EVENGNodeError(EVENGMCPError):
    """Raised when node operations fail."""
    pass


class EVENGNetworkError(EVENGMCPError):
    """Raised when network operations fail."""
    pass


class EVENGConfigurationError(EVENGMCPError):
    """Raised when configuration is invalid."""
    pass


class EVENGTimeoutError(EVENGMCPError):
    """Raised when operations timeout."""
    pass


class MCPServerError(EVENGMCPError):
    """Raised when MCP server operations fail."""
    pass


class MCPToolError(EVENGMCPError):
    """Raised when MCP tool execution fails."""
    pass


class MCPResourceError(EVENGMCPError):
    """Raised when MCP resource operations fail."""
    pass


def handle_eveng_api_error(response) -> None:
    """Handle EVE-NG API error responses."""
    if response.status_code == 401:
        raise EVENGAuthenticationError(
            "Authentication failed. Please check your credentials.",
            details={"status_code": response.status_code}
        )
    elif response.status_code == 403:
        raise EVENGAuthenticationError(
            "Access forbidden. Insufficient permissions.",
            details={"status_code": response.status_code}
        )
    elif response.status_code == 404:
        raise EVENGAPIError(
            "Resource not found.",
            status_code=response.status_code
        )
    elif response.status_code == 409:
        raise EVENGAPIError(
            "Conflict. Resource already exists or is in use.",
            status_code=response.status_code
        )
    elif response.status_code >= 500:
        raise EVENGAPIError(
            "EVE-NG server error. Please try again later.",
            status_code=response.status_code
        )
    elif response.status_code >= 400:
        try:
            error_data = response.json()
            message = error_data.get('message', 'Unknown API error')
        except:
            message = f"API error: {response.status_code}"
        
        raise EVENGAPIError(
            message,
            status_code=response.status_code,
            response_data=error_data if 'error_data' in locals() else {}
        )
