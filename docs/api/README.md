# API Reference

The EVE-NG MCP Server provides a comprehensive set of tools, resources, and prompts for managing EVE-NG network emulation environments through the Model Context Protocol.

## Overview

- **25 Tools**: Complete EVE-NG management functionality
- **4 Resources**: Dynamic information and documentation
- **6 Prompts**: Guided workflows for common tasks

## Tools

### Connection Management (4 tools)

| Tool | Description | Required Args | Optional Args |
|------|-------------|---------------|---------------|
| `connect_eveng_server` | Connect and authenticate to EVE-NG server | `host`, `username`, `password` | `port`, `protocol` |
| `disconnect_eveng_server` | Disconnect from EVE-NG server | None | None |
| `test_connection` | Test server connectivity | None | None |
| `get_server_info` | Get server information and status | None | None |

### Lab Management (4 tools)

| Tool | Description | Required Args | Optional Args |
|------|-------------|---------------|---------------|
| `list_labs` | List available labs | None | `path` |
| `create_lab` | Create a new lab | `name` | `path`, `description`, `author`, `version` |
| `get_lab_details` | Get detailed lab information | `lab_path` | None |
| `delete_lab` | Delete a lab | `lab_path` | None |

### Node Management (11 tools)

| Tool | Description | Required Args | Optional Args |
|------|-------------|---------------|---------------|
| `list_node_templates` | List available node templates | None | None |
| `list_nodes` | List nodes in a lab | `lab_path` | None |
| `add_node` | Add a node to a lab | `lab_path`, `template` | `name`, `node_type`, `left`, `top`, `delay`, `console`, `config`, `ethernet`, `serial`, `image`, `ram`, `cpu` |
| `get_node_details` | Get detailed node information | `lab_path`, `node_id` | None |
| `start_node` | Start a specific node | `lab_path`, `node_id` | None |
| `stop_node` | Stop a specific node | `lab_path`, `node_id` | None |
| `start_all_nodes` | Start all nodes in a lab | `lab_path` | None |
| `stop_all_nodes` | Stop all nodes in a lab | `lab_path` | None |
| `wipe_node` | Reset node to factory state | `lab_path`, `node_id` | None |
| `wipe_all_nodes` | Reset all nodes in a lab | `lab_path` | None |
| `delete_node` | Delete a node from a lab | `lab_path`, `node_id` | None |

### Network Management (6 tools)

| Tool | Description | Required Args | Optional Args |
|------|-------------|---------------|---------------|
| `list_network_types` | List available network types | `lab_path` | None |
| `list_lab_networks` | List networks in a lab | `lab_path` | None |
| `create_lab_network` | Create a network in a lab | `lab_path`, `network_type` | `name`, `left`, `top` |
| `delete_lab_network` | Delete a network from a lab | `lab_path`, `network_id` | None |
| `connect_node_to_network` | Connect node to network | `lab_path`, `node_id`, `node_interface`, `network_id` | None |
| `connect_node_to_node` | Connect two nodes directly | `lab_path`, `src_node_id`, `src_interface`, `dst_node_id`, `dst_interface` | None |
| `get_lab_topology` | Get complete lab topology | `lab_path` | None |

## Resources

### Dynamic Resources

| Resource | URI | Description | MIME Type |
|----------|-----|-------------|-----------|
| Server Status | `eveng://server/status` | Real-time EVE-NG server status | `text/plain` |
| API Reference | `eveng://help/api-reference` | Complete API documentation | `text/plain` |
| Topology Examples | `eveng://help/topology-examples` | Sample configurations | `text/plain` |
| Troubleshooting | `eveng://help/troubleshooting` | Common issues and solutions | `text/plain` |

## Prompts

### Guided Workflows

| Prompt | Description | Arguments |
|--------|-------------|-----------|
| `create_simple_lab` | Basic lab setup guide | `lab_name`, `lab_description` |
| `create_enterprise_topology` | Enterprise network template | `company_name`, `site_count` |
| `diagnose_connectivity` | Network troubleshooting workflow | `lab_name`, `source_node`, `target_node` |
| `configure_lab_automation` | Automation script generation | `lab_name`, `automation_type` |
| `analyze_lab_performance` | Performance optimization guidance | `lab_name` |
| `debug_node_issues` | Node-specific debugging workflow | `lab_name`, `node_name`, `issue_type` |

## Usage Examples

### Basic Connection

```json
{
  "method": "tools/call",
  "params": {
    "name": "connect_eveng_server",
    "arguments": {
      "host": "eve.local",
      "username": "admin",
      "password": "eve",
      "port": 80,
      "protocol": "http"
    }
  }
}
```

### Lab Creation

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_lab",
    "arguments": {
      "name": "my_network_lab",
      "description": "Test network topology",
      "author": "Network Engineer",
      "version": "1.0",
      "path": "/"
    }
  }
}
```

### Node Addition

```json
{
  "method": "tools/call",
  "params": {
    "name": "add_node",
    "arguments": {
      "lab_path": "/my_network_lab.unl",
      "template": "vios",
      "name": "Router-1",
      "left": 25,
      "top": 25,
      "ram": 512,
      "ethernet": 4
    }
  }
}
```

### Network Creation

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_lab_network",
    "arguments": {
      "lab_path": "/my_network_lab.unl",
      "network_type": "bridge",
      "name": "LAN-1",
      "left": 50,
      "top": 75
    }
  }
}
```

### Resource Access

```json
{
  "method": "resources/read",
  "params": {
    "uri": "eveng://server/status"
  }
}
```

### Prompt Usage

```json
{
  "method": "prompts/get",
  "params": {
    "name": "create_simple_lab",
    "arguments": {
      "lab_name": "test_lab",
      "lab_description": "Simple test environment"
    }
  }
}
```

## Error Handling

All tools return standardized error responses:

```json
{
  "error": {
    "code": "EVENG_CONNECTION_ERROR",
    "message": "Failed to connect to EVE-NG server",
    "details": {
      "host": "eve.local",
      "port": 80,
      "timeout": 30
    }
  }
}
```

Common error codes:
- `EVENG_CONNECTION_ERROR`: Connection issues
- `EVENG_AUTH_ERROR`: Authentication failures
- `EVENG_NOT_FOUND`: Resource not found
- `EVENG_INVALID_PARAMS`: Invalid parameters
- `EVENG_SERVER_ERROR`: Server-side errors

## Rate Limiting

The server implements rate limiting to protect the EVE-NG backend:
- Maximum 10 concurrent connections
- Request timeout: 30 seconds
- Session timeout: 1 hour

## Authentication

All tools require an active connection to EVE-NG. Use `connect_eveng_server` before calling other tools:

1. Connect: `connect_eveng_server`
2. Perform operations: Any other tool
3. Disconnect: `disconnect_eveng_server` (optional)

## Best Practices

1. **Connection Management**: Always test connection before operations
2. **Error Handling**: Check for errors in all responses
3. **Resource Cleanup**: Stop nodes before deleting labs
4. **Batch Operations**: Use bulk operations for multiple nodes
5. **Monitoring**: Use resources for real-time status monitoring

## Detailed Documentation

For detailed documentation of each tool, resource, and prompt, see:

- [Tools Documentation](tools/)
- [Resources Documentation](resources/)
- [Prompts Documentation](prompts/)
- [Examples](examples/)
- [Tutorials](tutorials/)
