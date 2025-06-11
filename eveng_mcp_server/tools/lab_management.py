"""Lab management tools for EVE-NG MCP Server."""

import json
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from ..config import get_logger
from ..core.exceptions import EVENGAPIError, EVENGLabError


logger = get_logger("LabManagementTools")


class ListLabsArgs(BaseModel):
    """Arguments for list_labs tool."""
    path: str = Field(default="/", description="Path to list labs from (default: /)")


class CreateLabArgs(BaseModel):
    """Arguments for create_lab tool."""
    name: str = Field(description="Name of the lab")
    path: str = Field(default="/", description="Path where to create the lab (default: /)")
    description: str = Field(default="", description="Lab description")
    author: str = Field(default="", description="Lab author")
    version: str = Field(default="1", description="Lab version")


class GetLabDetailsArgs(BaseModel):
    """Arguments for get_lab_details tool."""
    lab_path: str = Field(description="Full path to the lab (e.g., /lab_name.unl)")


class DeleteLabArgs(BaseModel):
    """Arguments for delete_lab tool."""
    lab_path: str = Field(description="Full path to the lab to delete")


def register_lab_tools(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register lab management tools."""
    
    @mcp.tool()
    async def list_labs(arguments: ListLabsArgs) -> list[TextContent]:
        """
        List available labs in EVE-NG.
        
        This tool retrieves a list of all labs available in the specified path
        on the EVE-NG server, including their basic information.
        """
        try:
            logger.info(f"Listing labs in path: {arguments.path}")
            
            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]
            
            # Get labs list
            labs = await eveng_client.list_labs(arguments.path)
            
            if not labs:
                return [TextContent(
                    type="text",
                    text=f"No labs found in path: {arguments.path}"
                )]
            
            # Format labs information
            labs_text = f"Labs in {arguments.path}:\n\n"
            
            for lab in labs:
                labs_text += f"📁 {lab.get('name', 'Unknown')}\n"
                labs_text += f"   Path: {lab.get('path', 'Unknown')}\n"
                labs_text += f"   Description: {lab.get('description', 'No description')}\n"
                labs_text += f"   Author: {lab.get('author', 'Unknown')}\n"
                labs_text += f"   Version: {lab.get('version', 'Unknown')}\n"
                labs_text += f"   Modified: {lab.get('modified', 'Unknown')}\n"
                labs_text += "\n"
            
            return [TextContent(
                type="text",
                text=labs_text
            )]
            
        except Exception as e:
            logger.error(f"Failed to list labs: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to list labs: {str(e)}"
            )]
    
    @mcp.tool()
    async def create_lab(arguments: CreateLabArgs) -> list[TextContent]:
        """
        Create a new lab in EVE-NG.
        
        This tool creates a new lab with the specified name and metadata
        in the given path on the EVE-NG server.
        """
        try:
            logger.info(f"Creating lab: {arguments.name} in {arguments.path}")
            
            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]
            
            # Create lab
            lab = await eveng_client.create_lab(
                name=arguments.name,
                path=arguments.path,
                description=arguments.description,
                author=arguments.author,
                version=arguments.version
            )
            
            return [TextContent(
                type="text",
                text=f"Successfully created lab!\n\n"
                     f"Name: {arguments.name}\n"
                     f"Path: {arguments.path}\n"
                     f"Description: {arguments.description}\n"
                     f"Author: {arguments.author}\n"
                     f"Version: {arguments.version}\n\n"
                     f"Lab is ready for adding nodes and networks."
            )]
            
        except Exception as e:
            logger.error(f"Failed to create lab: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to create lab: {str(e)}"
            )]
    
    @mcp.tool()
    async def get_lab_details(arguments: GetLabDetailsArgs) -> list[TextContent]:
        """
        Get detailed information about a specific lab.
        
        This tool retrieves comprehensive information about a lab including
        its metadata, nodes, networks, and current status.
        """
        try:
            logger.info(f"Getting details for lab: {arguments.lab_path}")
            
            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]
            
            # Get lab details
            lab = await eveng_client.get_lab(arguments.lab_path)
            
            # Format lab information
            details_text = f"Lab Details: {lab.get('name', 'Unknown')}\n\n"
            
            # Basic information
            details_text += "📋 Basic Information:\n"
            details_text += f"   Name: {lab.get('name', 'Unknown')}\n"
            details_text += f"   Path: {lab.get('path', 'Unknown')}\n"
            details_text += f"   Description: {lab.get('description', 'No description')}\n"
            details_text += f"   Author: {lab.get('author', 'Unknown')}\n"
            details_text += f"   Version: {lab.get('version', 'Unknown')}\n"
            details_text += f"   Created: {lab.get('created', 'Unknown')}\n"
            details_text += f"   Modified: {lab.get('modified', 'Unknown')}\n\n"
            
            # Nodes information
            nodes = lab.get('nodes', {})
            details_text += f"🖥️  Nodes ({len(nodes)}):\n"
            if nodes:
                for node_id, node in nodes.items():
                    details_text += f"   • {node.get('name', f'Node {node_id}')}\n"
                    details_text += f"     Type: {node.get('type', 'Unknown')}\n"
                    details_text += f"     Template: {node.get('template', 'Unknown')}\n"
                    details_text += f"     Status: {node.get('status', 'Unknown')}\n"
            else:
                details_text += "   No nodes configured\n"
            details_text += "\n"
            
            # Networks information
            networks = lab.get('networks', {})
            details_text += f"🌐 Networks ({len(networks)}):\n"
            if networks:
                for net_id, network in networks.items():
                    details_text += f"   • {network.get('name', f'Network {net_id}')}\n"
                    details_text += f"     Type: {network.get('type', 'Unknown')}\n"
            else:
                details_text += "   No networks configured\n"
            
            return [TextContent(
                type="text",
                text=details_text
            )]
            
        except Exception as e:
            logger.error(f"Failed to get lab details: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to get lab details: {str(e)}"
            )]
    
    @mcp.tool()
    async def delete_lab(arguments: DeleteLabArgs) -> list[TextContent]:
        """
        Delete a lab from EVE-NG.
        
        This tool permanently deletes a lab and all its associated resources
        from the EVE-NG server. This action cannot be undone.
        """
        try:
            logger.info(f"Deleting lab: {arguments.lab_path}")
            
            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]
            
            # Delete lab
            await eveng_client.client.delete_lab(arguments.lab_path)
            
            return [TextContent(
                type="text",
                text=f"Successfully deleted lab: {arguments.lab_path}\n\n"
                     f"⚠️  This action cannot be undone. The lab and all its "
                     f"associated resources have been permanently removed."
            )]
            
        except Exception as e:
            logger.error(f"Failed to delete lab: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to delete lab: {str(e)}"
            )]
