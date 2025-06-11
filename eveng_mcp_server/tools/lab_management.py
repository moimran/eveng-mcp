"""Lab management tools for EVE-NG MCP Server."""

import asyncio
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
    async def list_labs(path: str = "/") -> list[TextContent]:
        """
        List available labs in EVE-NG.

        This tool retrieves a list of all labs available in the specified path
        on the EVE-NG server, including their basic information.
        """
        try:
            logger.info(f"Listing labs in path: {path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Get labs list
            labs = await eveng_client.list_labs(path)

            if not labs:
                return [TextContent(
                    type="text",
                    text=f"No labs found in path: {path}"
                )]

            # Format labs information
            labs_text = f"Labs in {path}:\n\n"

            for lab in labs:
                labs_text += f"📁 {lab.get('name', 'Unknown')}\n"
                labs_text += f"   File: {lab.get('file', 'Unknown')}\n"
                labs_text += f"   Path: {lab.get('path', 'Unknown')}\n"
                labs_text += f"   Full Path: {lab.get('full_path', 'Unknown')}\n"
                labs_text += f"   Modified: {lab.get('mtime', 'Unknown')}\n"
                labs_text += f"   💡 Use 'get_lab_details' with path '{lab.get('full_path', '')}' for detailed metadata\n"
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
    async def create_lab(name: str, path: str = "/", description: str = "", author: str = "", version: str = "1") -> list[TextContent]:
        """
        Create a new lab in EVE-NG.

        This tool creates a new lab with the specified name and metadata
        in the given path on the EVE-NG server.
        """
        try:
            logger.info(f"Creating lab: {name} in {path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Create lab
            lab = await eveng_client.create_lab(
                name=name,
                path=path,
                description=description,
                author=author,
                version=version
            )

            return [TextContent(
                type="text",
                text=f"Successfully created lab!\n\n"
                     f"Name: {name}\n"
                     f"Path: {path}\n"
                     f"Description: {description}\n"
                     f"Author: {author}\n"
                     f"Version: {version}\n\n"
                     f"Lab is ready for adding nodes and networks."
            )]

        except Exception as e:
            logger.error(f"Failed to create lab: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to create lab: {str(e)}"
            )]
    
    @mcp.tool()
    async def get_lab_details(lab_path: str) -> list[TextContent]:
        """
        Get detailed information about a specific lab.

        This tool retrieves comprehensive information about a lab including
        its metadata, nodes, networks, and current status.
        """
        try:
            logger.info(f"Getting details for lab: {lab_path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Get lab details
            lab_response = await eveng_client.get_lab(lab_path)

            # Extract lab data from the response
            lab = lab_response.get('data', {})

            # Get nodes, networks, and topology separately
            try:
                nodes_response = await asyncio.to_thread(eveng_client.api.list_nodes, lab_path)
                nodes = nodes_response.get('data', {})
            except Exception as e:
                logger.warning(f"Failed to get nodes for lab {lab_path}: {e}")
                nodes = {}

            try:
                networks_response = await asyncio.to_thread(eveng_client.api.list_lab_networks, lab_path)
                networks = networks_response.get('data', {})
            except Exception as e:
                logger.warning(f"Failed to get networks for lab {lab_path}: {e}")
                networks = {}

            try:
                links_response = await asyncio.to_thread(eveng_client.api.list_lab_links, lab_path)
                links = links_response.get('data', {})
            except Exception as e:
                logger.warning(f"Failed to get links for lab {lab_path}: {e}")
                links = {}

            # Get node interfaces for each node
            node_interfaces = {}
            for node_id in nodes.keys():
                try:
                    interfaces_response = await asyncio.to_thread(eveng_client.api.get_node_interfaces, lab_path, node_id)
                    node_interfaces[node_id] = interfaces_response.get('data', {})
                except Exception as e:
                    logger.warning(f"Failed to get interfaces for node {node_id}: {e}")
                    node_interfaces[node_id] = {}

            # Format lab information
            details_text = f"Lab Details: {lab.get('name', 'Unknown')}\n\n"

            # Basic information
            details_text += "📋 Basic Information:\n"
            details_text += f"   Name: {lab.get('name', 'Unknown')}\n"
            details_text += f"   Filename: {lab.get('filename', 'Unknown')}\n"
            details_text += f"   Path: {lab_path}\n"
            details_text += f"   Description: {lab.get('description', 'No description')}\n"
            details_text += f"   Author: {lab.get('author', 'Unknown')}\n"
            details_text += f"   Version: {lab.get('version', 'Unknown')}\n"
            details_text += f"   ID: {lab.get('id', 'Unknown')}\n"
            details_text += f"   Script Timeout: {lab.get('scripttimeout', 'Unknown')} seconds\n"
            details_text += f"   Lock Status: {'Locked' if lab.get('lock', 0) else 'Unlocked'}\n\n"

            # Nodes information
            details_text += f"🖥️  Nodes ({len(nodes)}):\n"
            if nodes:
                for node_id, node in nodes.items():
                    # Parse status
                    status_map = {0: "Stopped", 1: "Starting", 2: "Running", 3: "Stopping"}
                    status = status_map.get(node.get('status', 0), f"Unknown ({node.get('status', 0)})")

                    # Parse console URL to extract port
                    console_url = node.get('url', '')
                    console_port = ''
                    if console_url and ':' in console_url:
                        console_port = console_url.split(':')[-1]

                    details_text += f"   • {node.get('name', f'Node {node_id}')}\n"
                    details_text += f"     ID: {node_id}\n"
                    details_text += f"     Type: {node.get('type', 'Unknown')}\n"
                    details_text += f"     Template: {node.get('template', 'Unknown')}\n"
                    details_text += f"     Image: {node.get('image', 'Unknown')}\n"
                    details_text += f"     Status: {status}\n"
                    details_text += f"     CPU: {node.get('cpu', 'Unknown')}\n"
                    details_text += f"     RAM: {node.get('ram', 'Unknown')} MB\n"
                    details_text += f"     Ethernet Ports: {node.get('ethernet', 'Unknown')}\n"
                    details_text += f"     Console Type: {node.get('console', 'None')}\n"
                    if console_url:
                        details_text += f"     Console URL: {console_url}\n"
                        if console_port:
                            details_text += f"     Console Port: {console_port}\n"
                    details_text += f"     UUID: {node.get('uuid', 'Unknown')}\n"

                    # Add interface information
                    interfaces = node_interfaces.get(node_id, {})
                    ethernet_interfaces = interfaces.get('ethernet', [])
                    serial_interfaces = interfaces.get('serial', [])

                    if ethernet_interfaces or serial_interfaces:
                        details_text += f"     Interfaces:\n"

                        for eth_int in ethernet_interfaces:
                            int_name = eth_int.get('name', 'Unknown')
                            net_id = eth_int.get('network_id', 0)
                            if net_id == 0:
                                connection = "Not connected"
                            else:
                                # Find network name
                                network_name = networks.get(str(net_id), {}).get('name', f'Network {net_id}')
                                connection = f"Connected to {network_name}"
                            details_text += f"       - {int_name}: {connection}\n"

                        for ser_int in serial_interfaces:
                            int_name = ser_int.get('name', 'Unknown')
                            details_text += f"       - {int_name} (Serial): Not connected\n"

                    details_text += "\n"
            else:
                details_text += "   No nodes configured\n"
            details_text += "\n"

            # Networks information
            details_text += f"🌐 Networks ({len(networks)}):\n"
            if networks:
                for net_id, network in networks.items():
                    details_text += f"   • {network.get('name', f'Network {net_id}')}\n"
                    details_text += f"     ID: {net_id}\n"
                    details_text += f"     Type: {network.get('type', 'Unknown')}\n"
                    details_text += f"     Connected Devices: {network.get('count', 0)}\n"
                    details_text += f"     Visibility: {'Visible' if network.get('visibility', 1) else 'Hidden'}\n"
                    details_text += f"     Icon: {network.get('icon', 'Unknown')}\n"
                    details_text += f"     Position: ({network.get('left', 'Unknown')}, {network.get('top', 'Unknown')})\n"
                    details_text += "\n"
            else:
                details_text += "   No networks configured\n"

            # Topology/Links information
            details_text += f"\n🔗 Topology & Connections:\n"
            if links:
                ethernet_links = links.get('ethernet', {})
                serial_links = links.get('serial', [])

                if ethernet_links:
                    details_text += f"   Ethernet Connections:\n"
                    for net_id, net_name in ethernet_links.items():
                        details_text += f"     - Network {net_id} ({net_name})\n"

                if serial_links:
                    details_text += f"   Serial Connections:\n"
                    for serial_link in serial_links:
                        details_text += f"     - {serial_link}\n"

                if not ethernet_links and not serial_links:
                    details_text += "   No connections configured\n"
            else:
                details_text += "   No topology information available\n"

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
    async def delete_lab(lab_path: str) -> list[TextContent]:
        """
        Delete a lab from EVE-NG.

        This tool permanently deletes a lab and all its associated resources
        from the EVE-NG server. This action cannot be undone.
        """
        try:
            logger.info(f"Deleting lab: {lab_path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Delete lab
            await eveng_client.client.delete_lab(lab_path)

            return [TextContent(
                type="text",
                text=f"Successfully deleted lab: {lab_path}\n\n"
                     f"⚠️  This action cannot be undone. The lab and all its "
                     f"associated resources have been permanently removed."
            )]

        except Exception as e:
            logger.error(f"Failed to delete lab: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to delete lab: {str(e)}"
            )]
