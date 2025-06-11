# VS Code Integration Guide

Complete guide for integrating the EVE-NG MCP Server with Visual Studio Code for enhanced network development workflows.

## 🎯 Overview

VS Code integration with the EVE-NG MCP Server enables developers to:

- Manage EVE-NG labs directly from VS Code
- Generate network configurations with IntelliSense
- Debug network topologies within the IDE
- Automate lab deployment and testing
- Integrate with version control workflows
- Create network documentation and diagrams

## 📋 Prerequisites

### Required Software
- **VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)
- **EVE-NG MCP Server**: Installed and configured
- **Node.js**: For extension development (optional)
- **Python Extension**: For Python development support

### Recommended Extensions
- **Python** (ms-python.python)
- **YAML** (redhat.vscode-yaml)
- **JSON** (ms-vscode.json)
- **REST Client** (humao.rest-client)
- **Mermaid Preview** (bierner.markdown-mermaid)

## ⚙️ Configuration Methods

### Method 1: Workspace Settings

Create `.vscode/settings.json` in your workspace:

```json
{
  "eveng.mcp.server": {
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
      "EVENG_PASSWORD": "eve",
      "EVENG_PORT": "80",
      "EVENG_PROTOCOL": "http"
    }
  },
  "eveng.mcp.autoStart": true,
  "eveng.mcp.debug": false
}
```

### Method 2: Tasks Integration

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
        "panel": "new",
        "showReuseMessage": true,
        "clear": false
      },
      "problemMatcher": [],
      "runOptions": {
        "runOn": "folderOpen"
      },
      "isBackground": true
    },
    {
      "label": "Stop EVE-NG MCP Server",
      "type": "shell",
      "command": "pkill",
      "args": ["-f", "eveng-mcp-server"],
      "group": "build"
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
        "${config:eveng.host}",
        "--username",
        "${config:eveng.username}",
        "--password",
        "${config:eveng.password}"
      ],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": true,
        "panel": "new"
      }
    },
    {
      "label": "Deploy Lab Configuration",
      "type": "shell",
      "command": "python",
      "args": ["scripts/deploy_lab.py", "${file}"],
      "group": "build",
      "dependsOn": "Start EVE-NG MCP Server"
    }
  ]
}
```

### Method 3: Launch Configuration

Create `.vscode/launch.json` for debugging:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug EVE-NG MCP Server",
      "type": "python",
      "request": "launch",
      "module": "eveng_mcp_server.cli",
      "args": [
        "run",
        "--transport",
        "stdio",
        "--debug"
      ],
      "env": {
        "EVENG_HOST": "eve.local",
        "EVENG_USERNAME": "admin",
        "EVENG_PASSWORD": "eve",
        "LOG_LEVEL": "DEBUG"
      },
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Test Lab Deployment",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/test_lab.py",
      "args": ["${file}"],
      "env": {
        "EVENG_HOST": "eve.local",
        "EVENG_USERNAME": "admin",
        "EVENG_PASSWORD": "eve"
      },
      "console": "integratedTerminal"
    }
  ]
}
```

## 🔧 Custom Extension Development

### Extension Structure

Create a custom VS Code extension for EVE-NG:

```
eveng-vscode-extension/
├── package.json
├── src/
│   ├── extension.ts
│   ├── evengProvider.ts
│   ├── labManager.ts
│   └── commands/
│       ├── connectServer.ts
│       ├── createLab.ts
│       └── deployConfig.ts
├── resources/
│   ├── icons/
│   └── templates/
└── syntaxes/
    └── eveng-config.tmLanguage.json
```

### Package Configuration

