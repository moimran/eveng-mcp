#!/usr/bin/env python3
"""
Detailed debug script to check EVE-NG API responses
"""

import asyncio
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evengsdk.api import EvengApi
from evengsdk.client import EvengClient

async def debug_api_detailed():
    """Debug EVE-NG API responses in detail"""
    
    print("🔍 Detailed EVE-NG API Debug")
    print("=" * 50)
    
    try:
        # Create client and API directly
        print("🔗 Creating EVE-NG client...")
        client = EvengClient(
            host="eve.local",
            port=80,
            protocol="http"
        )

        # Login
        print("🔐 Logging in...")
        login_result = client.login("admin", "eve")
        print(f"Login result: {login_result}")
        
        # Create API instance
        api = EvengApi(client)
        
        # Test list_folders
        print("\n📋 Testing list_folders()...")
        try:
            folders_result = api.list_folders()
            print(f"Type: {type(folders_result)}")
            print(f"Keys: {list(folders_result.keys()) if isinstance(folders_result, dict) else 'Not a dict'}")
            print(f"Full content: {json.dumps(folders_result, indent=2)}")
        except Exception as e:
            print(f"Error with list_folders(): {e}")
            import traceback
            traceback.print_exc()
            
        # Test get_folder for root
        print("\n📁 Testing get_folder('/')...")
        try:
            folder_result = api.get_folder("/")
            print(f"Type: {type(folder_result)}")
            print(f"Keys: {list(folder_result.keys()) if isinstance(folder_result, dict) else 'Not a dict'}")
            print(f"Full content: {json.dumps(folder_result, indent=2)}")
        except Exception as e:
            print(f"Error with get_folder('/'): {e}")
            import traceback
            traceback.print_exc()
            
        # Test get_folder for dev
        print("\n📁 Testing get_folder('/dev')...")
        try:
            folder_result = api.get_folder("/dev")
            print(f"Type: {type(folder_result)}")
            print(f"Keys: {list(folder_result.keys()) if isinstance(folder_result, dict) else 'Not a dict'}")
            print(f"Full content: {json.dumps(folder_result, indent=2)}")
        except Exception as e:
            print(f"Error with get_folder('/dev'): {e}")
            import traceback
            traceback.print_exc()
        
        # Logout
        print("\n🔌 Logging out...")
        client.logout()
        print("✅ Logged out successfully!")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_api_detailed())
