#!/usr/bin/env python3
"""
Direct test of MCP tools by importing and calling them directly
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eveng_mcp_server.tools.lab_management import (
    connect_eveng_server,
    list_labs,
    create_lab,
    get_lab_details
)
from eveng_mcp_server.core import get_eveng_client

async def test_lab_management():
    """Test lab management tools directly"""
    
    print("🧪 Testing Lab Management Tools Directly")
    print("=" * 50)
    
    try:
        # Step 1: Connect to EVE-NG server
        print("🔗 Step 1: Connect to EVE-NG server")
        connect_result = await connect_eveng_server({
            "host": "eve.local",
            "username": "admin",
            "password": "eve",
            "port": 80,
            "protocol": "http"
        })
        print(f"✅ Connection result: {connect_result}")
        
        # Step 2: List existing labs
        print("\n📋 Step 2: List existing labs")
        labs_result = await list_labs({"path": "/"})
        print(f"✅ Labs result: {labs_result}")
        
        # Step 3: Create test lab
        print("\n🏗️ Step 3: Create test lab")
        create_result = await create_lab({
            "name": "mcp_test_lab",
            "description": "Test lab created via MCP tools",
            "author": "MCP Testing",
            "version": "1.0",
            "path": "/"
        })
        print(f"✅ Create result: {create_result}")
        
        # Step 4: List labs again
        print("\n📋 Step 4: List labs after creation")
        updated_labs = await list_labs({"path": "/"})
        print(f"✅ Updated labs: {updated_labs}")
        
        # Step 5: Get lab details
        print("\n📊 Step 5: Get lab details")
        try:
            details_result = await get_lab_details({"lab_path": "/mcp_test_lab.unl"})
            print(f"✅ Lab details: {details_result}")
        except Exception as e:
            print(f"ℹ️ Lab details (expected if just created): {e}")
        
        print("\n🎉 Lab Management Test Complete!")
        print("👀 Please check your EVE-NG UI - you should see 'mcp_test_lab.unl'")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_lab_management())