**package.json**:
```json
{
  "name": "eveng-mcp-integration",
  "displayName": "EVE-NG MCP Integration",
  "description": "Integrate EVE-NG network emulation with VS Code",
  "version": "1.0.0",
  "publisher": "your-publisher",
  "engines": {
    "vscode": "^1.74.0"
  },
  "categories": ["Other", "Debuggers", "Snippets"],
  "keywords": ["eveng", "network", "emulation", "mcp", "cisco"],
  "activationEvents": [
    "onCommand:eveng.connectServer",
    "onLanguage:eveng-config",
    "workspaceContains:**/*.eveng"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "eveng.connectServer",
        "title": "Connect to EVE-NG Server",
        "category": "EVE-NG",
        "icon": "$(plug)"
      },
      {
        "command": "eveng.disconnectServer",
        "title": "Disconnect from EVE-NG Server",
        "category": "EVE-NG",
        "icon": "$(debug-disconnect)"
      },
      {
        "command": "eveng.listLabs",
        "title": "List Labs",
        "category": "EVE-NG",
        "icon": "$(list-unordered)"
      },
      {
        "command": "eveng.createLab",
        "title": "Create New Lab",
        "category": "EVE-NG",
        "icon": "$(add)"
      },
      {
        "command": "eveng.deployLab",
        "title": "Deploy Lab Configuration",
        "category": "EVE-NG",
        "icon": "$(rocket)"
      }
    ],
    "menus": {
      "explorer/context": [
        {
          "command": "eveng.deployLab",
          "when": "resourceExtname == .eveng",
          "group": "eveng"
        }
      ],
      "editor/context": [
        {
          "command": "eveng.deployLab",
          "when": "resourceExtname == .eveng",
          "group": "eveng"
        }
      ]
    },
    "views": {
      "explorer": [
        {
          "id": "evengLabs",
          "name": "EVE-NG Labs",
          "when": "eveng.connected"
        }
      ]
    },
    "viewsContainers": {
      "activitybar": [
        {
          "id": "eveng",
          "title": "EVE-NG",
          "icon": "$(circuit-board)"
        }
      ]
    },
    "configuration": {
      "title": "EVE-NG MCP",
      "properties": {
        "eveng.host": {
          "type": "string",
          "default": "eve.local",
          "description": "EVE-NG server hostname or IP address"
        },
        "eveng.port": {
          "type": "number",
          "default": 80,
          "description": "EVE-NG server port"
        },
        "eveng.protocol": {
          "type": "string",
          "enum": ["http", "https"],
          "default": "http",
          "description": "Protocol to use for EVE-NG connection"
        },
        "eveng.username": {
          "type": "string",
          "default": "admin",
          "description": "EVE-NG username"
        },
        "eveng.autoConnect": {
          "type": "boolean",
          "default": false,
          "description": "Automatically connect to EVE-NG on startup"
        },
        "eveng.mcp.serverPath": {
          "type": "string",
          "default": "eveng-mcp-server",
          "description": "Path to EVE-NG MCP server executable"
        }
      }
    },
    "languages": [
      {
        "id": "eveng-config",
        "aliases": ["EVE-NG Config", "eveng"],
        "extensions": [".eveng", ".unl"],
        "configuration": "./language-configuration.json"
      }
    ],
    "grammars": [
      {
        "language": "eveng-config",
        "scopeName": "source.eveng",
        "path": "./syntaxes/eveng-config.tmLanguage.json"
      }
    ],
    "snippets": [
      {
        "language": "eveng-config",
        "path": "./snippets/eveng.json"
      },
      {
        "language": "json",
        "path": "./snippets/eveng-json.json"
      }
    ]
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "devDependencies": {
    "@types/vscode": "^1.74.0",
    "@types/node": "16.x",
    "typescript": "^4.9.4"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "ws": "^8.14.0"
  }
}
```

### Main Extension Code

