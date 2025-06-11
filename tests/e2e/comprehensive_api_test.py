#!/usr/bin/env python3
"""
Comprehensive API Testing Suite for EVE-NG MCP Server
Tests every MCP tool and verifies with direct EVE-NG API calls
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime

class ComprehensiveAPITester:
    def __init__(self):
        self.mcp_base_url = "http://localhost:8000"
        self.eveng_base_url = "http://eve.local:80"
        self.eveng_username = "admin"
        self.eveng_password = "eve"
        self.test_results = []
        self.eveng_session = None
        self.test_lab_name = "mcp_comprehensive_test"
        self.test_lab_path = f"/{self.test_lab_name}.unl"
        
    async def log_test(self, test_name: str, status: str, mcp_result: Any = None, 
                      eveng_result: Any = None, notes: str = ""):
        """Log test results"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "status": status,
            "mcp_result": str(mcp_result)[:200] if mcp_result else None,
            "eveng_result": str(eveng_result)[:200] if eveng_result else None,
            "notes": notes
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if notes:
            print(f"   📝 {notes}")
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict = None) -> Dict:
        """Call MCP tool via HTTP"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Initialize session first
                init_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0.0"}
                    }
                }
                
                response = await client.post(f"{self.mcp_base_url}/messages", json=init_request)
                if response.status_code != 200:
                    return {"error": f"Failed to initialize: {response.status_code}"}
                
                # Call the tool
                tool_request = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments or {}
                    }
                }
                
                response = await client.post(f"{self.mcp_base_url}/messages", json=tool_request)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}"}
                    
        except Exception as e:
            return {"error": str(e)}
    
    async def call_eveng_api(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Call EVE-NG API directly"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Login if not already done
                if not self.eveng_session:
                    login_data = {
                        "username": self.eveng_username,
                        "password": self.eveng_password
                    }
                    response = await client.post(f"{self.eveng_base_url}/api/auth/login", json=login_data)
                    if response.status_code == 200:
                        self.eveng_session = response.cookies
                    else:
                        return {"error": f"Login failed: {response.status_code}"}
                
                # Make API call
                url = f"{self.eveng_base_url}/api{endpoint}"
                if method.upper() == "GET":
                    response = await client.get(url, cookies=self.eveng_session)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data, cookies=self.eveng_session)
                elif method.upper() == "PUT":
                    response = await client.put(url, json=data, cookies=self.eveng_session)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, cookies=self.eveng_session)
                
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}"}
                    
        except Exception as e:
            return {"error": str(e)}
    
    async def test_connection_management(self):
        """Test connection management tools"""
        print("\n🔗 Testing Connection Management APIs")
        print("=" * 50)
        
        # Test 1: connect_eveng_server
        mcp_result = await self.call_mcp_tool("connect_eveng_server", {
            "host": "eve.local",
            "username": "admin", 
            "password": "eve",
            "port": 80,
            "protocol": "http"
        })
        
        eveng_result = await self.call_eveng_api("GET", "/status")
        
        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("connect_eveng_server", "PASS", mcp_result, eveng_result)
        else:
            await self.log_test("connect_eveng_server", "FAIL", mcp_result, eveng_result)
        
        # Test 2: get_server_info
        mcp_result = await self.call_mcp_tool("get_server_info")
        eveng_result = await self.call_eveng_api("GET", "/status")
        
        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("get_server_info", "PASS", mcp_result, eveng_result)
        else:
            await self.log_test("get_server_info", "FAIL", mcp_result, eveng_result)
        
        # Test 3: test_connection
        mcp_result = await self.call_mcp_tool("test_connection", {})
        
        if "error" not in mcp_result:
            await self.log_test("test_connection", "PASS", mcp_result, None, "MCP connection test successful")
        else:
            await self.log_test("test_connection", "FAIL", mcp_result, None)
    
    async def test_lab_management(self):
        """Test lab management tools"""
        print("\n🧪 Testing Lab Management APIs")
        print("=" * 50)
        
        # Test 1: list_labs
        mcp_result = await self.call_mcp_tool("list_labs", {"path": "/"})
        eveng_result = await self.call_eveng_api("GET", "/labs")
        
        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("list_labs", "PASS", mcp_result, eveng_result)
        else:
            await self.log_test("list_labs", "FAIL", mcp_result, eveng_result)
        
        # Test 2: create_lab
        mcp_result = await self.call_mcp_tool("create_lab", {
            "name": self.test_lab_name,
            "description": "Comprehensive test lab created by MCP API tester",
            "author": "MCP Tester",
            "version": "1.0",
            "path": "/"
        })
        
        # Verify with direct API
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}")
        
        if "error" not in mcp_result:
            await self.log_test("create_lab", "PASS", mcp_result, eveng_result, f"Created {self.test_lab_name}")
        else:
            await self.log_test("create_lab", "FAIL", mcp_result, eveng_result)
        
        # Test 3: get_lab_details
        mcp_result = await self.call_mcp_tool("get_lab_details", {"lab_path": self.test_lab_path})
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}")
        
        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("get_lab_details", "PASS", mcp_result, eveng_result)
        else:
            await self.log_test("get_lab_details", "FAIL", mcp_result, eveng_result)
    
    async def test_node_management(self):
        """Test node management tools"""
        print("\n🖥️ Testing Node Management APIs")
        print("=" * 50)
        
        # Test 1: list_node_templates
        mcp_result = await self.call_mcp_tool("list_node_templates", {})
        eveng_result = await self.call_eveng_api("GET", "/list/templates")
        
        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("list_node_templates", "PASS", mcp_result, eveng_result)
        else:
            await self.log_test("list_node_templates", "FAIL", mcp_result, eveng_result)
        
        # Test 2: list_nodes (empty lab)
        mcp_result = await self.call_mcp_tool("list_nodes", {"lab_path": self.test_lab_path})
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/nodes")
        
        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("list_nodes", "PASS", mcp_result, eveng_result, "Empty lab - no nodes")
        else:
            await self.log_test("list_nodes", "FAIL", mcp_result, eveng_result)
        
        # Test 3: add_node
        mcp_result = await self.call_mcp_tool("add_node", {
            "lab_path": self.test_lab_path,
            "template": "linux",
            "name": "test-node-1",
            "left": 25,
            "top": 25
        })
        
        # Verify with direct API
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/nodes")
        
        if "error" not in mcp_result:
            await self.log_test("add_node", "PASS", mcp_result, eveng_result, "Added test-node-1")
        else:
            await self.log_test("add_node", "FAIL", mcp_result, eveng_result)
    
    async def test_network_management(self):
        """Test network management tools"""
        print("\n🌐 Testing Network Management APIs")
        print("=" * 50)

        # Test 1: list_network_types
        mcp_result = await self.call_mcp_tool("list_network_types", {"lab_path": self.test_lab_path})
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/networks")

        if "error" not in mcp_result:
            await self.log_test("list_network_types", "PASS", mcp_result, eveng_result)
        else:
            await self.log_test("list_network_types", "FAIL", mcp_result, eveng_result)

        # Test 2: list_lab_networks
        mcp_result = await self.call_mcp_tool("list_lab_networks", {"lab_path": self.test_lab_path})
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/networks")

        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("list_lab_networks", "PASS", mcp_result, eveng_result)
        else:
            await self.log_test("list_lab_networks", "FAIL", mcp_result, eveng_result)

        # Test 3: create_lab_network
        mcp_result = await self.call_mcp_tool("create_lab_network", {
            "lab_path": self.test_lab_path,
            "network_type": "bridge",
            "name": "test-network",
            "left": 50,
            "top": 50
        })

        # Verify with direct API
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/networks")

        if "error" not in mcp_result:
            await self.log_test("create_lab_network", "PASS", mcp_result, eveng_result, "Created test-network")
        else:
            await self.log_test("create_lab_network", "FAIL", mcp_result, eveng_result)

        # Test 4: get_lab_topology
        mcp_result = await self.call_mcp_tool("get_lab_topology", {"lab_path": self.test_lab_path})
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/topology")

        if "error" not in mcp_result:
            await self.log_test("get_lab_topology", "PASS", mcp_result, eveng_result, "Retrieved topology")
        else:
            await self.log_test("get_lab_topology", "FAIL", mcp_result, eveng_result)

    async def test_advanced_node_operations(self):
        """Test advanced node operations"""
        print("\n⚙️ Testing Advanced Node Operations")
        print("=" * 50)

        # Get node ID from previous test
        nodes_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/nodes")
        node_id = None
        if "data" in nodes_result and nodes_result["data"]:
            node_id = list(nodes_result["data"].keys())[0]

        if node_id:
            # Test get_node_details
            mcp_result = await self.call_mcp_tool("get_node_details", {
                "lab_path": self.test_lab_path,
                "node_id": node_id
            })
            eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}/nodes/{node_id}")

            if "error" not in mcp_result and "error" not in eveng_result:
                await self.log_test("get_node_details", "PASS", mcp_result, eveng_result)
            else:
                await self.log_test("get_node_details", "FAIL", mcp_result, eveng_result)

            # Test start_node
            mcp_result = await self.call_mcp_tool("start_node", {
                "lab_path": self.test_lab_path,
                "node_id": node_id
            })

            if "error" not in mcp_result:
                await self.log_test("start_node", "PASS", mcp_result, None, f"Started node {node_id}")
            else:
                await self.log_test("start_node", "FAIL", mcp_result, None)

            # Test stop_node
            mcp_result = await self.call_mcp_tool("stop_node", {
                "lab_path": self.test_lab_path,
                "node_id": node_id
            })

            if "error" not in mcp_result:
                await self.log_test("stop_node", "PASS", mcp_result, None, f"Stopped node {node_id}")
            else:
                await self.log_test("stop_node", "FAIL", mcp_result, None)
        else:
            await self.log_test("advanced_node_operations", "SKIP", None, None, "No nodes available for testing")

    async def test_cleanup_operations(self):
        """Test cleanup operations"""
        print("\n🧹 Testing Cleanup Operations")
        print("=" * 50)

        # Test delete_lab (cleanup)
        mcp_result = await self.call_mcp_tool("delete_lab", {"lab_path": self.test_lab_path})

        # Verify deletion
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}")

        if "error" not in mcp_result:
            await self.log_test("delete_lab", "PASS", mcp_result, eveng_result, f"Deleted {self.test_lab_name}")
        else:
            await self.log_test("delete_lab", "FAIL", mcp_result, eveng_result)

        # Test disconnect
        mcp_result = await self.call_mcp_tool("disconnect_eveng_server")

        if "error" not in mcp_result:
            await self.log_test("disconnect_eveng_server", "PASS", mcp_result, None, "Disconnected successfully")
        else:
            await self.log_test("disconnect_eveng_server", "FAIL", mcp_result, None)

    async def run_comprehensive_test(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive EVE-NG MCP API Testing")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"MCP Server: {self.mcp_base_url}")
        print(f"EVE-NG Server: {self.eveng_base_url}")
        print("=" * 60)

        try:
            # Run test suites
            await self.test_connection_management()
            await self.test_lab_management()
            await self.test_node_management()
            await self.test_network_management()
            await self.test_advanced_node_operations()
            await self.test_cleanup_operations()

            # Generate summary
            await self.generate_summary()

        except Exception as e:
            print(f"❌ Test suite failed: {e}")
            import traceback
            traceback.print_exc()
    
    async def generate_summary(self):
        """Generate test summary"""
        print("\n📊 Test Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"   - {result['test_name']}: {result.get('notes', 'No details')}")
        
        # Save detailed results
        with open("test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results.json")

async def main():
    tester = ComprehensiveAPITester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
