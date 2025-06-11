"""Network management tools for EVE-NG MCP Server."""

import json
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from ..config import get_logger
from ..core.exceptions import EVENGAPIError


logger = get_logger("NetworkManagementTools")


class ListNetworksArgs(BaseModel):
    """Arguments for list_networks tool."""
    lab_path: str = Field(description="Full path to the lab (e.g., /lab_name.unl)")


class CreateNetworkArgs(BaseModel):
    """Arguments for create_network tool."""
    lab_path: str = Field(description="Full path to the lab (e.g., /lab_name.unl)")
    network_type: str = Field(description="Network type (bridge, cloud, nat, etc.)")
    name: str = Field(default="", description="Network name (optional)")
    left: int = Field(default=50, description="Position from left (percentage, 0-100)")
    top: int = Field(default=50, description="Position from top (percentage, 0-100)")


class DeleteNetworkArgs(BaseModel):
    """Arguments for delete_network tool."""
    lab_path: str = Field(description="Full path to the lab (e.g., /lab_name.unl)")
    network_id: str = Field(description="Network ID to delete")


class ConnectNodeToNetworkArgs(BaseModel):
    """Arguments for connect_node_to_network tool."""
    lab_path: str = Field(description="Full path to the lab (e.g., /lab_name.unl)")
    node_id: str = Field(description="Source node ID")
    node_interface: str = Field(description="Node interface name (e.g., 'Gi0/0', 'eth0')")
    network_id: str = Field(description="Target network ID")


class ConnectNodeToNodeArgs(BaseModel):
    """Arguments for connect_node_to_node tool."""
    lab_path: str = Field(description="Full path to the lab (e.g., /lab_name.unl)")
    src_node_id: str = Field(description="Source node ID")
    src_interface: str = Field(description="Source node interface name")
    dst_node_id: str = Field(description="Destination node ID")
    dst_interface: str = Field(description="Destination node interface name")


class GetTopologyArgs(BaseModel):
    """Arguments for get_lab_topology tool."""
    lab_path: str = Field(description="Full path to the lab (e.g., /lab_name.unl)")