**src/extension.ts**:
```typescript
import * as vscode from 'vscode';
import { EVENGProvider } from './evengProvider';
import { LabManager } from './labManager';

export function activate(context: vscode.ExtensionContext) {
    console.log('EVE-NG MCP Extension is now active!');

    const evengProvider = new EVENGProvider();
    const labManager = new LabManager(evengProvider);

    // Register tree data provider
    vscode.window.registerTreeDataProvider('evengLabs', labManager);

    // Register commands
    const commands = [
        vscode.commands.registerCommand('eveng.connectServer', () => {
            return evengProvider.connect();
        }),
        
        vscode.commands.registerCommand('eveng.disconnectServer', () => {
            return evengProvider.disconnect();
        }),
        
        vscode.commands.registerCommand('eveng.listLabs', () => {
            return labManager.refresh();
        }),
        
        vscode.commands.registerCommand('eveng.createLab', async () => {
            const labName = await vscode.window.showInputBox({
                prompt: 'Enter lab name',
                placeHolder: 'my-network-lab'
            });
            
            if (labName) {
                const description = await vscode.window.showInputBox({
                    prompt: 'Enter lab description',
                    placeHolder: 'Network topology for testing'
                });
                
                return evengProvider.createLab(labName, description || '');
            }
        }),
        
        vscode.commands.registerCommand('eveng.deployLab', (uri: vscode.Uri) => {
            return deployLabConfiguration(uri, evengProvider);
        })
    ];

    context.subscriptions.push(...commands);

    // Auto-connect if configured
    const config = vscode.workspace.getConfiguration('eveng');
    if (config.get('autoConnect')) {
        evengProvider.connect();
    }
}

async function deployLabConfiguration(uri: vscode.Uri, provider: EVENGProvider) {
    try {
        const document = await vscode.workspace.openTextDocument(uri);
        const config = JSON.parse(document.getText());
        
        await provider.deployLab(config);
        
        vscode.window.showInformationMessage(
            `Lab '${config.name}' deployed successfully!`
        );
    } catch (error) {
        vscode.window.showErrorMessage(
            `Failed to deploy lab: ${error}`
        );
    }
}

export function deactivate() {}
```

## 📝 Code Snippets and Templates

### EVE-NG Configuration Snippets

Create `.vscode/eveng.code-snippets`:

```json
{
  "EVE-NG Lab Template": {
    "prefix": "eveng-lab",
    "body": [
      "{",
      "  \"name\": \"${1:lab-name}\",",
      "  \"description\": \"${2:Lab description}\",",
      "  \"author\": \"${3:$TM_FULLNAME}\",",
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
  "Cisco Router Node": {
    "prefix": "eveng-router",
    "body": [
      "\"${1:router-name}\": {",
      "  \"template\": \"vios\",",
      "  \"left\": ${2:25},",
      "  \"top\": ${3:25},",
      "  \"ram\": ${4:512},",
      "  \"ethernet\": ${5:4},",
      "  \"console\": \"telnet\",",
      "  \"delay\": ${6:0}",
      "}"
    ],
    "description": "Cisco router node configuration"
  },
  "Network Bridge": {
    "prefix": "eveng-network",
    "body": [
      "\"${1:network-name}\": {",
      "  \"type\": \"bridge\",",
      "  \"left\": ${2:50},",
      "  \"top\": ${3:100}",
      "}"
    ],
    "description": "Network bridge configuration"
  },
  "Lab Deployment Script": {
    "prefix": "eveng-deploy",
    "body": [
      "#!/usr/bin/env python3",
      "\"\"\"",
      "Deploy ${1:lab-name} to EVE-NG",
      "\"\"\"",
      "",
      "import asyncio",
      "from eveng_mcp_client import EVENGMCPClient",
      "",
      "async def deploy_lab():",
      "    client = EVENGMCPClient()",
      "    ",
      "    try:",
      "        await client.connect()",
      "        ",
      "        # Create lab",
      "        lab = await client.create_lab(",
      "            name=\"${1:lab-name}\",",
      "            description=\"${2:Lab description}\"",
      "        )",
      "        ",
      "        # Add nodes",
      "        $3",
      "        ",
      "        # Create networks",
      "        $4",
      "        ",
      "        print(f\"Lab '{lab['name']}' deployed successfully!\")",
      "        ",
      "    finally:",
      "        await client.disconnect()",
      "",
      "if __name__ == \"__main__\":",
      "    asyncio.run(deploy_lab())"
    ],
    "description": "Lab deployment script template"
  }
}
```

### Syntax Highlighting

Create `syntaxes/eveng-config.tmLanguage.json`:

```json
{
  "name": "EVE-NG Configuration",
  "scopeName": "source.eveng",
  "fileTypes": ["eveng", "unl"],
  "patterns": [
    {
      "include": "#lab-structure"
    },
    {
      "include": "#node-definition"
    },
    {
      "include": "#network-definition"
    }
  ],
  "repository": {
    "lab-structure": {
      "patterns": [
        {
          "name": "keyword.control.eveng",
          "match": "\\b(name|description|author|version|nodes|networks)\\b"
        }
      ]
    },
    "node-definition": {
      "patterns": [
        {
          "name": "entity.name.type.eveng",
          "match": "\\b(template|left|top|ram|ethernet|console|delay)\\b"
        },
        {
          "name": "string.quoted.double.eveng",
          "match": "\\b(vios|viosl2|linux|windows)\\b"
        }
      ]
    },
    "network-definition": {
      "patterns": [
        {
          "name": "entity.name.function.eveng",
          "match": "\\b(type|bridge|cloud|nat)\\b"
        }
      ]
    }
  }
}
```

