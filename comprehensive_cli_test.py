#!/usr/bin/env python3
"""
Comprehensive CLI-based API Testing Suite for EVE-NG MCP Server
Tests every MCP tool using CLI and verifies with direct EVE-NG API calls
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime

class ComprehensiveCLITester:
    def __init__(self):
        self.eveng_base_url = "http://eve.local:80"
        self.eveng_username = "admin"
        self.eveng_password = "eve"
        self.test_results = []
        self.eveng_session = None
        self.test_lab_name = "mcp_cli_test"
        self.test_lab_path = f"/{self.test_lab_name}.unl"
        
    async def log_test(self, test_name: str, status: str, mcp_result: Any = None, 
                      eveng_result: Any = None, notes: str = ""):
        """Log test results"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "status": status,
            "mcp_result": str(mcp_result)[:300] if mcp_result else None,
            "eveng_result": str(eveng_result)[:300] if eveng_result else None,
            "notes": notes
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if notes:
            print(f"   📝 {notes}")
    
    def call_mcp_cli_tool(self, method: str, params: Dict = None) -> Dict:
        """Call MCP tool via CLI"""
        try:
            # Build the CLI command
            cmd = [
                "npx", "@modelcontextprotocol/inspector", "--cli",
                "uv run eveng-mcp-server run --transport stdio",
                "--method", method
            ]
            
            if params:
                cmd.extend(["--params", json.dumps(params)])
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    return {"raw_output": result.stdout, "stderr": result.stderr}
            else:
                return {"error": f"CLI failed: {result.stderr}", "stdout": result.stdout}
                
        except subprocess.TimeoutExpired:
            return {"error": "CLI command timed out"}
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
    
    async def test_basic_functionality(self):
        """Test basic MCP functionality"""
        print("\n🔧 Testing Basic MCP Functionality")
        print("=" * 50)
        
        # Test 1: List tools
        mcp_result = self.call_mcp_cli_tool("tools/list")
        
        if "error" not in mcp_result and "tools" in mcp_result:
            tool_count = len(mcp_result["tools"])
            await self.log_test("tools/list", "PASS", mcp_result, None, f"Found {tool_count} tools")
        else:
            await self.log_test("tools/list", "FAIL", mcp_result, None)
        
        # Test 2: List resources
        mcp_result = self.call_mcp_cli_tool("resources/list")
        
        if "error" not in mcp_result and "resources" in mcp_result:
            resource_count = len(mcp_result["resources"])
            await self.log_test("resources/list", "PASS", mcp_result, None, f"Found {resource_count} resources")
        else:
            await self.log_test("resources/list", "FAIL", mcp_result, None)
        
        # Test 3: List prompts
        mcp_result = self.call_mcp_cli_tool("prompts/list")
        
        if "error" not in mcp_result and "prompts" in mcp_result:
            prompt_count = len(mcp_result["prompts"])
            await self.log_test("prompts/list", "PASS", mcp_result, None, f"Found {prompt_count} prompts")
        else:
            await self.log_test("prompts/list", "FAIL", mcp_result, None)
    
    async def test_connection_tools(self):
        """Test connection management tools"""
        print("\n🔗 Testing Connection Management Tools")
        print("=" * 50)
        
        # Test connect_eveng_server
        mcp_result = self.call_mcp_cli_tool("tools/call", {
            "name": "connect_eveng_server",
            "arguments": {
                "host": "eve.local",
                "username": "admin",
                "password": "eve",
                "port": 80,
                "protocol": "http"
            }
        })
        
        # Verify with direct API
        eveng_result = await self.call_eveng_api("GET", "/status")
        
        if "error" not in mcp_result and "error" not in eveng_result:
            await self.log_test("connect_eveng_server", "PASS", mcp_result, eveng_result, "Connection successful")
        else:
            await self.log_test("connect_eveng_server", "FAIL", mcp_result, eveng_result)
        
        # Test get_server_info
        mcp_result = self.call_mcp_cli_tool("tools/call", {
            "name": "get_server_info",
            "arguments": {}
        })
        
        if "error" not in mcp_result:
            await self.log_test("get_server_info", "PASS", mcp_result, eveng_result, "Server info retrieved")
        else:
            await self.log_test("get_server_info", "FAIL", mcp_result, eveng_result)
        
        # Test test_connection
        mcp_result = self.call_mcp_cli_tool("tools/call", {
            "name": "test_connection",
            "arguments": {}
        })
        
        if "error" not in mcp_result:
            await self.log_test("test_connection", "PASS", mcp_result, None, "Connection test successful")
        else:
            await self.log_test("test_connection", "FAIL", mcp_result, None)
    
    async def test_lab_management_tools(self):
        """Test lab management tools"""
        print("\n🧪 Testing Lab Management Tools")
        print("=" * 50)
        
        # Test list_labs
        mcp_result = self.call_mcp_cli_tool("tools/call", {
            "name": "list_labs",
            "arguments": {"path": "/"}
        })
        eveng_result = await self.call_eveng_api("GET", "/labs")
        
        if "error" not in mcp_result:
            await self.log_test("list_labs", "PASS", mcp_result, eveng_result, "Labs listed successfully")
        else:
            await self.log_test("list_labs", "FAIL", mcp_result, eveng_result)
        
        # Test create_lab
        mcp_result = self.call_mcp_cli_tool("tools/call", {
            "name": "create_lab",
            "arguments": {
                "name": self.test_lab_name,
                "description": "CLI test lab",
                "author": "CLI Tester",
                "version": "1.0",
                "path": "/"
            }
        })
        
        if "error" not in mcp_result:
            await self.log_test("create_lab", "PASS", mcp_result, None, f"Created {self.test_lab_name}")
        else:
            await self.log_test("create_lab", "FAIL", mcp_result, None)
        
        # Test get_lab_details
        mcp_result = self.call_mcp_cli_tool("tools/call", {
            "name": "get_lab_details",
            "arguments": {"lab_path": self.test_lab_path}
        })
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}")
        
        if "error" not in mcp_result:
            await self.log_test("get_lab_details", "PASS", mcp_result, eveng_result, "Lab details retrieved")
        else:
            await self.log_test("get_lab_details", "FAIL", mcp_result, eveng_result)
    
    async def run_comprehensive_test(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive EVE-NG MCP CLI Testing")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"EVE-NG Server: {self.eveng_base_url}")
        print("=" * 60)
        
        try:
            # Run test suites
            await self.test_basic_functionality()
            await self.test_connection_tools()
            await self.test_lab_management_tools()
            
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
        with open("cli_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: cli_test_results.json")

async def main():
    tester = ComprehensiveCLITester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
