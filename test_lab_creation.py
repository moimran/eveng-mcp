#!/usr/bin/env python3
"""
Direct test of EVE-NG MCP Server lab creation
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eveng_mcp_server.core import get_eveng_client
from eveng_mcp_server.config import get_config, configure_logging

async def test_lab_creation():
    """Test lab creation directly using EVE-NG client"""
    
    # Configure logging
    configure_logging()
    
    # Get EVE-NG client
    client = get_eveng_client()
    
    print("🧪 Testing Lab Creation via MCP Server")
    print("=" * 50)
    
    try:
        # Connect to EVE-NG server
        print("🔗 Connecting to EVE-NG server...")
        await client.connect(
            host="eve.local",
            username="admin", 
            password="eve",
            port=80,
            protocol="http"
        )
        print("✅ Connected successfully!")
        
        # List existing labs first
        print("\n📋 Listing existing labs...")
        existing_labs = await client.list_labs("/")
        print(f"Found {len(existing_labs.get('data', {}))} existing labs")
        
        # Create test lab
        print("\n🏗️ Creating test lab 'mcp_test_lab'...")
        lab_result = await client.create_lab(
            name="mcp_test_lab",
            path="/",
            description="Test lab created via MCP for validation",
            author="MCP Testing",
            version="1.0"
        )
        
        if lab_result.get('status') == 'success':
            print("✅ Lab created successfully!")
            print(f"Lab details: {lab_result}")
        else:
            print(f"❌ Lab creation failed: {lab_result}")
            
        # List labs again to confirm
        print("\n📋 Listing labs after creation...")
        updated_labs = await client.list_labs("/")
        print(f"Now found {len(updated_labs.get('data', {}))} labs")
        
        # Show lab details
        for lab_name, lab_info in updated_labs.get('data', {}).items():
            if 'mcp_test_lab' in lab_name:
                print(f"✅ Found our test lab: {lab_name}")
                print(f"   Description: {lab_info.get('description', 'N/A')}")
                print(f"   Author: {lab_info.get('author', 'N/A')}")
                break
        
        # Disconnect
        print("\n🔌 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected successfully!")
        
        print("\n🎉 Lab creation test completed!")
        print("👀 Please check your EVE-NG UI - you should see 'mcp_test_lab.unl' in the root folder")
        
    except Exception as e:
        print(f"❌ Error during lab creation test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_lab_creation())