## 🚀 Workflow Integration

### Git Integration

Create `.vscode/settings.json` for Git workflows:

```json
{
  "git.ignoreLimitWarning": true,
  "files.associations": {
    "*.eveng": "json",
    "*.unl": "xml"
  },
  "eveng.lab.autoSave": true,
  "eveng.lab.backupOnDeploy": true,
  "eveng.git.commitOnDeploy": false
}
```

### Automated Testing

Create test workflows in `.vscode/tasks.json`:

```json
{
  "label": "Test Lab Connectivity",
  "type": "shell",
  "command": "python",
  "args": [
    "scripts/test_connectivity.py",
    "--lab", "${input:labName}",
    "--timeout", "300"
  ],
  "group": "test",
  "presentation": {
    "echo": true,
    "reveal": "always",
    "focus": true,
    "panel": "new"
  },
  "dependsOn": "Deploy Lab Configuration"
}
```

### Documentation Generation

Integrate with Mermaid for topology diagrams:

```json
{
  "label": "Generate Topology Diagram",
  "type": "shell",
  "command": "python",
  "args": [
    "scripts/generate_diagram.py",
    "--lab", "${file}",
    "--output", "${fileDirname}/${fileBasenameNoExtension}.mmd"
  ],
  "group": "build"
}
```

## 🔧 Debugging and Development

### Debug Configuration

Use VS Code's debugging features:

```json
{
  "name": "Debug Lab Deployment",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/scripts/deploy_lab.py",
  "args": ["${file}"],
  "env": {
    "EVENG_HOST": "eve.local",
    "EVENG_USERNAME": "admin",
    "EVENG_PASSWORD": "eve",
    "LOG_LEVEL": "DEBUG"
  },
  "console": "integratedTerminal",
  "stopOnEntry": false,
  "breakpoints": [
    {
      "line": 25,
      "condition": "node_count > 5"
    }
  ]
}
```

### Live Development

Use VS Code's live development features:

1. **File Watchers**: Auto-deploy on file changes
2. **Integrated Terminal**: Run MCP commands directly
3. **Problem Matchers**: Parse EVE-NG errors
4. **IntelliSense**: Code completion for configurations

## 📊 Monitoring and Logging

### Output Channels

Create custom output channels for EVE-NG operations:

```typescript
const outputChannel = vscode.window.createOutputChannel('EVE-NG MCP');

outputChannel.appendLine('Connecting to EVE-NG server...');
outputChannel.show();
```

### Status Bar Integration

Show connection status in VS Code status bar:

```typescript
const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    100
);

statusBarItem.text = '$(plug) EVE-NG: Connected';
statusBarItem.color = '#00ff00';
statusBarItem.show();
```

## 🎯 Best Practices

### Project Structure

Organize your EVE-NG projects:

```
network-project/
├── .vscode/
│   ├── settings.json
│   ├── tasks.json
│   └── launch.json
├── labs/
│   ├── production.eveng
│   ├── testing.eveng
│   └── development.eveng
├── configs/
│   ├── routers/
│   ├── switches/
│   └── templates/
├── scripts/
│   ├── deploy_lab.py
│   ├── test_connectivity.py
│   └── backup_configs.py
└── docs/
    ├── topology.md
    └── diagrams/
```

### Version Control

Use Git effectively with EVE-NG:

```gitignore
# EVE-NG specific
*.tmp
*.backup
logs/
temp/

# VS Code
.vscode/settings.json
.vscode/launch.json

# Credentials
.env
secrets.json
```

## 🚀 Next Steps

1. **Install Extensions**: Set up recommended VS Code extensions
2. **Configure Workspace**: Create project-specific settings
3. **Develop Workflows**: Build custom tasks and launch configurations
4. **Create Templates**: Develop reusable lab templates
5. **Automate Testing**: Implement continuous integration for lab testing

For more integration examples, see our [Examples Repository](../examples/) and [Community Contributions](../community/).
