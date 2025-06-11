#!/bin/bash

# EVE-NG MCP Server Test Suite
# Using MCP Inspector CLI mode for comprehensive testing

echo "🧪 EVE-NG MCP Server - Comprehensive Test Suite"
echo "================================================"

# Test Case 1: List Tools
echo ""
echo "📋 Test Case 1: List Available Tools"
echo "------------------------------------"
npx @modelcontextprotocol/inspector --cli uv run eveng-mcp-server run --transport stdio --method tools/list

# Test Case 2: List Resources  
echo ""
echo "📊 Test Case 2: List Available Resources"
echo "----------------------------------------"
npx @modelcontextprotocol/inspector --cli uv run eveng-mcp-server run --transport stdio --method resources/list

# Test Case 3: List Prompts
echo ""
echo "🎯 Test Case 3: List Available Prompts"
echo "--------------------------------------"
npx @modelcontextprotocol/inspector --cli uv run eveng-mcp-server run --transport stdio --method prompts/list

echo ""
echo "✅ Basic MCP Server Tests Complete"
echo "=================================="
echo ""
echo "Next Steps:"
echo "1. Verify all tools, resources, and prompts are listed correctly"
echo "2. Use the web interface at http://eve.local/ to verify EVE-NG server is accessible"
echo "3. Run individual tool tests using the test-connection command"
echo ""
echo "To test connection manually:"
echo "uv run eveng-mcp-server test-connection --host eve.local --username admin --password eve"
