"""Static MCP resources for EVE-NG MCP Server."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from ..config import get_logger


logger = get_logger("StaticResources")


def register_static_resources(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register static MCP resources that provide documentation and examples."""
    
    @mcp.resource("eveng://help/api-reference")
    async def get_api_reference() -> str:
        """Get EVE-NG MCP Server API reference documentation."""
        return """# EVE-NG MCP Server API Reference

## Connection Management Tools

### connect_eveng_server
Connect to EVE-NG server with custom credentials.
**Parameters:**
- host: EVE-NG server hostname or IP
- username: Authentication username
- password: Authentication password
- port: Server port (default: 80)
- protocol: http/https (default: http)

### disconnect_eveng_server
Disconnect from EVE-NG server and cleanup sessions.

### test_connection
Test connectivity to EVE-NG server and return status.

### get_server_info
Retrieve server information including version and status.

## Lab Management Tools

### list_labs
List available labs in specified path.
**Parameters:**
- path: Path to list labs from (default: /)

### create_lab
Create a new lab with metadata.
**Parameters:**
- name: Lab name (required)
- path: Creation path (default: /)
- description: Lab description
- author: Lab author
- version: Lab version

### get_lab_details
Get comprehensive lab information including nodes and networks.
**Parameters:**
- lab_path: Full path to lab file

### delete_lab
Permanently delete a lab and all resources.
**Parameters:**
- lab_path: Full path to lab file

## Node Management Tools

### list_node_templates
List all available node templates with images and options.

### add_node
Add a node to a lab with comprehensive configuration.
**Parameters:**
- lab_path: Full path to lab file
- template: Node template name
- name: Node name (optional)
- node_type: Node type (qemu, iol, dynamips)
- left/top: Position coordinates (0-100%)
- ethernet/serial: Interface counts
- image: Specific image to use
- ram/cpu: Resource allocation

### list_nodes
List all nodes in a lab with status and configuration.
**Parameters:**
- lab_path: Full path to lab file

### get_node_details
Get detailed information about a specific node.
**Parameters:**
- lab_path: Full path to lab file
- node_id: Node ID

### start_node / stop_node
Control individual node power state.
**Parameters:**
- lab_path: Full path to lab file
- node_id: Node ID

### start_all_nodes / stop_all_nodes
Bulk operations for all nodes in a lab.
**Parameters:**
- lab_path: Full path to lab file

### wipe_node / wipe_all_nodes
Reset nodes to factory state (deletes all configuration).
**Parameters:**
- lab_path: Full path to lab file
- node_id: Node ID (for single node operation)

### delete_node
Remove a node from the lab permanently.
**Parameters:**
- lab_path: Full path to lab file
- node_id: Node ID

## Network Management Tools

### list_network_types
List all available network types (bridge, cloud, NAT, etc.).

### list_lab_networks
List all networks in a lab with details.
**Parameters:**
- lab_path: Full path to lab file

### create_lab_network
Create a new network in the lab.
**Parameters:**
- lab_path: Full path to lab file
- network_type: Network type (bridge, cloud, etc.)
- name: Network name (optional)
- left/top: Position coordinates (0-100%)

### delete_lab_network
Remove a network from the lab.
**Parameters:**
- lab_path: Full path to lab file
- network_id: Network ID

### connect_node_to_network
Connect a node interface to a network.
**Parameters:**
- lab_path: Full path to lab file
- node_id: Source node ID
- node_interface: Node interface name
- network_id: Target network ID

### connect_node_to_node
Create point-to-point connection between nodes.
**Parameters:**
- lab_path: Full path to lab file
- src_node_id: Source node ID
- src_interface: Source interface name
- dst_node_id: Destination node ID
- dst_interface: Destination interface name

### get_lab_topology
Retrieve complete topology with all connections.
**Parameters:**
- lab_path: Full path to lab file

## MCP Resources

### Dynamic Resources (Real-time data)
- eveng://server/status - Server status and information
- eveng://labs/{lab_name} - Lab metadata and configuration
- eveng://labs/{lab_name}/topology - Network topology
- eveng://labs/{lab_name}/nodes - Node inventory and status
- eveng://labs/{lab_name}/networks - Network configuration
- eveng://templates/{template_name} - Template specifications

### Static Resources (Documentation)
- eveng://help/api-reference - This API reference
- eveng://help/topology-examples - Sample topologies
- eveng://help/troubleshooting - Common issues and solutions

## Status Codes and Error Handling

All tools return structured responses with:
- Success messages with detailed information
- Error messages with specific failure reasons
- Status indicators (🟢 running, 🔴 stopped, ⚪ unknown)
- Rich formatting for better readability

## Best Practices

1. Always connect to EVE-NG server before using other tools
2. Use descriptive names for labs, nodes, and networks
3. Check node status before performing operations
4. Use bulk operations for efficiency when managing multiple nodes
5. Regularly check topology to understand lab connectivity
6. Use wipe operations carefully as they delete all configuration
"""
    
    @mcp.resource("eveng://help/topology-examples")
    async def get_topology_examples() -> str:
        """Get sample topology configurations and examples."""
        return """# EVE-NG Topology Examples

## Simple Router-Switch Topology

### Description
Basic topology with two routers connected through a switch.

### Components
- 2x Cisco IOSv routers
- 1x Cisco IOSvL2 switch
- 1x Management cloud

### Configuration Steps

1. **Create Lab**
```
create_lab:
  name: "simple-router-switch"
  description: "Basic router-switch topology"
  author: "Network Engineer"
```

2. **Add Routers**
```
add_node:
  template: "iosv"
  name: "R1"
  left: 20
  top: 30

add_node:
  template: "iosv"
  name: "R2"
  left: 80
  top: 30
```

3. **Add Switch**
```
add_node:
  template: "iosvl2"
  name: "SW1"
  left: 50
  top: 60
```

4. **Create Networks**
```
create_lab_network:
  network_type: "cloud"
  name: "Management"
  left: 50
  top: 10
```

5. **Connect Devices**
```
connect_node_to_node:
  src_node_id: "1"  # R1
  src_interface: "Gi0/0"
  dst_node_id: "3"  # SW1
  dst_interface: "Gi0/0"

connect_node_to_node:
  src_node_id: "2"  # R2
  src_interface: "Gi0/0"
  dst_node_id: "3"  # SW1
  dst_interface: "Gi0/1"
```

## Enterprise Campus Network

### Description
Multi-tier campus network with core, distribution, and access layers.

### Components
- 2x Core switches (L3)
- 4x Distribution switches (L3)
- 8x Access switches (L2)
- 2x Edge routers
- Management network

### Design Principles
- Redundant core layer
- HSRP/VRRP for gateway redundancy
- VLANs for network segmentation
- Trunk links between layers

## Data Center Topology

### Description
Leaf-spine data center architecture.

### Components
- 4x Spine switches
- 8x Leaf switches
- 16x Servers
- Management network

### Features
- ECMP routing
- BGP EVPN overlay
- VXLAN encapsulation
- Multi-tenancy support

## Service Provider Core

### Description
MPLS service provider core network.

### Components
- 6x PE routers
- 4x P routers
- 2x Route reflectors
- Customer sites

### Services
- L3VPN
- L2VPN
- Internet services
- MPLS TE

## Security Lab

### Description
Network security testing environment.

### Components
- Firewalls (ASA, Fortinet)
- IPS/IDS systems
- DMZ networks
- Internal/External zones

### Use Cases
- Penetration testing
- Security policy validation
- Incident response training
- Compliance testing

## Wireless Network

### Description
Enterprise wireless infrastructure.

### Components
- Wireless controllers
- Access points
- RADIUS servers
- Guest networks

### Features
- Multiple SSIDs
- 802.1X authentication
- Guest portal
- QoS policies

## Best Practices for Topology Design

1. **Naming Conventions**
   - Use descriptive names for devices
   - Include location/function in names
   - Consistent numbering scheme

2. **IP Addressing**
   - Plan IP address scheme
   - Use private address space
   - Document subnets

3. **Redundancy**
   - Implement redundant paths
   - Use spanning tree protocols
   - Configure backup links

4. **Scalability**
   - Design for growth
   - Use modular approach
   - Plan for future requirements

5. **Documentation**
   - Document all connections
   - Include configuration notes
   - Maintain topology diagrams
"""
    
    @mcp.resource("eveng://help/troubleshooting")
    async def get_troubleshooting_guide() -> str:
        """Get troubleshooting guide for common issues."""
        return """# EVE-NG MCP Server Troubleshooting Guide

## Connection Issues

### Problem: Cannot connect to EVE-NG server
**Symptoms:**
- Connection timeout errors
- Authentication failures
- Network unreachable errors

**Solutions:**
1. Verify server address and port
2. Check network connectivity: `ping eve.local`
3. Verify credentials (username/password)
4. Check firewall settings
5. Ensure EVE-NG service is running

**Commands:**
```bash
# Test connection
eveng-mcp-server test-connection --host eve.local --username admin --password eve

# Check configuration
eveng-mcp-server config-info
```

### Problem: SSL/TLS certificate errors
**Symptoms:**
- Certificate verification failures
- SSL handshake errors

**Solutions:**
1. Set `EVENG_SSL_VERIFY=false` for self-signed certificates
2. Add certificate to trust store
3. Use HTTP instead of HTTPS for testing

## Lab Management Issues

### Problem: Lab not found
**Symptoms:**
- "Lab not found" errors
- Empty lab lists

**Solutions:**
1. Check lab path format: `/lab_name.unl`
2. Verify lab exists in EVE-NG
3. Check user permissions
4. Ensure lab is not corrupted

### Problem: Cannot create lab
**Symptoms:**
- Lab creation failures
- Permission denied errors

**Solutions:**
1. Check disk space on EVE-NG server
2. Verify write permissions
3. Ensure unique lab name
4. Check path validity

## Node Management Issues

### Problem: Node won't start
**Symptoms:**
- Node stuck in "starting" state
- Start operation fails

**Solutions:**
1. Check available resources (CPU, RAM)
2. Verify image availability
3. Check node configuration
4. Review EVE-NG logs
5. Try wiping and reconfiguring node

**Commands:**
```bash
# Check node status
list_nodes --lab_path "/test_lab.unl"

# Get detailed node information
get_node_details --lab_path "/test_lab.unl" --node_id "1"

# Wipe node if needed
wipe_node --lab_path "/test_lab.unl" --node_id "1"
```

### Problem: Template not available
**Symptoms:**
- Template not found errors
- Missing images

**Solutions:**
1. Check available templates: `list_node_templates`
2. Verify image installation
3. Check template configuration
4. Update EVE-NG image library

### Problem: Console access issues
**Symptoms:**
- Cannot access node console
- Console connection failures

**Solutions:**
1. Verify node is running
2. Check console type (telnet/vnc)
3. Verify port availability
4. Check firewall rules

## Network Management Issues

### Problem: Cannot create networks
**Symptoms:**
- Network creation failures
- Invalid network type errors

**Solutions:**
1. Check available network types: `list_network_types`
2. Verify network name uniqueness
3. Check positioning parameters
4. Ensure lab is not locked

### Problem: Connection failures
**Symptoms:**
- Cannot connect nodes
- Interface not available errors

**Solutions:**
1. Verify node interfaces exist
2. Check interface naming convention
3. Ensure nodes are compatible
4. Verify network exists

**Commands:**
```bash
# List available networks
list_lab_networks --lab_path "/test_lab.unl"

# Check topology
get_lab_topology --lab_path "/test_lab.unl"
```

## Performance Issues

### Problem: Slow operations
**Symptoms:**
- Long response times
- Timeout errors

**Solutions:**
1. Check EVE-NG server resources
2. Reduce concurrent operations
3. Optimize lab size
4. Check network latency

### Problem: High resource usage
**Symptoms:**
- Server overload
- Memory exhaustion

**Solutions:**
1. Monitor running nodes
2. Stop unused nodes
3. Optimize node resources
4. Scale EVE-NG infrastructure

## API and MCP Issues

### Problem: Tool execution failures
**Symptoms:**
- MCP tool errors
- Invalid parameter errors

**Solutions:**
1. Check parameter format
2. Verify required fields
3. Review error messages
4. Check tool documentation

### Problem: Resource access failures
**Symptoms:**
- Resource not found
- Access denied errors

**Solutions:**
1. Verify resource URI format
2. Check authentication status
3. Ensure resource exists
4. Review permissions

## Logging and Debugging

### Enable Debug Logging
```bash
# Run with debug mode
eveng-mcp-server run --debug

# Set log level
export MCP_LOG_LEVEL=DEBUG
```

### Check Logs
- Review structured logs for error details
- Look for API call traces
- Check connection status messages
- Monitor resource usage

### Common Log Messages
- "Authentication failed" - Check credentials
- "Connection timeout" - Check network/firewall
- "Resource not found" - Verify paths and IDs
- "Permission denied" - Check user permissions

## Getting Help

1. **Check Documentation**
   - API reference: `eveng://help/api-reference`
   - Examples: `eveng://help/topology-examples`

2. **Test Basic Connectivity**
   ```bash
   eveng-mcp-server test-connection
   ```

3. **Review Configuration**
   ```bash
   eveng-mcp-server config-info
   ```

4. **Enable Verbose Logging**
   ```bash
   eveng-mcp-server run --debug
   ```

5. **Check EVE-NG Server**
   - Verify EVE-NG web interface access
   - Check server logs
   - Monitor resource usage

## Best Practices for Troubleshooting

1. **Start Simple**
   - Test basic connectivity first
   - Use minimal configurations
   - Isolate issues step by step

2. **Check Prerequisites**
   - Verify server requirements
   - Ensure proper installation
   - Check dependencies

3. **Use Systematic Approach**
   - Document error messages
   - Test one change at a time
   - Keep configuration backups

4. **Monitor Resources**
   - Check CPU and memory usage
   - Monitor disk space
   - Watch network utilization

5. **Keep Updated**
   - Use latest software versions
   - Apply security patches
   - Update documentation
"""
