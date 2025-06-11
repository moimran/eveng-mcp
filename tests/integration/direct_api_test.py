#!/usr/bin/env python3
"""
Direct API Testing - Test each MCP tool individually and verify with EVE-NG API
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime

class DirectAPITester:
    def __init__(self):
        self.eveng_base_url = "http://eve.local:80"
        self.eveng_username = "admin"
        self.eveng_password = "eve"
        self.test_results = []
        self.eveng_session = None
        self.test_lab_name = "direct_api_test"
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
    
    def run_mcp_command(self, command: str) -> Dict:
        """Run MCP command directly"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {"success": True, "output": result.stdout, "stderr": result.stderr}
            else:
                return {"success": False, "output": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
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
    
    async def test_basic_commands(self):
        """Test basic MCP commands"""
        print("\n🔧 Testing Basic MCP Commands")
        print("=" * 50)
        
        # Test 1: Connection test
        mcp_result = self.run_mcp_command("uv run eveng-mcp-server test-connection --host eve.local --username admin --password eve")
        eveng_result = await self.call_eveng_api("GET", "/status")
        
        if mcp_result["success"] and "Connection successful" in mcp_result["output"]:
            await self.log_test("test-connection", "PASS", mcp_result, eveng_result, "CLI connection test successful")
        else:
            await self.log_test("test-connection", "FAIL", mcp_result, eveng_result)
        
        # Test 2: Config info
        mcp_result = self.run_mcp_command("uv run eveng-mcp-server config-info")
        
        if mcp_result["success"] and "EVE-NG Configuration" in mcp_result["output"]:
            await self.log_test("config-info", "PASS", mcp_result, None, "Configuration displayed successfully")
        else:
            await self.log_test("config-info", "FAIL", mcp_result, None)
        
        # Test 3: Version
        mcp_result = self.run_mcp_command("uv run eveng-mcp-server version")
        
        if mcp_result["success"] and "EVE-NG MCP Server" in mcp_result["output"]:
            await self.log_test("version", "PASS", mcp_result, None, "Version info displayed")
        else:
            await self.log_test("version", "FAIL", mcp_result, None)
    
    async def test_mcp_inspector_tools(self):
        """Test MCP tools using inspector"""
        print("\n🔍 Testing MCP Tools via Inspector")
        print("=" * 50)
        
        # Test 1: List tools
        mcp_result = self.run_mcp_command('npx @modelcontextprotocol/inspector --cli "uv run eveng-mcp-server run --transport stdio" --method tools/list')
        
        if mcp_result["success"] and "tools" in mcp_result["output"]:
            await self.log_test("inspector-tools-list", "PASS", mcp_result, None, "Tools listed via inspector")
        else:
            await self.log_test("inspector-tools-list", "FAIL", mcp_result, None)
        
        # Test 2: List resources
        mcp_result = self.run_mcp_command('npx @modelcontextprotocol/inspector --cli "uv run eveng-mcp-server run --transport stdio" --method resources/list')
        
        if mcp_result["success"] and "resources" in mcp_result["output"]:
            await self.log_test("inspector-resources-list", "PASS", mcp_result, None, "Resources listed via inspector")
        else:
            await self.log_test("inspector-resources-list", "FAIL", mcp_result, None)
        
        # Test 3: List prompts
        mcp_result = self.run_mcp_command('npx @modelcontextprotocol/inspector --cli "uv run eveng-mcp-server run --transport stdio" --method prompts/list')
        
        if mcp_result["success"] and "prompts" in mcp_result["output"]:
            await self.log_test("inspector-prompts-list", "PASS", mcp_result, None, "Prompts listed via inspector")
        else:
            await self.log_test("inspector-prompts-list", "FAIL", mcp_result, None)
    
    async def test_eveng_api_directly(self):
        """Test EVE-NG API directly to verify it's working"""
        print("\n🌐 Testing EVE-NG API Directly")
        print("=" * 50)
        
        # Test 1: Get status
        eveng_result = await self.call_eveng_api("GET", "/status")
        
        if "error" not in eveng_result and "data" in eveng_result:
            await self.log_test("eveng-status", "PASS", None, eveng_result, f"EVE-NG version: {eveng_result['data'].get('version', 'Unknown')}")
        else:
            await self.log_test("eveng-status", "FAIL", None, eveng_result)
        
        # Test 2: List labs
        eveng_result = await self.call_eveng_api("GET", "/labs")
        
        if "error" not in eveng_result:
            lab_count = len(eveng_result.get("data", {}))
            await self.log_test("eveng-list-labs", "PASS", None, eveng_result, f"Found {lab_count} labs")
        else:
            await self.log_test("eveng-list-labs", "FAIL", None, eveng_result)
        
        # Test 3: List templates
        eveng_result = await self.call_eveng_api("GET", "/list/templates")
        
        if "error" not in eveng_result:
            template_count = len(eveng_result.get("data", {}))
            await self.log_test("eveng-list-templates", "PASS", None, eveng_result, f"Found {template_count} templates")
        else:
            await self.log_test("eveng-list-templates", "FAIL", None, eveng_result)
    
    async def test_lab_creation_workflow(self):
        """Test complete lab creation workflow"""
        print("\n🧪 Testing Lab Creation Workflow")
        print("=" * 50)
        
        # Test 1: Create lab via EVE-NG API
        lab_data = {
            "name": self.test_lab_name,
            "description": "Direct API test lab",
            "author": "API Tester",
            "version": "1"
        }
        
        eveng_result = await self.call_eveng_api("POST", "/labs", lab_data)
        
        if "error" not in eveng_result:
            await self.log_test("eveng-create-lab", "PASS", None, eveng_result, f"Created lab {self.test_lab_name}")
        else:
            await self.log_test("eveng-create-lab", "FAIL", None, eveng_result)
        
        # Test 2: Get lab details
        eveng_result = await self.call_eveng_api("GET", f"/labs{self.test_lab_path}")
        
        if "error" not in eveng_result:
            await self.log_test("eveng-get-lab-details", "PASS", None, eveng_result, "Lab details retrieved")
        else:
            await self.log_test("eveng-get-lab-details", "FAIL", None, eveng_result)
        
        # Test 3: Delete lab (cleanup)
        eveng_result = await self.call_eveng_api("DELETE", f"/labs{self.test_lab_path}")
        
        if "error" not in eveng_result:
            await self.log_test("eveng-delete-lab", "PASS", None, eveng_result, f"Deleted lab {self.test_lab_name}")
        else:
            await self.log_test("eveng-delete-lab", "FAIL", None, eveng_result)
    
    async def run_comprehensive_test(self):
        """Run all tests"""
        print("🚀 Starting Direct API Testing")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"EVE-NG Server: {self.eveng_base_url}")
        print("=" * 60)
        
        try:
            # Run test suites
            await self.test_basic_commands()
            await self.test_mcp_inspector_tools()
            await self.test_eveng_api_directly()
            await self.test_lab_creation_workflow()
            
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
        with open("direct_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: direct_test_results.json")

async def main():
    tester = DirectAPITester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())
