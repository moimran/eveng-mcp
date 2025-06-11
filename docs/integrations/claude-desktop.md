# Claude Desktop Integration Guide

Complete guide for integrating the EVE-NG MCP Server with Claude Desktop for seamless network emulation management.

## 🎯 Overview

Claude Desktop provides native MCP (Model Context Protocol) support, allowing you to use EVE-NG functionality directly within your conversations with Claude. This integration enables you to:

- Create and manage EVE-NG labs through natural language
- Add and configure network nodes conversationally
- Monitor lab status and topology
- Troubleshoot network issues with Claude's assistance
- Generate network configurations and scripts

## 📋 Prerequisites

### Required Software
- **Claude Desktop**: Download from [claude.ai/download](https://claude.ai/download)
- **EVE-NG MCP Server**: Installed and configured
- **EVE-NG Server**: Accessible from your machine
- **Python 3.10+** and **UV package manager**

### Network Requirements
- Network connectivity to EVE-NG server
- Firewall rules allowing HTTP/HTTPS access to EVE-NG
- Valid EVE-NG user credentials

## ⚙️ Configuration

### Step 1: Locate Configuration File

Find your Claude Desktop configuration file:

**macOS**:
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**:
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux**:
```bash
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Basic Configuration

Add the EVE-NG MCP Server to your configuration:

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

### Step 3: Environment-Specific Configurations

#### Development Environment

```json
{
  "mcpServers": {
    "eveng-dev": {
      "command": "uv",
      "args": [
        "run",
        "eveng-mcp-server",
        "run",
        "--transport",
        "stdio",
        "--debug"
      ],
      "cwd": "/path/to/eveng-mcp-server",
      "env": {
        "EVENG_HOST": "eve-dev.local",
        "EVENG_USERNAME": "admin",
        "EVENG_PASSWORD": "eve",
        "LOG_LEVEL": "DEBUG",
        "EVENG_SSL_VERIFY": "false"
      }
    }
  }
}
```

#### Production Environment

```json
{
  "mcpServers": {
    "eveng-prod": {
      "command": "eveng-mcp-server",
      "args": [
        "run",
        "--transport",
        "stdio",
        "--config",
        "/etc/eveng-mcp/production.json"
      ],
      "env": {
        "EVENG_HOST": "eve-prod.company.com",
        "EVENG_USERNAME": "${EVENG_USERNAME}",
        "EVENG_PASSWORD": "${EVENG_PASSWORD}",
        "EVENG_PROTOCOL": "https",
        "EVENG_PORT": "443",
        "EVENG_SSL_VERIFY": "true"
      }
    }
  }
}
```

### Step 4: Multiple Server Configuration

Configure multiple EVE-NG servers:

```json
{
  "mcpServers": {
    "eveng-lab": {
      "command": "uv",
      "args": ["run", "eveng-mcp-server", "run", "--transport", "stdio"],
      "cwd": "/path/to/eveng-mcp-server",
      "env": {
        "EVENG_HOST": "eve-lab.local",
        "EVENG_USERNAME": "admin",
        "EVENG_PASSWORD": "eve"
      }
    },
    "eveng-production": {
      "command": "uv",
      "args": ["run", "eveng-mcp-server", "run", "--transport", "stdio"],
      "cwd": "/path/to/eveng-mcp-server",
      "env": {
        "EVENG_HOST": "eve-prod.company.com",
        "EVENG_USERNAME": "prod-user",
        "EVENG_PASSWORD": "secure-password",
        "EVENG_PROTOCOL": "https",
        "EVENG_PORT": "443"
      }
    }
  }
}
```

## 🚀 Usage Examples

### Basic Lab Management

#### Creating a Lab

**User**: "Create a new EVE-NG lab called 'enterprise-network' for testing our company's network design"

**Claude Response**: 
```
I'll create a new lab called 'enterprise-network' for you.

[Claude calls create_lab tool]

✅ Successfully created lab 'enterprise-network'!

The lab has been created with the following details:
- Name: enterprise-network
- Description: Testing company network design
- Author: Claude Assistant
- Version: 1.0
- Path: /enterprise-network.unl

You can now start adding nodes and configuring your network topology. Would you like me to add some routers or switches to get started?
```

#### Listing Labs

**User**: "Show me all my current EVE-NG labs"

**Claude Response**:
```
Let me check your current EVE-NG labs.

[Claude calls list_labs tool]

Here are your current labs:

📁 **Available Labs:**
1. **enterprise-network** - Testing company network design
2. **bgp-lab** - BGP routing protocols testing
3. **security-lab** - Security testing environment

Would you like me to get more details about any specific lab or help you manage them?
```

### Node Management

#### Adding Network Devices

**User**: "Add two Cisco routers and a switch to my enterprise-network lab"

**Claude Response**:
```
I'll add two Cisco routers and a switch to your enterprise-network lab.

[Claude calls add_node tool multiple times]

✅ Successfully added network devices:

**Routers:**
- Router-1 (Cisco vIOS) at position (50, 50)
  - RAM: 512MB, Ethernet ports: 4
- Router-2 (Cisco vIOS) at position (200, 50)
  - RAM: 512MB, Ethernet ports: 4

**Switch:**
- Switch-1 (Cisco vIOSL2) at position (125, 150)
  - RAM: 256MB, Ethernet ports: 16

Your lab now has 3 devices ready for configuration. Would you like me to create networks to connect them?
```

#### Starting Lab Devices

**User**: "Start all devices in the enterprise-network lab"

**Claude Response**:
```
I'll start all devices in your enterprise-network lab.

[Claude calls start_all_nodes tool]

✅ Starting all nodes in enterprise-network lab...

**Status Update:**
- Router-1: Starting... ✅ Running
- Router-2: Starting... ✅ Running  
- Switch-1: Starting... ✅ Running

All devices are now running and ready for configuration. The startup process typically takes 2-3 minutes for Cisco devices.
```

### Network Topology Management

#### Creating Networks

**User**: "Create a management network and connect all devices to it"

**Claude Response**:
```
I'll create a management network and connect all your devices to it.

[Claude calls create_lab_network and connect_node_to_network tools]

✅ Network topology configured:

**Created Networks:**
- Management-Network (Bridge) at position (125, 100)

**Device Connections:**
- Router-1 → Management-Network (eth0)
- Router-2 → Management-Network (eth0)
- Switch-1 → Management-Network (eth0)

Your management network is now set up! All devices can communicate on the 192.168.1.0/24 network (you'll need to configure IP addresses on each device).
```

#### Viewing Topology

**User**: "Show me the current topology of my enterprise-network lab"

**Claude Response**:
```
Let me get the current topology of your enterprise-network lab.

[Claude calls get_lab_topology tool]

📊 **Enterprise-Network Lab Topology:**

**Devices (3):**
```
┌─────────────┐    ┌─────────────┐
│  Router-1   │    │  Router-2   │
│ (Running)   │    │ (Running)   │
└──────┬──────┘    └──────┬──────┘
       │                  │
       └────────┬─────────┘
                │
        ┌───────▼────────┐
        │ Management-Net │
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │   Switch-1     │
        │  (Running)     │
        └────────────────┘
```

**Networks (1):**
- Management-Network: 3 connections

**Status:** All devices running, ready for configuration
```

### Advanced Operations

#### Lab Automation

**User**: "Create a script to automatically configure OSPF on all routers in my lab"

**Claude Response**:
```
I'll help you create an OSPF configuration script for your routers.

[Claude calls get_lab_details and list_nodes tools]

Based on your lab topology, here's an OSPF configuration script:

**OSPF Configuration Script:**

```bash
#!/bin/bash
# OSPF Configuration for Enterprise-Network Lab

# Router-1 Configuration
echo "Configuring Router-1..."
telnet 192.168.1.10 << EOF
enable
configure terminal
router ospf 1
network 192.168.1.0 0.0.0.255 area 0
network 10.1.1.0 0.0.0.255 area 0
exit
exit
write memory
EOF

# Router-2 Configuration  
echo "Configuring Router-2..."
telnet 192.168.1.11 << EOF
enable
configure terminal
router ospf 1
network 192.168.1.0 0.0.0.255 area 0
network 10.1.2.0 0.0.0.255 area 0
exit
exit
write memory
EOF

echo "OSPF configuration complete!"
```

This script configures OSPF area 0 on both routers. Make sure to:
1. Configure IP addresses on interfaces first
2. Adjust network statements for your specific subnets
3. Run this script from a machine that can reach your lab devices

Would you like me to help you configure the IP addresses first?
```

## 🎯 Best Practices

### Conversation Patterns

#### Effective Prompts

**Good**: "Create a lab with 3 routers running OSPF in area 0"
**Better**: "Create a lab called 'ospf-test' with 3 Cisco routers, configure them in a triangle topology with OSPF area 0, and add appropriate networks between them"

#### Context Building

Start conversations with context:
```
"I'm working on a network design for a small office with 50 users. I need to test VLAN segmentation and inter-VLAN routing. Can you help me create an EVE-NG lab for this?"
```

#### Iterative Development

Build labs incrementally:
1. "Create a basic lab with 2 routers"
2. "Add a switch between them"
3. "Create VLANs 10 and 20 on the switch"
4. "Configure inter-VLAN routing on Router-1"

### Security Considerations

#### Credential Management

**Don't**: Store passwords in plain text
```json
{
  "env": {
    "EVENG_PASSWORD": "admin123"
  }
}
```

**Do**: Use environment variables
```json
{
  "env": {
    "EVENG_PASSWORD": "${EVENG_PASSWORD}"
  }
}
```

#### Network Security

- Use HTTPS for production EVE-NG servers
- Implement proper firewall rules
- Use VPN for remote access
- Regular password rotation

## 🔧 Troubleshooting

### Common Issues

#### Server Not Detected

**Problem**: Claude doesn't show EVE-NG tools

**Check**:
1. Configuration file syntax (valid JSON)
2. File path and permissions
3. Command availability (`uv --version`)
4. Environment variables

**Solution**:
```bash
# Validate configuration
cat ~/.config/Claude/claude_desktop_config.json | jq '.'

# Test command manually
uv run eveng-mcp-server run --transport stdio
```

#### Connection Failures

**Problem**: "Failed to connect to EVE-NG server"

**Check**:
1. Network connectivity: `ping eve.local`
2. Service availability: `curl http://eve.local:80`
3. Credentials: Test in EVE-NG web interface
4. Firewall rules

#### Performance Issues

**Problem**: Slow responses or timeouts

**Solutions**:
1. Increase timeout values
2. Use local EVE-NG server
3. Optimize network connection
4. Check EVE-NG server resources

### Debug Mode

Enable detailed logging:

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

Check Claude Desktop logs:

**macOS**:
```bash
tail -f ~/Library/Logs/Claude/claude-desktop.log
```

**Windows**:
```bash
Get-Content "$env:LOCALAPPDATA\Claude\Logs\claude-desktop.log" -Wait
```

## 📚 Advanced Features

### Custom Prompts

Use the built-in prompts for guided workflows:

**User**: "Help me create an enterprise network topology"

**Claude**: Uses the `create_enterprise_topology` prompt to guide you through:
1. Network requirements gathering
2. Device selection and placement
3. Network segmentation design
4. Security considerations
5. Configuration templates

### Resource Integration

Access real-time information:

**User**: "What's the current status of my EVE-NG server?"

**Claude**: Uses the `eveng://server/status` resource to provide:
- Server version and health
- Resource utilization
- Active labs and nodes
- System performance metrics

## 🎉 Next Steps

1. **Start Simple**: Begin with basic lab creation and node management
2. **Build Complexity**: Gradually add more sophisticated network designs
3. **Automate**: Use Claude to generate configuration scripts and automation
4. **Integrate**: Combine with other tools and workflows
5. **Share**: Document your lab designs and share with the community

For more advanced integration patterns, see our [VS Code Integration Guide](vscode.md) and [Custom Client Examples](../examples/).
