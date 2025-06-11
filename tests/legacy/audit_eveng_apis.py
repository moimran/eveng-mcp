#!/usr/bin/env python3
"""
Comprehensive audit of all EVE-NG APIs to ensure we're getting complete information
"""

import asyncio
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eveng_mcp_server.core import get_eveng_client

async def audit_all_apis():
    """Comprehensive audit of all EVE-NG APIs"""
    
    print("🔍 COMPREHENSIVE EVE-NG API AUDIT")
    print("=" * 60)
    
    client = get_eveng_client()
    
    try:
        # Connect to EVE-NG server
        print("🔗 Connecting to EVE-NG server...")
        await client.connect()
        print("✅ Connected successfully!")
        
        # 1. FOLDERS API AUDIT
        print("\n" + "="*60)
        print("📁 1. FOLDERS API AUDIT")
        print("="*60)
        
        print("\n📋 Testing list_folders()...")
        folders_response = await asyncio.to_thread(client.api.list_folders)
        print(f"Response type: {type(folders_response)}")
        print(f"Response keys: {list(folders_response.keys()) if isinstance(folders_response, dict) else 'Not a dict'}")
        print(f"Full response: {json.dumps(folders_response, indent=2)}")
        
        print("\n📋 Testing get_folder('/')...")
        try:
            root_folder = await asyncio.to_thread(client.api.get_folder, "/")
            print(f"Root folder type: {type(root_folder)}")
            print(f"Root folder keys: {list(root_folder.keys()) if isinstance(root_folder, dict) else 'Not a dict'}")
            print(f"Root folder: {json.dumps(root_folder, indent=2)}")
        except Exception as e:
            print(f"Error getting root folder: {e}")
            
        print("\n📋 Testing get_folder('/dev')...")
        try:
            dev_folder = await asyncio.to_thread(client.api.get_folder, "/dev")
            print(f"Dev folder type: {type(dev_folder)}")
            print(f"Dev folder keys: {list(dev_folder.keys()) if isinstance(dev_folder, dict) else 'Not a dict'}")
            print(f"Dev folder: {json.dumps(dev_folder, indent=2)}")
        except Exception as e:
            print(f"Error getting dev folder: {e}")
        
        # 2. LAB API AUDIT
        print("\n" + "="*60)
        print("🧪 2. LAB API AUDIT")
        print("="*60)
        
        lab_path = "//dev/devlab.unl"
        print(f"\n📋 Testing get_lab('{lab_path}')...")
        try:
            lab_response = await asyncio.to_thread(client.api.get_lab, lab_path)
            print(f"Lab response type: {type(lab_response)}")
            print(f"Lab response keys: {list(lab_response.keys()) if isinstance(lab_response, dict) else 'Not a dict'}")
            print(f"Lab response: {json.dumps(lab_response, indent=2)}")
        except Exception as e:
            print(f"Error getting lab: {e}")
        
        # 3. NODES API AUDIT
        print("\n" + "="*60)
        print("🖥️  3. NODES API AUDIT")
        print("="*60)
        
        print(f"\n📋 Testing list_nodes('{lab_path}')...")
        try:
            nodes_response = await asyncio.to_thread(client.api.list_nodes, lab_path)
            print(f"Nodes response type: {type(nodes_response)}")
            print(f"Nodes response keys: {list(nodes_response.keys()) if isinstance(nodes_response, dict) else 'Not a dict'}")
            print(f"Nodes response: {json.dumps(nodes_response, indent=2)}")
            
            # Test individual node details
            nodes_data = nodes_response.get('data', {})
            if nodes_data:
                first_node_id = list(nodes_data.keys())[0]
                print(f"\n📋 Testing get_node('{lab_path}', '{first_node_id}')...")
                try:
                    node_detail = await asyncio.to_thread(client.api.get_node, lab_path, first_node_id)
                    print(f"Node detail type: {type(node_detail)}")
                    print(f"Node detail keys: {list(node_detail.keys()) if isinstance(node_detail, dict) else 'Not a dict'}")
                    print(f"Node detail: {json.dumps(node_detail, indent=2)}")
                except Exception as e:
                    print(f"Error getting node detail: {e}")
                    
                # Test node interfaces
                print(f"\n📋 Testing get_node_interfaces('{lab_path}', '{first_node_id}')...")
                try:
                    interfaces = await asyncio.to_thread(client.api.get_node_interfaces, lab_path, first_node_id)
                    print(f"Interfaces type: {type(interfaces)}")
                    print(f"Interfaces keys: {list(interfaces.keys()) if isinstance(interfaces, dict) else 'Not a dict'}")
                    print(f"Interfaces: {json.dumps(interfaces, indent=2)}")
                except Exception as e:
                    print(f"Error getting interfaces: {e}")
                    
        except Exception as e:
            print(f"Error getting nodes: {e}")
        
        # 4. NETWORKS API AUDIT
        print("\n" + "="*60)
        print("🌐 4. NETWORKS API AUDIT")
        print("="*60)
        
        print(f"\n📋 Testing list_lab_networks('{lab_path}')...")
        try:
            networks_response = await asyncio.to_thread(client.api.list_lab_networks, lab_path)
            print(f"Networks response type: {type(networks_response)}")
            print(f"Networks response keys: {list(networks_response.keys()) if isinstance(networks_response, dict) else 'Not a dict'}")
            print(f"Networks response: {json.dumps(networks_response, indent=2)}")
            
            # Test individual network details
            networks_data = networks_response.get('data', {})
            if networks_data:
                first_net_id = list(networks_data.keys())[0]
                print(f"\n📋 Testing get_lab_network('{lab_path}', '{first_net_id}')...")
                try:
                    network_detail = await asyncio.to_thread(client.api.get_lab_network, lab_path, first_net_id)
                    print(f"Network detail type: {type(network_detail)}")
                    print(f"Network detail keys: {list(network_detail.keys()) if isinstance(network_detail, dict) else 'Not a dict'}")
                    print(f"Network detail: {json.dumps(network_detail, indent=2)}")
                except Exception as e:
                    print(f"Error getting network detail: {e}")
                    
        except Exception as e:
            print(f"Error getting networks: {e}")
        
        # 5. LINKS/TOPOLOGY API AUDIT
        print("\n" + "="*60)
        print("🔗 5. LINKS/TOPOLOGY API AUDIT")
        print("="*60)
        
        print(f"\n📋 Testing list_lab_links('{lab_path}')...")
        try:
            links_response = await asyncio.to_thread(client.api.list_lab_links, lab_path)
            print(f"Links response type: {type(links_response)}")
            print(f"Links response keys: {list(links_response.keys()) if isinstance(links_response, dict) else 'Not a dict'}")
            print(f"Links response: {json.dumps(links_response, indent=2)}")
        except Exception as e:
            print(f"Error getting links: {e}")
        
        # 6. TEMPLATES API AUDIT
        print("\n" + "="*60)
        print("📋 6. TEMPLATES API AUDIT")
        print("="*60)
        
        print("\n📋 Testing list_node_templates()...")
        try:
            templates_response = await asyncio.to_thread(client.api.list_node_templates)
            print(f"Templates response type: {type(templates_response)}")
            print(f"Templates response keys: {list(templates_response.keys()) if isinstance(templates_response, dict) else 'Not a dict'}")
            # Don't print full templates as it's very large
            if isinstance(templates_response, dict) and 'data' in templates_response:
                templates_data = templates_response['data']
                print(f"Templates data type: {type(templates_data)}")
                if isinstance(templates_data, dict):
                    print(f"Template categories: {list(templates_data.keys())}")
                    for category, templates in templates_data.items():
                        if isinstance(templates, dict):
                            print(f"  {category}: {len(templates)} templates")
                        break  # Just show first category structure
        except Exception as e:
            print(f"Error getting templates: {e}")
        
        # 7. SYSTEM INFO API AUDIT
        print("\n" + "="*60)
        print("ℹ️  7. SYSTEM INFO API AUDIT")
        print("="*60)
        
        print("\n📋 Testing get_system_status()...")
        try:
            status_response = await asyncio.to_thread(client.api.get_system_status)
            print(f"Status response type: {type(status_response)}")
            print(f"Status response keys: {list(status_response.keys()) if isinstance(status_response, dict) else 'Not a dict'}")
            print(f"Status response: {json.dumps(status_response, indent=2)}")
        except Exception as e:
            print(f"Error getting system status: {e}")
        
        # Disconnect
        print("\n🔌 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected successfully!")
        
        print("\n" + "="*60)
        print("✅ API AUDIT COMPLETE")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error during audit: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(audit_all_apis())
