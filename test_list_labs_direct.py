#!/usr/bin/env python3
"""
Direct test of list_labs function to see the actual API response
"""

import asyncio
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eveng_mcp_server.core import get_eveng_client

async def test_list_labs_direct():
    """Test list_labs function directly"""
    
    print("🔍 Testing list_labs function directly")
    print("=" * 50)
    
    client = get_eveng_client()
    
    try:
        # Connect to EVE-NG server
        print("🔗 Connecting to EVE-NG server...")
        await client.connect()
        print("✅ Connected successfully!")
        
        # Test list_labs for root path
        print("\n📋 Testing list_labs('/')...")
        try:
            labs = await client.list_labs("/")
            print(f"✅ Success! Found {len(labs)} labs")
            for lab in labs:
                print(f"  - {lab}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
        # Test list_labs for /dev path
        print("\n📋 Testing list_labs('/dev')...")
        try:
            labs = await client.list_labs("/dev")
            print(f"✅ Success! Found {len(labs)} labs")
            for lab in labs:
                print(f"  - {lab}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Disconnect
        print("\n🔌 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected successfully!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_list_labs_direct())