def register_network_tools(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register network management tools."""

    @mcp.tool()
    async def list_network_types(arguments: ListNetworksArgs) -> list[TextContent]:
        """
        List available network types in EVE-NG.

        This tool retrieves all available network types that can be used
        to create networks in labs (bridge, cloud, nat, etc.).
        """
        try:
            logger.info("Listing available network types")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Get network types
            network_types = await eveng_client.list_network_types()

            if not network_types.get('data'):
                return [TextContent(
                    type="text",
                    text="No network types found on the server."
                )]

            # Format network types information
            types_text = "Available Network Types:\n\n"

            for type_name, type_info in network_types['data'].items():
                types_text += f"🌐 {type_name}\n"
                types_text += f"   Description: {type_info.get('description', 'No description')}\n"
                types_text += f"   Type: {type_info.get('type', 'Unknown')}\n"
                types_text += "\n"

            return [TextContent(
                type="text",
                text=types_text
            )]

        except Exception as e:
            logger.error(f"Failed to list network types: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to list network types: {str(e)}"
            )]

    @mcp.tool()
    async def list_lab_networks(arguments: ListNetworksArgs) -> list[TextContent]:
        """
        List all networks in a lab.

        This tool retrieves information about all networks configured
        in the specified lab, including their types and connections.
        """
        try:
            logger.info(f"Listing networks in lab: {arguments.lab_path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Get lab networks
            networks = await eveng_client.list_lab_networks(arguments.lab_path)

            if not networks.get('data'):
                return [TextContent(
                    type="text",
                    text=f"No networks found in lab: {arguments.lab_path}"
                )]

            # Format networks information
            networks_text = f"Networks in {arguments.lab_path}:\n\n"

            for net_id, network in networks['data'].items():
                networks_text += f"🌐 {network.get('name', f'Network {net_id}')} (ID: {net_id})\n"
                networks_text += f"   Type: {network.get('type', 'Unknown')}\n"
                networks_text += f"   Visibility: {'Visible' if network.get('visibility') == 1 else 'Hidden'}\n"
                networks_text += f"   Position: ({network.get('left', 0)}%, {network.get('top', 0)}%)\n"
                networks_text += "\n"

            return [TextContent(
                type="text",
                text=networks_text
            )]

        except Exception as e:
            logger.error(f"Failed to list lab networks: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to list lab networks: {str(e)}"
            )]

    @mcp.tool()
    async def create_lab_network(arguments: CreateNetworkArgs) -> list[TextContent]:
        """
        Create a network in a lab.

        This tool creates a new network (cloud, bridge, NAT, etc.) in the lab
        with the specified type and positioning.
        """
        try:
            logger.info(f"Creating network in lab: {arguments.lab_path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Create network
            result = await eveng_client.add_lab_network(
                arguments.lab_path,
                arguments.network_type,
                name=arguments.name,
                left=arguments.left,
                top=arguments.top,
                visibility=1  # Make network visible by default
            )

            if result.get('status') == 'success':
                net_id = result.get('data', {}).get('id', 'Unknown')
                return [TextContent(
                    type="text",
                    text=f"Successfully created network in lab!\n\n"
                         f"Lab: {arguments.lab_path}\n"
                         f"Network Type: {arguments.network_type}\n"
                         f"Network ID: {net_id}\n"
                         f"Name: {arguments.name or f'Network{net_id}'}\n"
                         f"Position: ({arguments.left}%, {arguments.top}%)\n\n"
                         f"Network created successfully. You can now connect nodes to it."
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to create network: {result.get('message', 'Unknown error')}"
                )]

        except Exception as e:
            logger.error(f"Failed to create network: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to create network: {str(e)}"
            )]

    @mcp.tool()
    async def delete_lab_network(arguments: DeleteNetworkArgs) -> list[TextContent]:
        """
        Delete a network from a lab.

        This tool permanently removes a network from the lab. All connections
        to this network will be lost. This action cannot be undone.
        """
        try:
            logger.info(f"Deleting network {arguments.network_id} from {arguments.lab_path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Delete network
            result = await eveng_client.delete_lab_network(arguments.lab_path, int(arguments.network_id))

            if result.get('status') == 'success':
                return [TextContent(
                    type="text",
                    text=f"Successfully deleted network {arguments.network_id} from {arguments.lab_path}\n\n"
                         f"⚠️  The network has been permanently removed from the lab.\n"
                         f"All connections to this network have been lost.\n"
                         f"This action cannot be undone."
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to delete network: {result.get('message', 'Unknown error')}"
                )]

        except Exception as e:
            logger.error(f"Failed to delete network: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to delete network: {str(e)}"
            )]

    @mcp.tool()
    async def connect_node_to_network(arguments: ConnectNodeToNetworkArgs) -> list[TextContent]:
        """
        Connect a node to a network.

        This tool creates a connection between a node interface and a network
        in the lab, enabling communication through that network.
        """
        try:
            logger.info(f"Connecting node {arguments.node_id} to network {arguments.network_id}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Connect node to network (cloud)
            result = await eveng_client.connect_node_to_cloud(
                arguments.lab_path,
                arguments.node_id,
                arguments.node_interface,
                arguments.network_id
            )

            if result.get('status') == 'success':
                return [TextContent(
                    type="text",
                    text=f"Successfully connected node to network!\n\n"
                         f"Lab: {arguments.lab_path}\n"
                         f"Node: {arguments.node_id}\n"
                         f"Interface: {arguments.node_interface}\n"
                         f"Network: {arguments.network_id}\n\n"
                         f"Connection established successfully."
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Failed to connect node to network: {result.get('message', 'Unknown error')}"
                )]

        except Exception as e:
            logger.error(f"Failed to connect node to network: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to connect node to network: {str(e)}"
            )]

    @mcp.tool()
    async def connect_node_to_node(arguments: ConnectNodeToNodeArgs) -> list[TextContent]:
        """
        Connect two nodes together directly.

        This tool creates a direct point-to-point connection between two nodes
        in the lab, enabling direct communication between them.
        """
        try:
            logger.info(f"Connecting node {arguments.src_node_id} to node {arguments.dst_node_id}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Connect nodes together
            result = await eveng_client.connect_node_to_node(
                arguments.lab_path,
                arguments.src_node_id,
                arguments.src_interface,
                arguments.dst_node_id,
                arguments.dst_interface
            )

            if result:  # connect_node_to_node returns boolean
                return [TextContent(
                    type="text",
                    text=f"Successfully connected nodes!\n\n"
                         f"Lab: {arguments.lab_path}\n"
                         f"Source Node: {arguments.src_node_id} ({arguments.src_interface})\n"
                         f"Destination Node: {arguments.dst_node_id} ({arguments.dst_interface})\n\n"
                         f"Point-to-point connection established successfully."
                )]
            else:
                return [TextContent(
                    type="text",
                    text="Failed to connect nodes: Connection could not be established."
                )]

        except Exception as e:
            logger.error(f"Failed to connect nodes: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to connect nodes: {str(e)}"
            )]

    @mcp.tool()
    async def get_lab_topology(arguments: GetTopologyArgs) -> list[TextContent]:
        """
        Get lab topology information.

        This tool retrieves the complete topology of the lab including
        all nodes, networks, and their connections.
        """
        try:
            logger.info(f"Getting topology for lab: {arguments.lab_path}")

            if not eveng_client.is_connected:
                return [TextContent(
                    type="text",
                    text="Not connected to EVE-NG server. Use connect_eveng_server tool first."
                )]

            # Get topology
            topology = await eveng_client.get_lab_topology(arguments.lab_path)

            if not topology.get('data'):
                return [TextContent(
                    type="text",
                    text=f"No topology information found for lab: {arguments.lab_path}"
                )]

            # Format topology information
            topology_text = f"Lab Topology: {arguments.lab_path}\n\n"

            topology_data = topology['data']

            # Show connections
            topology_text += "🔗 Connections:\n"
            if topology_data:
                for connection_id, connection in topology_data.items():
                    src_type = "Node" if connection.get('source_type') == 'node' else "Network"
                    dst_type = "Node" if connection.get('destination_type') == 'node' else "Network"

                    topology_text += f"   {src_type} {connection.get('source', 'Unknown')}"
                    if connection.get('source_label'):
                        topology_text += f" ({connection.get('source_label')})"
                    topology_text += f" ↔ {dst_type} {connection.get('destination', 'Unknown')}"
                    if connection.get('destination_label'):
                        topology_text += f" ({connection.get('destination_label')})"
                    topology_text += "\n"
            else:
                topology_text += "   No connections found\n"

            return [TextContent(
                type="text",
                text=topology_text
            )]

        except Exception as e:
            logger.error(f"Failed to get lab topology: {e}")
            return [TextContent(
                type="text",
                text=f"Failed to get lab topology: {str(e)}"
            )]
