#!/usr/bin/env python3
"""
Test client for EVE-NG MCP Server
Tests connection management and basic functionality
"""

import asyncio
import json
import httpx
from typing import Dict, Any

class MCPTestClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
        
    async def initialize_session(self):
        """Initialize MCP session"""
        async with httpx.AsyncClient() as client:
            # Connect to SSE endpoint
            response = await client.get(f"{self.base_url}/sse")
            print(f"SSE Connection: {response.status_code}")
            
            # Send initialize message
            init_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = await client.post(
                f"{self.base_url}/messages/",
                json=init_message
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Initialized: {result}")
                return True
            else:
                print(f"❌ Initialization failed: {response.status_code}")
                return False
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Call an MCP tool"""
        async with httpx.AsyncClient() as client:
            message = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            response = await client.post(
                f"{self.base_url}/messages/",
                json=message
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Tool {tool_name} result: {result}")
                return result
            else:
                print(f"❌ Tool {tool_name} failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None

async def test_connection_management():
    """Test Case 1: Connection Management"""
    print("🧪 Starting Test Case 1: Connection Management")
    
    client = MCPTestClient()
    
    # Step 1: Initialize session
    print("\n📡 Step 1: Initialize MCP session")
    if not await client.initialize_session():
        print("❌ Failed to initialize session")
        return False
    
    # Step 2: Connect to EVE-NG server
    print("\n🔗 Step 2: Connect to EVE-NG server")
    connect_result = await client.call_tool("connect_eveng_server", {
        "host": "eve.local",
        "username": "admin", 
        "password": "eve",
        "port": 80,
        "protocol": "http"
    })
    
    if not connect_result:
        print("❌ Failed to connect to EVE-NG server")
        return False
    
    # Step 3: Test connection
    print("\n🔍 Step 3: Test connection status")
    test_result = await client.call_tool("test_connection", {})
    
    if not test_result:
        print("❌ Failed to test connection")
        return False
    
    # Step 4: Get server info
    print("\n📊 Step 4: Get server information")
    info_result = await client.call_tool("get_server_info", {})
    
    if not info_result:
        print("❌ Failed to get server info")
        return False
    
    # Step 5: Disconnect
    print("\n🔌 Step 5: Disconnect from server")
    disconnect_result = await client.call_tool("disconnect_eveng_server", {})
    
    if not disconnect_result:
        print("❌ Failed to disconnect")
        return False
    
    print("\n✅ Test Case 1: Connection Management - PASSED")
    return True

if __name__ == "__main__":
    asyncio.run(test_connection_management())
