#!/bin/bash

# EVE-NG MCP Server - Lab Integration Test
# This script tests lab creation and management via MCP tools

echo "🧪 EVE-NG MCP Server - Lab Integration Test"
echo "============================================"

# Test 1: List existing labs
echo ""
echo "📋 Step 1: List existing labs"
echo "-----------------------------"
echo "Command: uv run eveng-mcp-server list-labs --path /"
uv run eveng-mcp-server list-labs --path /

# Test 2: Create a test lab
echo ""
echo "🏗️ Step 2: Create test lab 'mcp_test_lab'"
echo "----------------------------------------"
echo "Command: uv run eveng-mcp-server create-lab --name mcp_test_lab --description 'Test lab created via MCP' --author 'MCP Testing'"
uv run eveng-mcp-server create-lab --name mcp_test_lab --description "Test lab created via MCP" --author "MCP Testing"

# Test 3: List labs again to confirm creation
echo ""
echo "📋 Step 3: List labs after creation"
echo "-----------------------------------"
echo "Command: uv run eveng-mcp-server list-labs --path /"
uv run eveng-mcp-server list-labs --path /

# Test 4: Get lab details
echo ""
echo "📊 Step 4: Get lab details"
echo "--------------------------"
echo "Command: uv run eveng-mcp-server get-lab-details --lab_path /mcp_test_lab.unl"
uv run eveng-mcp-server get-lab-details --lab_path /mcp_test_lab.unl

echo ""
echo "✅ Lab Integration Test Complete!"
echo "================================"
echo ""
echo "👀 Please check your EVE-NG UI at http://eve.local/"
echo "   You should see 'mcp_test_lab.unl' in the root folder"
echo ""
echo "Next: We'll test node management if lab creation was successful"
