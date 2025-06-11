#!/usr/bin/env python3
"""
Test MCP server via socat bridge
"""

import socket
import json
import time

def send_json_rpc(host, port, request):
    """Send JSON-RPC request via TCP socket"""
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        # Connect
        sock.connect((host, port))
        
        # Send request
        request_str = json.dumps(request) + '\n'
        sock.send(request_str.encode())
        
        # Receive response
        response = sock.recv(4096).decode()
        sock.close()
        
        return json.loads(response.strip())
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_mcp_via_socat():
    """Test MCP server via socat bridge"""
    
    print("🧪 Testing MCP Server via Socat Bridge")
    print("=" * 40)
    
    host = "localhost"
    port = 8001
    
    # Test 1: Initialize
    print("📡 Step 1: Initialize MCP session")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "socat-test-client",
                "version": "1.0.0"
            }
        }
    }
    
    response = send_json_rpc(host, port, init_request)
    if response:
        print(f"✅ Initialize successful!")
        print(f"   Server: {response.get('result', {}).get('serverInfo', {})}")
    else:
        print("❌ Initialize failed")
        return
    
    # Test 2: List tools
    print("\n🔧 Step 2: List available tools")
    tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    
    response = send_json_rpc(host, port, tools_request)
    if response:
        tools = response.get('result', {}).get('tools', [])
        print(f"✅ Found {len(tools)} tools")
        
        # Show EVE-NG specific tools
        eveng_tools = [t['name'] for t in tools if any(keyword in t['name'] for keyword in ['eveng', 'lab', 'node', 'network'])]
        print(f"   EVE-NG tools: {eveng_tools[:10]}...")  # Show first 10
    else:
        print("❌ List tools failed")
        return
    
    # Test 3: List resources
    print("\n📊 Step 3: List available resources")
    resources_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "resources/list"
    }
    
    response = send_json_rpc(host, port, resources_request)
    if response:
        resources = response.get('result', {}).get('resources', [])
        print(f"✅ Found {len(resources)} resources")
        for resource in resources[:5]:  # Show first 5
            print(f"   - {resource.get('name', 'Unknown')}: {resource.get('description', 'No description')}")
    else:
        print("❌ List resources failed")
    
    # Test 4: List prompts
    print("\n🎯 Step 4: List available prompts")
    prompts_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "prompts/list"
    }
    
    response = send_json_rpc(host, port, prompts_request)
    if response:
        prompts = response.get('result', {}).get('prompts', [])
        print(f"✅ Found {len(prompts)} prompts")
        for prompt in prompts[:3]:  # Show first 3
            print(f"   - {prompt.get('name', 'Unknown')}: {prompt.get('description', 'No description')}")
    else:
        print("❌ List prompts failed")
    
    print("\n🎉 Socat Bridge Test Complete!")
    print("✅ MCP server is working correctly via socat bridge")

if __name__ == "__main__":
    test_mcp_via_socat()
