"""Connection management tools for EVE-NG MCP Server."""

from typing import Any, Dict, TYPE_CHECKING
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from ..config import get_logger
from ..core.exceptions import EVENGConnectionError, EVENGAuthenticationError


logger = get_logger("ConnectionTools")


class ConnectServerArgs(BaseModel):
    """Arguments for connect_eveng_server tool."""
    host: str = Field(description="EVE-NG server hostname or IP address")
    username: str = Field(description="Username for authentication")
    password: str = Field(description="Password for authentication")
    port: int = Field(default=80, description="Server port (default: 80)")
    protocol: str = Field(default="http", description="Protocol (http/https, default: http)")


class TestConnectionArgs(BaseModel):
    """Arguments for test_connection tool."""
    pass  # No arguments needed


def register_connection_tools(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register connection management tools."""
    
    @mcp.tool()
    async def connect_eveng_server(arguments: ConnectServerArgs) -> list[TextContent]:
        """
        Connect to EVE-NG server and authenticate.
        
        This tool establishes a connection to the EVE-NG server using the provided
        credentials. The connection will be maintained for subsequent operations.
        """
        try:
            logger.info(f"Attempting to connect to EVE-NG server at {arguments.host}")
            
            # Update client configuration
            config = eveng_client.config
            config.eveng.host = arguments.host
            config.eveng.username = arguments.username
            config.eveng.password = arguments.password
            config.eveng.port = arguments.port
            config.eveng.protocol = arguments.protocol
            
            # Connect to server
            await eveng_client.connect()
            
            # Get server status for confirmation
            status = await eveng_client.get_server_status()
            
            result = {
                "status": "connected",
                "server": f"{arguments.protocol}://{arguments.host}:{arguments.port}",
                "username": arguments.username,
                "server_info": status
            }
            
            logger.info(f"Successfully connected to EVE-NG server at {arguments.host}")
            
            return [TextContent(
                type="text",
                text=f"Successfully connected to EVE-NG server!\n\n"
                     f"Server: {arguments.protocol}://{arguments.host}:{arguments.port}\n"
                     f"Username: {arguments.username}\n"
                     f"Server Version: {status.get('version', 'Unknown')}\n"
                     f"Status: {status.get('status', 'Unknown')}"
            )]
            
        except EVENGAuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            return [TextContent(
                type="text",
                text=f"Authentication failed: {str(e)}\n\n"
                     f"Please check your username and password and try again."
            )]
            
        except EVENGConnectionError as e:
            logger.error(f"Connection failed: {e}")
            return [TextContent(
                type="text",
                text=f"Connection failed: {str(e)}\n\n"
                     f"Please check the server address and network connectivity."
            )]
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return [TextContent(
                type="text",
                text=f"Unexpected error occurred: {str(e)}\n\n"
                     f"Please check your configuration and try again."
            )]
    
    @mcp.tool()
    async def disconnect_eveng_server() -> list[TextContent]:
        """
        Disconnect from EVE-NG server.
        
        This tool closes the connection to the EVE-NG server and cleans up
        any active sessions.
        """
        try:
            logger.info("Disconnecting from EVE-NG server")
            await eveng_client.disconnect()
            
            return [TextContent(
                type="text",
                text="Successfully disconnected from EVE-NG server."
            )]
            
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
            return [TextContent(
                type="text",
                text=f"Warning: Error during disconnect: {str(e)}\n\n"
                     f"Connection may have been closed already."
            )]
    
    @mcp.tool()
    async def test_connection(arguments: TestConnectionArgs) -> list[TextContent]:
        """
        Test connection to EVE-NG server.
        
        This tool verifies that the connection to the EVE-NG server is working
        properly and returns server status information.
        """
        try:
            logger.info("Testing EVE-NG server connection")
            
            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]
            
            # Test connection by getting server status
            status = await eveng_client.get_server_status()
            
            return [TextContent(
                type="text",
                text=f"Connection test successful!\n\n"
                     f"Server: {eveng_client.config.eveng.base_url}\n"
                     f"Status: Connected\n"
                     f"Server Version: {status.get('version', 'Unknown')}\n"
                     f"Server Status: {status.get('status', 'Unknown')}\n"
                     f"Uptime: {status.get('uptime', 'Unknown')}"
            )]
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return [TextContent(
                type="text",
                text=f"Connection test failed: {str(e)}\n\n"
                     f"Please check your connection and try again."
            )]
    
    @mcp.tool()
    async def get_server_info() -> list[TextContent]:
        """
        Get EVE-NG server information and status.
        
        This tool retrieves detailed information about the EVE-NG server
        including version, status, capabilities, and system information.
        """
        try:
            logger.info("Retrieving EVE-NG server information")
            
            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]
            
            # Get server status and information
            status = await eveng_client.get_server_status()
            
            # Format the information nicely
            info_text = "EVE-NG Server Information:\n\n"
            info_text += f"Server URL: {eveng_client.config.eveng.base_url}\n"
            info_text += f"Version: {status.get('version', 'Unknown')}\n"
            info_text += f"Status: {status.get('status', 'Unknown')}\n"
            info_text += f"Uptime: {status.get('uptime', 'Unknown')}\n"
            
            if 'cpu' in status:
                info_text += f"CPU Usage: {status['cpu']}%\n"
            if 'memory' in status:
                info_text += f"Memory Usage: {status['memory']}%\n"
            if 'disk' in status:
                info_text += f"Disk Usage: {status['disk']}%\n"
            
            return [TextContent(
                type="text",
                text=info_text
            )]
            
        except Exception as e:
            logger.error(f"Failed to get server info: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to get server information: {str(e)}"
            )]
