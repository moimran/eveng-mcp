# Client Integrations

This guide covers how to integrate the EVE-NG MCP Server with various MCP-compatible clients, including Claude Desktop and VS Code.

## 📋 Table of Contents

- [Claude Desktop Integration](#claude-desktop-integration)
- [VS Code Integration](#vs-code-integration)
- [MCP Inspector Integration](#mcp-inspector-integration)
- [Custom Client Integration](#custom-client-integration)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start Guides

For detailed integration instructions, see our comprehensive guides:

- **[📖 Claude Desktop Integration Guide](claude-desktop.md)** - Complete setup and usage guide for Claude Desktop
- **[💻 VS Code Integration Guide](vscode.md)** - Full VS Code integration with tasks, debugging, and extensions
- **[📁 Example Configurations](../../examples/integrations/)** - Ready-to-use configuration files and scripts

## 🤖 Claude Desktop Integration

Claude Desktop provides native MCP support, making it easy to integrate with the EVE-NG MCP Server.

### Prerequisites

1. **Claude Desktop**: Download from [Claude.ai](https://claude.ai/download)
2. **EVE-NG MCP Server**: Installed and configured
3. **EVE-NG Server**: Accessible from your machine

### Configuration

#### Method 1: Direct Configuration

1. **Locate Claude Desktop Config**:
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json
   
   # Windows
   %APPDATA%\Claude\claude_desktop_config.json
   
   # Linux
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Add EVE-NG MCP Server Configuration**:
   ```json
   {
     "mcpServers": {
       "eveng-mcp-server": {
         "command": "uv",
         "args": [
           "run",
           "eveng-mcp-server",
           "run",
           "--transport",
           "stdio"
         ],
         "cwd": "/path/to/eveng-mcp-server",
         "env": {
           "EVENG_HOST": "eve.local",
           "EVENG_USERNAME": "admin",
           "EVENG_PASSWORD": "eve",
           "EVENG_PORT": "80",
           "EVENG_PROTOCOL": "http"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** to load the new configuration.

#### Method 2: Using Installed Package

If you've installed the EVE-NG MCP Server as a package:

```json
{
  "mcpServers": {
    "eveng-mcp-server": {
      "command": "eveng-mcp-server",
      "args": ["run", "--transport", "stdio"],
      "env": {
        "EVENG_HOST": "eve.local",
        "EVENG_USERNAME": "admin",
        "EVENG_PASSWORD": "eve"
      }
    }
  }
}
```

#### Method 3: Using Docker

```json
{
  "mcpServers": {
    "eveng-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env", "EVENG_HOST=eve.local",
        "--env", "EVENG_USERNAME=admin",
        "--env", "EVENG_PASSWORD=eve",
        "eveng-mcp-server:latest",
        "run",
        "--transport", "stdio"
      ]
    }
  }
}
```

### Usage in Claude Desktop

Once configured, you can use EVE-NG functionality directly in Claude Desktop:

#### Example Conversations

**Creating a Lab**:
```
User: Create a new EVE-NG lab called "test-network" with description "Testing network topology"

Claude: I'll create a new lab for you using the EVE-NG MCP server.

[Claude calls create_lab tool]

The lab "test-network" has been successfully created! You can now add nodes and configure your network topology.
```

**Adding Nodes**:
```
User: Add two Cisco routers to the test-network lab

Claude: I'll add two Cisco routers to your test-network lab.

[Claude calls add_node tool twice]

I've successfully added two Cisco vIOS routers to your lab:
- Router-1 at position (25, 25)
- Router-2 at position (100, 25)
```

**Getting Lab Status**:
```
User: Show me the current status of my EVE-NG labs

Claude: Let me check the status of your EVE-NG labs.

[Claude calls list_labs and get_lab_details tools]

Here are your current labs:
1. test-network: 2 nodes, 0 networks
2. production-lab: 5 nodes, 3 networks, all nodes running
```

### Advanced Configuration

#### Environment-Specific Configurations

**Development Environment**:
```json
{
  "mcpServers": {
    "eveng-dev": {
      "command": "uv",
      "args": ["run", "eveng-mcp-server", "run", "--transport", "stdio", "--debug"],
      "cwd": "/path/to/eveng-mcp-server",
      "env": {
        "EVENG_HOST": "eve-dev.local",
        "EVENG_USERNAME": "admin",
        "EVENG_PASSWORD": "eve",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

**Production Environment**:
```json
{
  "mcpServers": {
    "eveng-prod": {
      "command": "eveng-mcp-server",
      "args": ["run", "--transport", "stdio", "--config", "/etc/eveng-mcp/production.json"],
      "env": {
        "EVENG_HOST": "eve-prod.company.com",
        "EVENG_USERNAME": "${EVENG_USERNAME}",
        "EVENG_PASSWORD": "${EVENG_PASSWORD}",
        "EVENG_PROTOCOL": "https",
        "EVENG_PORT": "443"
      }
    }
  }
}
```

## 💻 VS Code Integration

VS Code can integrate with MCP servers through extensions and custom configurations.

### Method 1: MCP Extension

1. **Install MCP Extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Model Context Protocol" or "MCP"
   - Install the official MCP extension

2. **Configure MCP Server**:
   
   Create `.vscode/settings.json` in your workspace:
   ```json
   {
     "mcp.servers": {
       "eveng-mcp-server": {
         "command": "uv",
         "args": [
           "run",
           "eveng-mcp-server",
           "run",
           "--transport",
           "stdio"
         ],
         "cwd": "${workspaceFolder}",
         "env": {
           "EVENG_HOST": "eve.local",
           "EVENG_USERNAME": "admin",
           "EVENG_PASSWORD": "eve"
         }
       }
     }
   }
   ```

### Method 2: Task Integration

Create `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start EVE-NG MCP Server",
      "type": "shell",
      "command": "uv",
      "args": [
        "run",
        "eveng-mcp-server",
        "run",
        "--transport",
        "sse",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "new"
      },
      "problemMatcher": [],
      "runOptions": {
        "runOn": "folderOpen"
      }
    },
    {
      "label": "Test EVE-NG Connection",
      "type": "shell",
      "command": "uv",
      "args": [
        "run",
        "eveng-mcp-server",
        "test-connection",
        "--host",
        "eve.local",
        "--username",
        "admin",
        "--password",
        "eve"
      ],
      "group": "test"
    }
  ]
}
```

### Method 3: Custom Extension

Create a custom VS Code extension for EVE-NG integration:

**package.json**:
```json
{
  "name": "eveng-mcp-integration",
  "displayName": "EVE-NG MCP Integration",
  "description": "Integrate EVE-NG with VS Code via MCP",
  "version": "1.0.0",
  "engines": {
    "vscode": "^1.74.0"
  },
  "categories": ["Other"],
  "activationEvents": [
    "onCommand:eveng.connectServer",
    "onCommand:eveng.listLabs"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "eveng.connectServer",
        "title": "Connect to EVE-NG Server"
      },
      {
        "command": "eveng.listLabs",
        "title": "List EVE-NG Labs"
      },
      {
        "command": "eveng.createLab",
        "title": "Create New Lab"
      }
    ],
    "configuration": {
      "title": "EVE-NG MCP",
      "properties": {
        "eveng.host": {
          "type": "string",
          "default": "eve.local",
          "description": "EVE-NG server hostname"
        },
        "eveng.username": {
          "type": "string",
          "default": "admin",
          "description": "EVE-NG username"
        },
        "eveng.password": {
          "type": "string",
          "description": "EVE-NG password"
        }
      }
    }
  }
}
```

### VS Code Snippets

Create `.vscode/eveng.code-snippets`:
```json
{
  "EVE-NG Lab Configuration": {
    "prefix": "eveng-lab",
    "body": [
      "{",
      "  \"name\": \"${1:lab-name}\",",
      "  \"description\": \"${2:Lab description}\",",
      "  \"author\": \"${3:Your Name}\",",
      "  \"version\": \"${4:1.0}\",",
      "  \"nodes\": {",
      "    $5",
      "  },",
      "  \"networks\": {",
      "    $6",
      "  }",
      "}"
    ],
    "description": "EVE-NG lab configuration template"
  },
  "EVE-NG Node Configuration": {
    "prefix": "eveng-node",
    "body": [
      "\"${1:node-name}\": {",
      "  \"template\": \"${2:vios}\",",
      "  \"left\": ${3:25},",
      "  \"top\": ${4:25},",
      "  \"ram\": ${5:512},",
      "  \"ethernet\": ${6:4}",
      "}"
    ],
    "description": "EVE-NG node configuration"
  }
}
```

## 🔍 MCP Inspector Integration

The MCP Inspector provides a web-based interface for testing and debugging.

### Web Interface

1. **Start EVE-NG MCP Server in SSE mode**:
   ```bash
   uv run eveng-mcp-server run --transport sse --host 0.0.0.0 --port 8000
   ```

2. **Start MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. **Connect**: Open http://127.0.0.1:6274 and connect to `http://localhost:8000`

### CLI Interface

```bash
# List all tools
npx @modelcontextprotocol/inspector \
  --cli "uv run eveng-mcp-server run --transport stdio" \
  --method tools/list

# Test specific tool
npx @modelcontextprotocol/inspector \
  --cli "uv run eveng-mcp-server run --transport stdio" \
  --method tools/call \
  --params '{"name": "list_labs", "arguments": {"path": "/"}}'
```

## 🔧 Custom Client Integration

### Python Client Example

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def eveng_client_example():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "eveng-mcp-server", "run", "--transport", "stdio"],
        env={
            "EVENG_HOST": "eve.local",
            "EVENG_USERNAME": "admin",
            "EVENG_PASSWORD": "eve"
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # Connect to EVE-NG
            result = await session.call_tool("connect_eveng_server", {
                "host": "eve.local",
                "username": "admin",
                "password": "eve"
            })
            print(f"Connection result: {result}")
            
            # List labs
            labs = await session.call_tool("list_labs", {"path": "/"})
            print(f"Labs: {labs}")

if __name__ == "__main__":
    asyncio.run(eveng_client_example())
```

### JavaScript/Node.js Client

```javascript
const { spawn } = require('child_process');
const { MCPClient } = require('@modelcontextprotocol/client');

class EVENGMCPClient {
    constructor() {
        this.client = null;
        this.process = null;
    }
    
    async connect() {
        // Start MCP server process
        this.process = spawn('uv', [
            'run', 'eveng-mcp-server', 'run', '--transport', 'stdio'
        ], {
            env: {
                ...process.env,
                EVENG_HOST: 'eve.local',
                EVENG_USERNAME: 'admin',
                EVENG_PASSWORD: 'eve'
            }
        });
        
        // Create MCP client
        this.client = new MCPClient({
            read: this.process.stdout,
            write: this.process.stdin
        });
        
        await this.client.initialize();
    }
    
    async listLabs() {
        return await this.client.callTool('list_labs', { path: '/' });
    }
    
    async createLab(name, description) {
        return await this.client.callTool('create_lab', {
            name,
            description,
            author: 'Node.js Client',
            version: '1.0'
        });
    }
    
    async disconnect() {
        if (this.process) {
            this.process.kill();
        }
    }
}

// Usage
async function main() {
    const client = new EVENGMCPClient();
    
    try {
        await client.connect();
        
        const labs = await client.listLabs();
        console.log('Labs:', labs);
        
        const result = await client.createLab('test-lab', 'Test lab from Node.js');
        console.log('Created lab:', result);
        
    } finally {
        await client.disconnect();
    }
}

main().catch(console.error);
```

## 🔧 Troubleshooting

### Common Issues

#### Claude Desktop Not Detecting Server

**Problem**: Claude Desktop doesn't show EVE-NG tools

**Solutions**:
1. Check configuration file location and syntax
2. Verify command path and arguments
3. Check environment variables
4. Restart Claude Desktop
5. Check logs in Claude Desktop developer tools

#### VS Code Integration Issues

**Problem**: MCP extension not working

**Solutions**:
1. Verify extension installation
2. Check workspace settings
3. Ensure MCP server is accessible
4. Check VS Code output panel for errors

#### Connection Failures

**Problem**: Cannot connect to EVE-NG server

**Solutions**:
1. Test direct connection: `curl http://eve.local:80`
2. Verify credentials
3. Check network connectivity
4. Review environment variables

### Debug Mode

Enable debug logging for troubleshooting:

```json
{
  "mcpServers": {
    "eveng-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "eveng-mcp-server",
        "run",
        "--transport",
        "stdio",
        "--debug"
      ],
      "env": {
        "LOG_LEVEL": "DEBUG",
        "EVENG_HOST": "eve.local",
        "EVENG_USERNAME": "admin",
        "EVENG_PASSWORD": "eve"
      }
    }
  }
}
```

### Log Analysis

Check logs for integration issues:

```bash
# Claude Desktop logs (macOS)
tail -f ~/Library/Logs/Claude/claude-desktop.log

# VS Code logs
# Help > Toggle Developer Tools > Console

# EVE-NG MCP Server logs
tail -f logs/eveng-mcp-server.log
```

## 📚 Additional Resources

- [Claude Desktop Documentation](https://claude.ai/docs)
- [VS Code Extension Development](https://code.visualstudio.com/api)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [EVE-NG API Documentation](https://www.eve-ng.net/documentation/api)

## 🤝 Community Examples

Check our [examples repository](../examples/) for more integration examples and community contributions.
