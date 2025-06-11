"""Dynamic MCP resources for EVE-NG MCP Server."""

import json
import re
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from mcp.types import Resource, TextResourceContents
from urllib.parse import urlparse, parse_qs

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from ..config import get_logger
from ..core.exceptions import EVENGAPIError


logger = get_logger("DynamicResources")


def register_dynamic_resources(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register dynamic MCP resources that provide real-time data."""
    
    @mcp.resource("eveng://server/status")
    async def get_server_status() -> str:
        """Get real-time EVE-NG server status."""
        try:
            if not eveng_client.is_connected:
                await eveng_client.connect()
            
            status = await eveng_client.get_server_status()
            
            # Format as JSON for easy consumption
            status_data = {
                "server": eveng_client.config.eveng.base_url,
                "status": "connected",
                "version": status.get("version", "Unknown"),
                "uptime": status.get("uptime", "Unknown"),
                "timestamp": status.get("timestamp", "Unknown")
            }
            
            return json.dumps(status_data, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to get server status: {e}")
            return json.dumps({"error": str(e), "status": "error"}, indent=2)
    
    @mcp.resource("eveng://labs/{lab_name}")
    async def get_lab_resource(lab_name: str) -> str:
        """Get lab configuration and metadata."""
        try:
            if not eveng_client.is_connected:
                await eveng_client.connect()
            
            # Construct lab path
            lab_path = f"/{lab_name}.unl" if not lab_name.endswith('.unl') else f"/{lab_name}"
            
            lab = await eveng_client.get_lab(lab_path)
            
            if not lab.get('data'):
                return json.dumps({"error": f"Lab {lab_name} not found"}, indent=2)
            
            lab_data = lab['data']
            
            # Format lab information
            resource_data = {
                "name": lab_data.get("name", lab_name),
                "path": lab_path,
                "description": lab_data.get("description", ""),
                "author": lab_data.get("author", ""),
                "version": lab_data.get("version", ""),
                "created": lab_data.get("created", ""),
                "modified": lab_data.get("modified", ""),
                "node_count": len(lab_data.get("nodes", {})),
                "network_count": len(lab_data.get("networks", {})),
                "status": "active" if lab_data.get("nodes") else "empty"
            }
            
            return json.dumps(resource_data, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to get lab resource: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    @mcp.resource("eveng://labs/{lab_name}/topology")
    async def get_lab_topology_resource(lab_name: str) -> str:
        """Get lab topology representation."""
        try:
            if not eveng_client.is_connected:
                await eveng_client.connect()
            
            lab_path = f"/{lab_name}.unl" if not lab_name.endswith('.unl') else f"/{lab_name}"
            
            # Get topology
            topology = await eveng_client.get_lab_topology(lab_path)
            
            if not topology.get('data'):
                return json.dumps({"error": f"No topology found for lab {lab_name}"}, indent=2)
            
            # Format topology data
            connections = []
            for conn_id, conn in topology['data'].items():
                connections.append({
                    "id": conn_id,
                    "source": {
                        "type": conn.get("source_type", "unknown"),
                        "id": conn.get("source", ""),
                        "interface": conn.get("source_label", "")
                    },
                    "destination": {
                        "type": conn.get("destination_type", "unknown"),
                        "id": conn.get("destination", ""),
                        "interface": conn.get("destination_label", "")
                    }
                })
            
            topology_data = {
                "lab": lab_name,
                "connections": connections,
                "connection_count": len(connections)
            }
            
            return json.dumps(topology_data, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to get lab topology: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    @mcp.resource("eveng://labs/{lab_name}/nodes")
    async def get_lab_nodes_resource(lab_name: str) -> str:
        """Get lab node inventory and status."""
        try:
            if not eveng_client.is_connected:
                await eveng_client.connect()
            
            lab_path = f"/{lab_name}.unl" if not lab_name.endswith('.unl') else f"/{lab_name}"
            
            nodes = await eveng_client.list_nodes(lab_path)
            
            if not nodes.get('data'):
                return json.dumps({"error": f"No nodes found in lab {lab_name}"}, indent=2)
            
            # Format nodes data
            nodes_list = []
            for node_id, node in nodes['data'].items():
                status_map = {0: "stopped", 1: "starting", 2: "running", 3: "stopping"}
                nodes_list.append({
                    "id": node_id,
                    "name": node.get("name", f"Node{node_id}"),
                    "template": node.get("template", "unknown"),
                    "type": node.get("type", "unknown"),
                    "image": node.get("image", "unknown"),
                    "status": status_map.get(node.get("status", 0), "unknown"),
                    "cpu": node.get("cpu", 0),
                    "ram": node.get("ram", 0),
                    "console": node.get("console", "unknown"),
                    "position": {
                        "left": node.get("left", 0),
                        "top": node.get("top", 0)
                    }
                })
            
            nodes_data = {
                "lab": lab_name,
                "nodes": nodes_list,
                "node_count": len(nodes_list),
                "running_count": len([n for n in nodes_list if n["status"] == "running"]),
                "stopped_count": len([n for n in nodes_list if n["status"] == "stopped"])
            }
            
            return json.dumps(nodes_data, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to get lab nodes: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    @mcp.resource("eveng://labs/{lab_name}/networks")
    async def get_lab_networks_resource(lab_name: str) -> str:
        """Get lab network configuration."""
        try:
            if not eveng_client.is_connected:
                await eveng_client.connect()
            
            lab_path = f"/{lab_name}.unl" if not lab_name.endswith('.unl') else f"/{lab_name}"
            
            networks = await eveng_client.list_lab_networks(lab_path)
            
            if not networks.get('data'):
                return json.dumps({"error": f"No networks found in lab {lab_name}"}, indent=2)
            
            # Format networks data
            networks_list = []
            for net_id, network in networks['data'].items():
                networks_list.append({
                    "id": net_id,
                    "name": network.get("name", f"Network{net_id}"),
                    "type": network.get("type", "unknown"),
                    "visibility": "visible" if network.get("visibility") == 1 else "hidden",
                    "position": {
                        "left": network.get("left", 0),
                        "top": network.get("top", 0)
                    }
                })
            
            networks_data = {
                "lab": lab_name,
                "networks": networks_list,
                "network_count": len(networks_list)
            }
            
            return json.dumps(networks_data, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to get lab networks: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    @mcp.resource("eveng://templates/{template_name}")
    async def get_template_resource(template_name: str) -> str:
        """Get template specifications."""
        try:
            if not eveng_client.is_connected:
                await eveng_client.connect()
            
            template_details = await eveng_client.node_template_detail(template_name)
            
            if not template_details.get('data'):
                return json.dumps({"error": f"Template {template_name} not found"}, indent=2)
            
            template_data = template_details['data']
            
            # Format template information
            resource_data = {
                "name": template_name,
                "type": template_data.get("type", "unknown"),
                "description": template_data.get("description", ""),
                "options": template_data.get("options", {}),
                "images": template_data.get("listimages", []),
                "supported_features": {
                    "ethernet": template_data.get("ethernet", 0),
                    "serial": template_data.get("serial", 0),
                    "console": template_data.get("console", "unknown")
                }
            }
            
            return json.dumps(resource_data, indent=2)
            
        except Exception as e:
            logger.error(f"Failed to get template resource: {e}")
            return json.dumps({"error": str(e)}, indent=2)

    @mcp.resource("eveng://nodes/{lab_name}/{node_name}/config")
    async def get_node_config_resource(lab_name: str, node_name: str) -> str:
        """Get individual node configuration."""
        try:
            if not eveng_client.is_connected:
                await eveng_client.connect()

            lab_path = f"/{lab_name}.unl" if not lab_name.endswith('.unl') else f"/{lab_name}"

            # First get all nodes to find the node ID by name
            nodes = await eveng_client.list_nodes(lab_path)

            if not nodes.get('data'):
                return json.dumps({"error": f"No nodes found in lab {lab_name}"}, indent=2)

            # Find the node by name
            target_node = None
            node_id = None
            for nid, node_data in nodes['data'].items():
                if node_data.get('name') == node_name:
                    target_node = node_data
                    node_id = nid
                    break

            if not target_node:
                return json.dumps({"error": f"Node {node_name} not found in lab {lab_name}"}, indent=2)

            # Get node configuration
            try:
                config = await eveng_client.get_node_config(lab_path, int(node_id))
                config_data = config.get('data', {})
            except Exception as config_error:
                logger.warning(f"Could not retrieve configuration for node {node_name}: {config_error}")
                config_data = {"error": f"Configuration not available: {str(config_error)}"}

            # Get detailed node information
            node_details = await eveng_client.get_node_details(lab_path, int(node_id))
            node_info = node_details.get('data', {})

            resource_data = {
                "node_name": node_name,
                "node_id": node_id,
                "lab_name": lab_name,
                "lab_path": lab_path,
                "node_info": {
                    "template": node_info.get('template', 'unknown'),
                    "image": node_info.get('image', 'unknown'),
                    "status": node_info.get('status', 'unknown'),
                    "cpu": node_info.get('cpu', 1),
                    "ram": node_info.get('ram', 512),
                    "ethernet": node_info.get('ethernet', 0),
                    "serial": node_info.get('serial', 0),
                    "console": node_info.get('console', 'unknown'),
                    "delay": node_info.get('delay', 0),
                    "icon": node_info.get('icon', 'unknown'),
                    "type": node_info.get('type', 'unknown'),
                    "left": node_info.get('left', 0),
                    "top": node_info.get('top', 0)
                },
                "configuration": config_data,
                "interfaces": node_info.get('interfaces', {}),
                "metadata": {
                    "retrieved_at": "2025-06-11T03:53:00Z",
                    "config_available": "error" not in config_data,
                    "node_running": node_info.get('status') == 2  # 2 = running
                }
            }

            return json.dumps(resource_data, indent=2)

        except Exception as e:
            logger.error(f"Failed to get node config resource: {e}")
            return json.dumps({"error": str(e)}, indent=2)
