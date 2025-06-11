#!/usr/bin/env python3
"""
Debug script to check get_lab API response
"""

import asyncio
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eveng_mcp_server.core import get_eveng_client

async def test_get_lab_debug():
    """Test get_lab function to see the actual API response"""
    
    print("🔍 Testing get_lab function")
    print("=" * 50)
    
    client = get_eveng_client()
    
    try:
        # Connect to EVE-NG server
        print("🔗 Connecting to EVE-NG server...")
        await client.connect()
        print("✅ Connected successfully!")
        
        # Test get_lab for devlab
        print("\n📋 Testing get_lab('//dev/devlab.unl')...")
        try:
            lab_data = await client.get_lab("//dev/devlab.unl")
            print(f"✅ Success! Lab data type: {type(lab_data)}")
            print(f"Lab data keys: {list(lab_data.keys()) if isinstance(lab_data, dict) else 'Not a dict'}")
            print(f"Full lab data: {json.dumps(lab_data, indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
        # Test get_lab for mcp_test_lab
        print("\n📋 Testing get_lab('//dev/mcp_test_lab.unl')...")
        try:
            lab_data = await client.get_lab("//dev/mcp_test_lab.unl")
            print(f"✅ Success! Lab data type: {type(lab_data)}")
            print(f"Lab data keys: {list(lab_data.keys()) if isinstance(lab_data, dict) else 'Not a dict'}")
            print(f"Full lab data: {json.dumps(lab_data, indent=2)}")
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
    asyncio.run(test_get_lab_debug())
