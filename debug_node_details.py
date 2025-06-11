#!/usr/bin/env python3
"""
Debug script to check detailed node information including console ports
"""

import asyncio
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eveng_mcp_server.core import get_eveng_client

async def debug_node_details():
    """Debug node details to see console port information"""
    
    print("🔍 Debugging Node Details and Console Information")
    print("=" * 60)
    
    client = get_eveng_client()
    
    try:
        # Connect to EVE-NG server
        print("🔗 Connecting to EVE-NG server...")
        await client.connect()
        print("✅ Connected successfully!")
        
        # Get nodes from devlab
        print("\n📋 Getting nodes from devlab...")
        try:
            nodes_response = await asyncio.to_thread(client.api.list_nodes, "//dev/devlab.unl")
            nodes = nodes_response.get('data', {})
            
            print(f"Found {len(nodes)} nodes")
            print(f"Nodes response structure: {json.dumps(nodes_response, indent=2)}")
            
            # Get detailed info for each node
            for node_id, node_info in nodes.items():
                print(f"\n🖥️  Node {node_id} - {node_info.get('name', 'Unknown')}:")
                print(f"   Full node data: {json.dumps(node_info, indent=2)}")
                
                # Try to get individual node details
                try:
                    node_detail_response = await asyncio.to_thread(client.api.get_node, "//dev/devlab.unl", node_id)
                    print(f"   Individual node details: {json.dumps(node_detail_response, indent=2)}")
                except Exception as e:
                    print(f"   Failed to get individual node details: {e}")
                    
        except Exception as e:
            print(f"❌ Error getting nodes: {e}")
            import traceback
            traceback.print_exc()
        
        # Disconnect
        print("\n🔌 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected successfully!")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_node_details())
