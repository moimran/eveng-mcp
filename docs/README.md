# EVE-NG MCP Server

A comprehensive Model Context Protocol (MCP) server for EVE-NG network emulation platform, providing seamless integration and management capabilities through standardized MCP interfaces.

## 🚀 Features

- **Complete EVE-NG Integration**: Full API coverage for labs, nodes, networks, and topology management
- **25 Powerful Tools**: Comprehensive set of tools for all EVE-NG operations
- **4 Dynamic Resources**: Real-time server status and comprehensive documentation
- **6 Smart Prompts**: Guided workflows for common network emulation tasks
- **Multiple Transport Protocols**: stdio, SSE, and TCP bridge support
- **Production Ready**: Robust error handling, logging, and monitoring
- **Cross-Platform**: Windows, Linux, and macOS compatibility

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ⚡ Quick Start

### Prerequisites

- Python 3.10 or higher
- EVE-NG server (6.0.0 or higher)
- UV package manager (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/eveng-mcp-server.git
cd eveng-mcp-server

# Install dependencies
uv sync

# Test connection to EVE-NG
uv run eveng-mcp-server test-connection --host your-eve-server --username admin --password eve
```

### Basic Usage

```bash
# Start the MCP server (stdio mode)
uv run eveng-mcp-server run

# Start with SSE transport for web access
uv run eveng-mcp-server run --transport sse --host 0.0.0.0 --port 8000

# View configuration
uv run eveng-mcp-server config-info

# Show version
uv run eveng-mcp-server version
```

## 🔧 Installation

### System Requirements

- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 12+
- **Python**: 3.10 or higher
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Network**: Access to EVE-NG server on port 80/443

### Package Manager Installation

#### Using UV (Recommended)

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/your-org/eveng-mcp-server.git
cd eveng-mcp-server
uv sync
```

#### Using Pip

```bash
# Clone repository
git clone https://github.com/your-org/eveng-mcp-server.git
cd eveng-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Docker Installation

```bash
# Build Docker image
docker build -t eveng-mcp-server .

# Run container
docker run -p 8000:8000 eveng-mcp-server
```

### Development Installation

```bash
# Clone with development dependencies
git clone https://github.com/your-org/eveng-mcp-server.git
cd eveng-mcp-server

# Install with development dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# EVE-NG Server Configuration
EVENG_HOST=eve.local
EVENG_PORT=80
EVENG_PROTOCOL=http
EVENG_USERNAME=admin
EVENG_PASSWORD=eve
EVENG_SSL_VERIFY=false
EVENG_TIMEOUT=30
EVENG_MAX_RETRIES=3

# MCP Server Configuration
MCP_NAME=EVE-NG MCP Server
MCP_VERSION=1.0.0
MCP_TRANSPORT=stdio
MCP_HOST=localhost
MCP_PORT=8000
MCP_LOG_LEVEL=INFO
MCP_LOG_FORMAT=json

# Security Configuration
SECURITY_DISABLE_SSL_WARNINGS=true
SECURITY_MAX_CONCURRENT_CONNECTIONS=10
SECURITY_SESSION_TIMEOUT=3600

# Development Settings
DEBUG=false
TESTING=false
```

### Configuration File

Alternative JSON configuration (`config.json`):

```json
{
  "eveng": {
    "host": "eve.local",
    "port": 80,
    "protocol": "http",
    "username": "admin",
    "password": "eve",
    "ssl_verify": false,
    "timeout": 30,
    "max_retries": 3
  },
  "mcp": {
    "name": "EVE-NG MCP Server",
    "version": "1.0.0",
    "transport": "stdio",
    "host": "localhost",
    "port": 8000,
    "log_level": "INFO",
    "log_format": "json"
  },
  "security": {
    "disable_ssl_warnings": true,
    "max_concurrent_connections": 10,
    "session_timeout": 3600
  }
}
```

### CLI Configuration

```bash
# Set configuration via CLI
uv run eveng-mcp-server run --host eve.local --port 80 --transport sse

# Load custom configuration file
uv run eveng-mcp-server run --config /path/to/config.json

# Enable debug mode
uv run eveng-mcp-server run --debug
```

## 🎯 Usage

### Command Line Interface

#### Basic Commands

```bash
# Test EVE-NG connection
uv run eveng-mcp-server test-connection

# Show current configuration
uv run eveng-mcp-server config-info

# Display version information
uv run eveng-mcp-server version

# Run server with different transports
uv run eveng-mcp-server run --transport stdio
uv run eveng-mcp-server run --transport sse --host 0.0.0.0 --port 8000
```

#### Advanced Usage

```bash
# Custom EVE-NG server
uv run eveng-mcp-server test-connection \
  --host 192.168.1.100 \
  --username admin \
  --password mypassword \
  --port 443 \
  --protocol https

# Debug mode with custom config
uv run eveng-mcp-server run \
  --config /etc/eveng-mcp/config.json \
  --debug \
  --transport sse \
  --host 0.0.0.0 \
  --port 8080
```

### MCP Inspector Integration

#### Web Interface

1. Start the MCP server in SSE mode:
   ```bash
   uv run eveng-mcp-server run --transport sse --host 0.0.0.0 --port 8000
   ```

2. Open MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. Connect to: `http://localhost:8000`

#### CLI Testing

```bash
# List all available tools
npx @modelcontextprotocol/inspector \
  --cli "uv run eveng-mcp-server run --transport stdio" \
  --method tools/list

# List all resources
npx @modelcontextprotocol/inspector \
  --cli "uv run eveng-mcp-server run --transport stdio" \
  --method resources/list

# Call a specific tool
npx @modelcontextprotocol/inspector \
  --cli "uv run eveng-mcp-server run --transport stdio" \
  --method tools/call \
  --params '{"name": "list_labs", "arguments": {"path": "/"}}'
```

### Programmatic Usage

#### Python Client Example

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "eveng-mcp-server", "run", "--transport", "stdio"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # Call a tool
            result = await session.call_tool("list_labs", {"path": "/"})
            print(f"Labs: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📚 API Reference

### Tools (25 Available)

The EVE-NG MCP Server provides 25 comprehensive tools organized into four categories:

- **[Connection Management](api/tools/connection.md)** (4 tools)
- **[Lab Management](api/tools/labs.md)** (4 tools)  
- **[Node Management](api/tools/nodes.md)** (11 tools)
- **[Network Management](api/tools/networks.md)** (6 tools)

### Resources (4 Available)

- **[Server Status](api/resources/status.md)** - Real-time EVE-NG server information
- **[API Reference](api/resources/reference.md)** - Complete API documentation
- **[Topology Examples](api/resources/examples.md)** - Sample network configurations
- **[Troubleshooting Guide](api/resources/troubleshooting.md)** - Common issues and solutions

### Prompts (6 Available)

- **[Simple Lab Creation](api/prompts/simple-lab.md)** - Basic lab setup workflow
- **[Enterprise Topology](api/prompts/enterprise.md)** - Complex network design
- **[Connectivity Diagnosis](api/prompts/diagnosis.md)** - Network troubleshooting
- **[Lab Automation](api/prompts/automation.md)** - Automation script generation
- **[Performance Analysis](api/prompts/performance.md)** - Optimization guidance
- **[Node Debugging](api/prompts/debugging.md)** - Node-specific troubleshooting

## 🚀 Deployment

See the [Deployment Guide](deployment/README.md) for detailed production deployment instructions including:

- [Docker Deployment](deployment/docker.md)
- [Kubernetes Deployment](deployment/kubernetes.md)
- [Systemd Service](deployment/systemd.md)
- [Reverse Proxy Setup](deployment/proxy.md)
- [Monitoring and Logging](deployment/monitoring.md)
- [Security Configuration](deployment/security.md)

## 🧪 Testing

See the [Testing Guide](testing/README.md) for comprehensive testing procedures:

- [Unit Tests](testing/unit.md)
- [Integration Tests](testing/integration.md)
- [End-to-End Tests](testing/e2e.md)
- [Performance Tests](testing/performance.md)
- [MCP Inspector Testing](testing/inspector.md)

## 🔧 Troubleshooting

See the [Troubleshooting Guide](troubleshooting/README.md) for common issues and solutions:

- [Connection Issues](troubleshooting/connection.md)
- [Authentication Problems](troubleshooting/auth.md)
- [Performance Issues](troubleshooting/performance.md)
- [Configuration Errors](troubleshooting/config.md)
- [FAQ](troubleshooting/faq.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development Setup
- Coding Standards
- Pull Request Process
- Issue Reporting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [EVE-NG](https://www.eve-ng.net/) for the excellent network emulation platform
- [Model Context Protocol](https://modelcontextprotocol.io/) for the standardized interface
- [Anthropic](https://www.anthropic.com/) for MCP development and support

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/eveng-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/eveng-mcp-server/discussions)
- **Email**: support@your-org.com
