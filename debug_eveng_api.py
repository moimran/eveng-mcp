#!/usr/bin/env python3
"""
Debug script to check EVE-NG API responses
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eveng_mcp_server.core import get_eveng_client

async def debug_api():
    """Debug EVE-NG API responses"""
    
    print("🔍 Debugging EVE-NG API responses")
    print("=" * 50)
    
    client = get_eveng_client()
    
    try:
        # Connect to EVE-NG server
        print("🔗 Connecting to EVE-NG server...")
        await client.connect()
        print("✅ Connected successfully!")
        
        # Test list_folders
        print("\n📋 Testing list_folders()...")
        folders_result = await asyncio.to_thread(client.api.list_folders)
        print(f"Type: {type(folders_result)}")
        print(f"Content: {folders_result}")
        
        # Test get_folder for root
        print("\n📁 Testing get_folder('/')...")
        try:
            folder_result = await asyncio.to_thread(client.api.get_folder, "/")
            print(f"Type: {type(folder_result)}")
            print(f"Content: {folder_result}")
        except Exception as e:
            print(f"Error with get_folder('/'): {e}")
            
        # Test get_folder for empty string
        print("\n📁 Testing get_folder('')...")
        try:
            folder_result = await asyncio.to_thread(client.api.get_folder, "")
            print(f"Type: {type(folder_result)}")
            print(f"Content: {folder_result}")
        except Exception as e:
            print(f"Error with get_folder(''): {e}")
        
        # Disconnect
        print("\n🔌 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected successfully!")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_api())
