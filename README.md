# EVE-NG MCP Server

A comprehensive Model Context Protocol (MCP) server for EVE-NG network emulation platform integration. This server exposes EVE-NG's full API capabilities through MCP's standardized interface, enabling LLMs to manage network topologies, labs, nodes, and configurations.

## Features

### 🔌 Connection Management
- Secure authentication with EVE-NG servers
- Connection testing and health monitoring
- Session management with automatic reconnection
- Support for both HTTP and HTTPS protocols

### 🧪 Lab Management
- Create, list, and delete labs
- Comprehensive lab information retrieval
- Lab metadata management (description, author, version)
- Import/export capabilities (planned)

### 🖥️ Node Management
- Add and configure nodes with various templates
- Start, stop, and manage node lifecycle
- Bulk operations for multiple nodes
- Node configuration and status monitoring
- Comprehensive template and image support

### 🌐 Network Management
- Create and manage networks (clouds, bridges, NAT)
- Connect nodes to networks and each other
- Topology visualization and management
- Network configuration and monitoring

### 📊 MCP Resources & Prompts (Planned)
- Dynamic resources for real-time lab status
- Static resources for documentation and examples
- Guided prompts for common workflows
- Educational content generation

## Installation

### Prerequisites
- Python 3.11 or higher
- UV package manager
- Access to an EVE-NG server

### Using UV (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd eveng-mcp-server

# Install dependencies
uv sync

# Copy example configuration
cp .env.example .env

# Edit configuration as needed
nano .env
```

## Configuration

The server can be configured using environment variables or a `.env` file:

```bash
# EVE-NG Server Settings
EVENG_HOST=eve.local
EVENG_PORT=80
EVENG_PROTOCOL=http
EVENG_USERNAME=admin
EVENG_PASSWORD=eve

# MCP Server Settings
MCP_TRANSPORT=stdio
MCP_LOG_LEVEL=INFO
```

See `.env.example` for all available configuration options.

## Usage

### Command Line Interface

```bash
# Run with stdio transport (default)
uv run eveng-mcp-server run

# Run with SSE transport
uv run eveng-mcp-server run --transport sse --host localhost --port 8000

# Test EVE-NG connection
uv run eveng-mcp-server test-connection --host eve.local --username admin --password eve

# Show configuration
uv run eveng-mcp-server config-info

# Show version
uv run eveng-mcp-server version
```

## Available MCP Tools

### Connection Management
- `connect_eveng_server` - Connect to EVE-NG server
- `disconnect_eveng_server` - Disconnect from server
- `test_connection` - Test server connectivity
- `get_server_info` - Get server information and status

### Lab Management
- `list_labs` - List available labs
- `create_lab` - Create a new lab
- `get_lab_details` - Get detailed lab information
- `delete_lab` - Delete a lab

### Node Management
- `list_node_templates` - List available node templates
- `add_node` - Add nodes to labs with comprehensive configuration
- `list_nodes` - List lab nodes with status and details
- `get_node_details` - Get detailed node information
- `start_node` / `stop_node` - Control individual node power state
- `start_all_nodes` / `stop_all_nodes` - Bulk node operations
- `wipe_node` / `wipe_all_nodes` - Reset nodes to factory state
- `delete_node` - Remove nodes from labs

### Network Management
- `list_network_types` - List available network types
- `list_lab_networks` - List all networks in a lab
- `create_lab_network` - Create networks with positioning
- `delete_lab_network` - Remove networks from labs
- `connect_node_to_network` - Connect nodes to networks
- `connect_node_to_node` - Create point-to-point connections
- `get_lab_topology` - Retrieve complete topology information

## Testing

```bash
# Test EVE-NG connection
uv run eveng-mcp-server test-connection

# Run the server
uv run eveng-mcp-server run
```

## Development Status

- ✅ Basic MCP server framework
- ✅ EVE-NG connection management
- ✅ Lab management tools
- ✅ Node management tools
- ✅ Network management tools
- 📋 MCP resources implementation (planned)
- 📋 MCP prompts for guided workflows (planned)