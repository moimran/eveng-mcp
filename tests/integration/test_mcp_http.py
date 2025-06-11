#!/usr/bin/env python3
"""
Test MCP server via HTTP requests
"""

import asyncio
import json
import httpx

async def test_mcp_lab_creation():
    """Test lab creation via MCP HTTP interface"""
    
    print("🧪 Testing MCP Server via HTTP")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Test 1: Initialize MCP session
            print("📡 Step 1: Initialize MCP session")
            init_request = {
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
            
            response = await client.post(f"{base_url}/messages", json=init_request)
            print(f"✅ Initialize response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Server info: {result.get('result', {}).get('serverInfo', {})}")
            
            # Test 2: List tools
            print("\n🔧 Step 2: List available tools")
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            response = await client.post(f"{base_url}/messages", json=tools_request)
            print(f"✅ Tools list response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                tools = result.get('result', {}).get('tools', [])
                print(f"   Found {len(tools)} tools")
                lab_tools = [t['name'] for t in tools if 'lab' in t['name']]
                print(f"   Lab tools: {lab_tools}")
            
            # Test 3: Connect to EVE-NG
            print("\n🔗 Step 3: Connect to EVE-NG server")
            connect_request = {
                "jsonrpc": "2.0",
                "id": 3,
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
            
            response = await client.post(f"{base_url}/messages", json=connect_request)
            print(f"✅ Connect response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Connect result: {result.get('result', {})}")
            else:
                print(f"   Error: {response.text}")
                return
            
            # Test 4: List existing labs
            print("\n📋 Step 4: List existing labs")
            list_labs_request = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "list_labs",
                    "arguments": {
                        "path": "/"
                    }
                }
            }
            
            response = await client.post(f"{base_url}/messages", json=list_labs_request)
            print(f"✅ List labs response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Labs result: {result.get('result', {})}")
            
            # Test 5: Create test lab
            print("\n🏗️ Step 5: Create test lab")
            create_lab_request = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "create_lab",
                    "arguments": {
                        "name": "mcp_test_lab",
                        "description": "Test lab created via MCP HTTP interface",
                        "author": "MCP Testing",
                        "version": "1.0",
                        "path": "/"
                    }
                }
            }
            
            response = await client.post(f"{base_url}/messages", json=create_lab_request)
            print(f"✅ Create lab response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Create result: {result.get('result', {})}")
            else:
                print(f"   Error: {response.text}")
            
            # Test 6: List labs again
            print("\n📋 Step 6: List labs after creation")
            response = await client.post(f"{base_url}/messages", json=list_labs_request)
            print(f"✅ List labs (after) response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Updated labs: {result.get('result', {})}")
            
            print("\n🎉 MCP HTTP Test Complete!")
            print("👀 Please check your EVE-NG UI - you should see 'mcp_test_lab.unl'")
            
        except Exception as e:
            print(f"❌ Error during HTTP test: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_lab_creation())
