"""Workflow prompts for EVE-NG MCP Server."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from mcp.types import PromptMessage, TextContent

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ..core.eveng_client import EVENGClientWrapper

from ..config import get_logger


logger = get_logger("WorkflowPrompts")


def register_workflow_prompts(mcp: "FastMCP", eveng_client: "EVENGClientWrapper") -> None:
    """Register workflow prompts for guided operations."""
    
    @mcp.prompt("create_simple_lab")
    async def create_simple_lab_prompt(
        lab_name: str = "test_lab",
        lab_description: str = "Simple test laboratory"
    ) -> List[PromptMessage]:
        """Guide for creating a basic lab setup with essential components."""
        
        content = f"""# Create Simple Lab: {lab_name}

## Overview
This workflow will guide you through creating a basic network lab with fundamental components.

## Prerequisites
- EVE-NG server connection established
- Basic understanding of network topologies
- Required node templates available

## Step-by-Step Guide

### 1. Connect to EVE-NG Server
First, establish connection to your EVE-NG server:

```
Tool: connect_eveng_server
Parameters:
  host: "eve.local"
  username: "admin"
  password: "eve"
  protocol: "http"
  port: 80
```

### 2. Create the Lab
Create a new lab with basic metadata:

```
Tool: create_lab
Parameters:
  name: "{lab_name}"
  description: "{lab_description}"
  author: "Network Engineer"
  version: "1.0"
  path: "/"
```

### 3. Add Network Devices
Add essential network devices to your lab:

#### Router 1
```
Tool: add_node
Parameters:
  lab_path: "/{lab_name}.unl"
  template: "iosv"
  name: "R1"
  left: 25
  top: 40
  ram: 512
  cpu: 1
```

#### Router 2
```
Tool: add_node
Parameters:
  lab_path: "/{lab_name}.unl"
  template: "iosv"
  name: "R2"
  left: 75
  top: 40
  ram: 512
  cpu: 1
```

#### Switch
```
Tool: add_node
Parameters:
  lab_path: "/{lab_name}.unl"
  template: "iosvl2"
  name: "SW1"
  left: 50
  top: 70
  ram: 256
  cpu: 1
```

### 4. Create Networks
Add network segments for connectivity:

#### Management Network
```
Tool: create_lab_network
Parameters:
  lab_path: "/{lab_name}.unl"
  network_type: "cloud"
  name: "Management"
  left: 50
  top: 10
```

#### LAN Network
```
Tool: create_lab_network
Parameters:
  lab_path: "/{lab_name}.unl"
  network_type: "bridge"
  name: "LAN"
  left: 50
  top: 90
```

### 5. Connect Devices
Establish connectivity between devices:

#### Connect R1 to SW1
```
Tool: connect_node_to_node
Parameters:
  lab_path: "/{lab_name}.unl"
  src_node_id: "1"
  src_interface: "Gi0/0"
  dst_node_id: "3"
  dst_interface: "Gi0/0"
```

#### Connect R2 to SW1
```
Tool: connect_node_to_node
Parameters:
  lab_path: "/{lab_name}.unl"
  src_node_id: "2"
  src_interface: "Gi0/0"
  dst_node_id: "3"
  dst_interface: "Gi0/1"
```

#### Connect R1 and R2 directly
```
Tool: connect_node_to_node
Parameters:
  lab_path: "/{lab_name}.unl"
  src_node_id: "1"
  src_interface: "Gi0/1"
  dst_node_id: "2"
  dst_interface: "Gi0/1"
```

### 6. Verify Lab Setup
Check your lab configuration:

```
Tool: get_lab_details
Parameters:
  lab_path: "/{lab_name}.unl"
```

```
Tool: list_nodes
Parameters:
  lab_path: "/{lab_name}.unl"
```

```
Tool: get_lab_topology
Parameters:
  lab_path: "/{lab_name}.unl"
```

### 7. Start Lab
Power on all devices:

```
Tool: start_all_nodes
Parameters:
  lab_path: "/{lab_name}.unl"
```

## Next Steps
- Configure IP addresses on interfaces
- Set up routing protocols
- Test connectivity between devices
- Add additional devices as needed

## Tips
- Use descriptive names for devices and networks
- Plan IP addressing scheme before configuration
- Document your topology for future reference
- Test connectivity step by step

Your basic lab "{lab_name}" is now ready for configuration and testing!
"""
        
        return [
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=content)
            )
        ]
    
    @mcp.prompt("create_enterprise_topology")
    async def create_enterprise_topology_prompt(
        company_name: str = "Enterprise Corp",
        site_count: int = 3
    ) -> List[PromptMessage]:
        """Template for creating complex enterprise network topologies."""
        
        content = f"""# Create Enterprise Topology: {company_name}

## Overview
This workflow guides you through creating a comprehensive enterprise network topology with multiple sites, redundancy, and advanced features.

## Architecture Design
- **Core Layer**: Redundant core switches for high availability
- **Distribution Layer**: L3 switches for inter-VLAN routing
- **Access Layer**: L2 switches for end-user connectivity
- **WAN Edge**: Routers for site-to-site connectivity
- **Security**: Firewalls and security appliances

## Prerequisites
- EVE-NG server with sufficient resources
- Enterprise-grade node templates (ASR, Catalyst, ASA)
- Understanding of enterprise network design principles

## Phase 1: Core Infrastructure

### 1. Create Enterprise Lab
```
Tool: create_lab
Parameters:
  name: "{company_name.lower().replace(' ', '_')}_enterprise"
  description: "Enterprise network topology for {company_name}"
  author: "Network Architect"
  version: "1.0"
```

### 2. Core Layer (Redundant)
Deploy redundant core switches:

#### Core Switch 1
```
Tool: add_node
Parameters:
  template: "cat9kv"
  name: "CORE-SW-01"
  left: 40
  top: 20
  ram: 1024
  cpu: 2
```

#### Core Switch 2
```
Tool: add_node
Parameters:
  template: "cat9kv"
  name: "CORE-SW-02"
  left: 60
  top: 20
  ram: 1024
  cpu: 2
```

### 3. Distribution Layer
Deploy distribution switches for each site:

#### Site 1 Distribution
```
Tool: add_node
Parameters:
  template: "cat9kv"
  name: "DIST-SW-01A"
  left: 20
  top: 40
```

```
Tool: add_node
Parameters:
  template: "cat9kv"
  name: "DIST-SW-01B"
  left: 30
  top: 40
```

### 4. Access Layer
Deploy access switches:

#### Site 1 Access Switches
```
Tool: add_node
Parameters:
  template: "iosvl2"
  name: "ACC-SW-01"
  left: 15
  top: 60
```

```
Tool: add_node
Parameters:
  template: "iosvl2"
  name: "ACC-SW-02"
  left: 35
  top: 60
```

## Phase 2: WAN Connectivity

### 1. Edge Routers
Deploy WAN edge routers:

#### Primary Edge Router
```
Tool: add_node
Parameters:
  template: "asrv"
  name: "EDGE-RTR-01"
  left: 50
  top: 5
  ram: 2048
  cpu: 2
```

#### Backup Edge Router
```
Tool: add_node
Parameters:
  template: "asrv"
  name: "EDGE-RTR-02"
  left: 50
  top: 15
```

### 2. MPLS Provider Network
Simulate service provider infrastructure:

```
Tool: create_lab_network
Parameters:
  network_type: "cloud"
  name: "MPLS_Cloud"
  left: 50
  top: 0
```

## Phase 3: Security Infrastructure

### 1. Perimeter Firewall
```
Tool: add_node
Parameters:
  template: "asav"
  name: "FW-PERIMETER"
  left: 50
  top: 10
  ram: 2048
```

### 2. Internal Firewalls
```
Tool: add_node
Parameters:
  template: "asav"
  name: "FW-INTERNAL"
  left: 50
  top: 30
```

## Phase 4: Network Segments

### 1. Management Network
```
Tool: create_lab_network
Parameters:
  network_type: "bridge"
  name: "MGMT_VLAN"
  left: 10
  top: 10
```

### 2. Server Network
```
Tool: create_lab_network
Parameters:
  network_type: "bridge"
  name: "SERVER_VLAN"
  left: 90
  top: 40
```

### 3. User Networks
```
Tool: create_lab_network
Parameters:
  network_type: "bridge"
  name: "USER_VLAN_100"
  left: 10
  top: 80
```

```
Tool: create_lab_network
Parameters:
  network_type: "bridge"
  name: "USER_VLAN_200"
  left: 30
  top: 80
```

## Phase 5: Connectivity Matrix

### 1. Core Interconnections
Connect core switches with redundant links:

```
Tool: connect_node_to_node
Parameters:
  src_node_id: "1"  # CORE-SW-01
  src_interface: "Gi0/0"
  dst_node_id: "2"  # CORE-SW-02
  dst_interface: "Gi0/0"
```

### 2. Core to Distribution
Connect each distribution switch to both core switches:

```
Tool: connect_node_to_node
Parameters:
  src_node_id: "1"  # CORE-SW-01
  src_interface: "Gi0/1"
  dst_node_id: "3"  # DIST-SW-01A
  dst_interface: "Gi0/0"
```

### 3. Distribution to Access
Connect access switches to distribution layer:

```
Tool: connect_node_to_node
Parameters:
  src_node_id: "3"  # DIST-SW-01A
  src_interface: "Gi0/1"
  dst_node_id: "5"  # ACC-SW-01
  dst_interface: "Gi0/0"
```

## Phase 6: Verification and Testing

### 1. Verify Topology
```
Tool: get_lab_topology
Parameters:
  lab_path: "/{company_name.lower().replace(' ', '_')}_enterprise.unl"
```

### 2. Check All Nodes
```
Tool: list_nodes
Parameters:
  lab_path: "/{company_name.lower().replace(' ', '_')}_enterprise.unl"
```

### 3. Start Infrastructure
```
Tool: start_all_nodes
Parameters:
  lab_path: "/{company_name.lower().replace(' ', '_')}_enterprise.unl"
```

## Configuration Guidelines

### 1. IP Addressing Scheme
- Management: 10.0.0.0/24
- Core Links: 10.1.0.0/30 subnets
- Distribution Links: 10.2.0.0/30 subnets
- User VLANs: 192.168.x.0/24

### 2. VLAN Design
- VLAN 1: Native (unused)
- VLAN 10: Management
- VLAN 100-199: User VLANs
- VLAN 200-299: Server VLANs
- VLAN 999: Quarantine

### 3. Routing Protocols
- Core/Distribution: OSPF Area 0
- WAN: BGP with service provider
- Redundancy: HSRP/VRRP

### 4. Security Policies
- Inter-VLAN filtering
- Perimeter security
- Access control lists
- Network segmentation

## Advanced Features
- QoS implementation
- Multicast support
- Network monitoring
- Backup and recovery

Your enterprise topology for {company_name} is now ready for advanced configuration!
"""

        return [
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=content)
            )
        ]

    @mcp.prompt("diagnose_connectivity")
    async def diagnose_connectivity_prompt(
        lab_name: str = "test_lab",
        source_node: str = "R1",
        target_node: str = "R2"
    ) -> List[PromptMessage]:
        """Network troubleshooting workflow for connectivity issues."""

        content = f"""# Diagnose Connectivity Issues: {lab_name}

## Overview
Systematic approach to troubleshooting network connectivity between {source_node} and {target_node}.

## Troubleshooting Methodology
Follow the OSI model from bottom to top for systematic diagnosis.

## Step 1: Physical Layer Verification

### Check Lab Status
```
Tool: get_lab_details
Parameters:
  lab_path: "/{lab_name}.unl"
```

### Verify Node Status
```
Tool: list_nodes
Parameters:
  lab_path: "/{lab_name}.unl"
```

**Expected Results:**
- All nodes should be in "running" state (🟢)
- No nodes in "stopped" or "starting" state

### Check Individual Nodes
```
Tool: get_node_details
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "1"  # Adjust based on {source_node}
```

```
Tool: get_node_details
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "2"  # Adjust based on {target_node}
```

## Step 2: Data Link Layer Verification

### Check Topology
```
Tool: get_lab_topology
Parameters:
  lab_path: "/{lab_name}.unl"
```

**Verify:**
- Physical connections exist between nodes
- Interface assignments are correct
- No missing or incorrect connections

### Check Network Segments
```
Tool: list_lab_networks
Parameters:
  lab_path: "/{lab_name}.unl"
```

**Verify:**
- Required networks exist
- Network types are appropriate
- No network configuration issues

## Step 3: Network Layer Diagnosis

### Console Access Checklist
1. Access {source_node} console
2. Check interface status: `show ip interface brief`
3. Verify IP configuration: `show running-config`
4. Check routing table: `show ip route`

### Common Commands for {source_node}
```
# Interface status
show ip interface brief
show interfaces status

# IP configuration
show running-config interface
show ip interface

# Routing information
show ip route
show ip protocols
show ip arp
```

### Ping Tests from {source_node}
```
# Test local interfaces
ping [local_interface_ip]

# Test directly connected networks
ping [next_hop_ip]

# Test target node
ping [target_node_ip]

# Test with extended ping
ping
Protocol [ip]:
Target IP address: [target_ip]
Repeat count [5]: 10
Datagram size [100]:
Timeout in seconds [2]:
Extended commands [n]: y
Source address or interface: [source_interface]
```

## Step 4: Transport Layer Testing

### TCP Connectivity Tests
```
# Telnet to specific ports
telnet [target_ip] 23
telnet [target_ip] 22
telnet [target_ip] 80

# Check listening services
show tcp brief
show udp brief
```

## Step 5: Application Layer Verification

### Service-Specific Tests
```
# HTTP/HTTPS testing
curl http://[target_ip]
curl https://[target_ip]

# DNS resolution
nslookup [hostname]
dig [hostname]

# SNMP testing
snmpwalk -v2c -c public [target_ip]
```

## Common Issues and Solutions

### Issue 1: Node Not Starting
**Symptoms:** Node stuck in starting state
**Solutions:**
1. Check available resources
2. Verify image availability
3. Restart node
4. Wipe and reconfigure

**Commands:**
```
Tool: stop_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"

Tool: wipe_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"

Tool: start_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"
```

### Issue 2: No Physical Connectivity
**Symptoms:** Interfaces down, no carrier
**Solutions:**
1. Verify cable connections
2. Check interface configuration
3. Verify network segments

**Verification:**
```
Tool: get_lab_topology
Parameters:
  lab_path: "/{lab_name}.unl"
```

### Issue 3: IP Configuration Issues
**Symptoms:** Ping fails, wrong subnet
**Solutions:**
1. Verify IP addressing scheme
2. Check subnet masks
3. Verify VLAN configuration

### Issue 4: Routing Problems
**Symptoms:** Remote networks unreachable
**Solutions:**
1. Check routing tables
2. Verify routing protocols
3. Check default gateways

### Issue 5: Firewall/ACL Blocking
**Symptoms:** Selective connectivity issues
**Solutions:**
1. Check access control lists
2. Verify firewall rules
3. Review security policies

## Systematic Testing Approach

### 1. Layer-by-Layer Testing
- Start with physical connectivity
- Move up through OSI layers
- Test each layer thoroughly

### 2. Divide and Conquer
- Test connectivity to intermediate devices
- Isolate problem segments
- Focus on specific failure points

### 3. Documentation
- Record all test results
- Document configuration changes
- Maintain troubleshooting log

## Advanced Diagnostics

### Packet Capture
```
# Enable debug on interfaces
debug ip packet
debug ip icmp

# Monitor specific protocols
debug ospf events
debug bgp updates
```

### Performance Testing
```
# Bandwidth testing
iperf3 -s  # On target
iperf3 -c [target_ip]  # On source

# Latency testing
ping -c 100 [target_ip]
traceroute [target_ip]
```

### SNMP Monitoring
```
# Interface statistics
snmpwalk -v2c -c public [device_ip] 1.3.6.1.2.1.2.2.1.10
snmpwalk -v2c -c public [device_ip] 1.3.6.1.2.1.2.2.1.16

# System information
snmpwalk -v2c -c public [device_ip] 1.3.6.1.2.1.1
```

## Resolution Verification

### Final Connectivity Test
```
# Comprehensive ping test
ping [target_ip] repeat 100

# Application-level test
telnet [target_ip] [port]

# Performance verification
traceroute [target_ip]
```

### Documentation
1. Record root cause
2. Document solution steps
3. Update network documentation
4. Create prevention measures

## Prevention Strategies

### 1. Monitoring
- Implement network monitoring
- Set up alerting
- Regular health checks

### 2. Documentation
- Maintain accurate topology diagrams
- Document all configurations
- Keep troubleshooting procedures updated

### 3. Testing
- Regular connectivity testing
- Automated health checks
- Disaster recovery testing

Your connectivity diagnosis between {source_node} and {target_node} in {lab_name} is now complete!
"""

        return [
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=content)
            )
        ]

    @mcp.prompt("configure_lab_automation")
    async def configure_lab_automation_prompt(
        lab_name: str = "automation_lab",
        automation_type: str = "ansible"
    ) -> List[PromptMessage]:
        """Automation script generation for lab configuration and management."""

        content = f"""# Configure Lab Automation: {lab_name}

## Overview
This workflow guides you through setting up automation for your EVE-NG lab using {automation_type}.

## Automation Benefits
- Consistent configuration deployment
- Rapid lab provisioning
- Configuration backup and restore
- Compliance verification
- Disaster recovery

## Prerequisites
- EVE-NG lab with running devices
- Automation tools installed ({automation_type})
- Network connectivity to lab devices
- Device credentials configured

## Phase 1: Automation Environment Setup

### 1. Verify Lab Status
```
Tool: get_lab_details
Parameters:
  lab_path: "/{lab_name}.unl"
```

```
Tool: list_nodes
Parameters:
  lab_path: "/{lab_name}.unl"
```

### 2. Ensure All Nodes Are Running
```
Tool: start_all_nodes
Parameters:
  lab_path: "/{lab_name}.unl"
```

## Phase 2: Inventory Management

### Ansible Inventory Example
```yaml
# inventory.yml
all:
  children:
    routers:
      hosts:
        R1:
          ansible_host: 192.168.1.1
          ansible_network_os: ios
          ansible_user: admin
          ansible_password: cisco
        R2:
          ansible_host: 192.168.1.2
          ansible_network_os: ios
          ansible_user: admin
          ansible_password: cisco
    switches:
      hosts:
        SW1:
          ansible_host: 192.168.1.10
          ansible_network_os: ios
          ansible_user: admin
          ansible_password: cisco
  vars:
    ansible_connection: network_cli
    ansible_python_interpreter: /usr/bin/python3
```

### Python Script Inventory
```python
# inventory.py
devices = {{
    'routers': [
        {{'name': 'R1', 'ip': '192.168.1.1', 'type': 'ios'}},
        {{'name': 'R2', 'ip': '192.168.1.2', 'type': 'ios'}}
    ],
    'switches': [
        {{'name': 'SW1', 'ip': '192.168.1.10', 'type': 'ios'}}
    ]
}}
```

## Phase 3: Configuration Templates

### Interface Configuration Template
```jinja2
# templates/interface.j2
interface {{{{ interface_name }}}}
 description {{{{ interface_description }}}}
 ip address {{{{ ip_address }}}} {{{{ subnet_mask }}}}
 no shutdown
```

### OSPF Configuration Template
```jinja2
# templates/ospf.j2
router ospf [PROCESS_ID]
 router-id [ROUTER_ID]
[FOR_EACH_NETWORK]
 network [NETWORK_ADDRESS] [WILDCARD] area [AREA]
[END_FOR]
```

### VLAN Configuration Template
```jinja2
# templates/vlan.j2
[FOR_EACH_VLAN]
vlan [VLAN_ID]
 name [VLAN_NAME]
[END_FOR]
```

## Phase 4: Automation Playbooks

### Basic Configuration Playbook
```yaml
# playbooks/basic_config.yml
---
- name: Configure Basic Settings
  hosts: all
  gather_facts: no
  tasks:
    - name: Configure hostname
      ios_config:
        lines:
          - hostname [INVENTORY_HOSTNAME]

    - name: Configure management interface
      ios_config:
        lines:
          - interface [MGMT_INTERFACE]
          - ip address [MGMT_IP] [MGMT_MASK]
          - no shutdown

    - name: Save configuration
      ios_config:
        save_when: always
```

### Interface Configuration Playbook
```yaml
# playbooks/interfaces.yml
---
- name: Configure Interfaces
  hosts: all
  gather_facts: no
  tasks:
    - name: Configure interfaces
      ios_config:
        lines:
          - description [ITEM_DESCRIPTION]
          - ip address [ITEM_IP] [ITEM_MASK]
          - no shutdown
        parents: interface [ITEM_NAME]
      loop: "[INTERFACES]"
      when: interfaces is defined
```

### Routing Configuration Playbook
```yaml
# playbooks/routing.yml
---
- name: Configure OSPF
  hosts: routers
  gather_facts: no
  tasks:
    - name: Configure OSPF process
      ios_config:
        lines:
          - router ospf [OSPF_PROCESS]
          - router-id [ROUTER_ID]

    - name: Configure OSPF networks
      ios_config:
        lines:
          - network [ITEM_NETWORK] [ITEM_WILDCARD] area [ITEM_AREA]
        parents: router ospf [OSPF_PROCESS]
      loop: "[OSPF_NETWORKS]"
```

## Phase 5: Backup and Restore

### Configuration Backup Playbook
```yaml
# playbooks/backup.yml
---
- name: Backup Device Configurations
  hosts: all
  gather_facts: no
  tasks:
    - name: Gather device facts
      ios_facts:
        gather_subset: config

    - name: Save configuration to file
      copy:
        content: "{{{{ ansible_net_config }}}}"
        dest: "./backups/{{{{ inventory_hostname }}}}_{{{{ ansible_date_time.date }}}}.cfg"
      delegate_to: localhost
```

### Configuration Restore Playbook
```yaml
# playbooks/restore.yml
---
- name: Restore Device Configurations
  hosts: all
  gather_facts: no
  tasks:
    - name: Load configuration from file
      ios_config:
        src: "./backups/{{{{ inventory_hostname }}}}_latest.cfg"
        replace: config
```

## Phase 6: Compliance and Validation

### Security Compliance Check
```yaml
# playbooks/compliance.yml
---
- name: Security Compliance Check
  hosts: all
  gather_facts: no
  tasks:
    - name: Check for required security settings
      ios_command:
        commands:
          - show running-config | include service password-encryption
          - show running-config | include enable secret
          - show running-config | include login block-for
      register: security_check

    - name: Validate security settings
      assert:
        that:
          - "'service password-encryption' in security_check.stdout[0]"
          - "'enable secret' in security_check.stdout[1]"
        fail_msg: "Security settings not properly configured"
```

### Interface Status Validation
```yaml
# playbooks/validate.yml
---
- name: Validate Interface Status
  hosts: all
  gather_facts: no
  tasks:
    - name: Check interface status
      ios_command:
        commands:
          - show ip interface brief
      register: interface_status

    - name: Verify all interfaces are up
      assert:
        that:
          - "'down' not in interface_status.stdout[0]"
        fail_msg: "Some interfaces are down"
```

## Phase 7: Execution Scripts

### Main Automation Script
```bash
#!/bin/bash
# automation.sh

echo "Starting lab automation for {lab_name}..."

# Verify lab is running
echo "Checking lab status..."
eveng-mcp-server list-nodes --lab_path "/{lab_name}.unl"

# Start all nodes if needed
echo "Starting all nodes..."
eveng-mcp-server start-all-nodes --lab_path "/{lab_name}.unl"

# Wait for nodes to boot
echo "Waiting for nodes to boot..."
sleep 60

# Run basic configuration
echo "Applying basic configuration..."
ansible-playbook -i inventory.yml playbooks/basic_config.yml

# Configure interfaces
echo "Configuring interfaces..."
ansible-playbook -i inventory.yml playbooks/interfaces.yml

# Configure routing
echo "Configuring routing protocols..."
ansible-playbook -i inventory.yml playbooks/routing.yml

# Validate configuration
echo "Validating configuration..."
ansible-playbook -i inventory.yml playbooks/validate.yml

# Backup configurations
echo "Backing up configurations..."
ansible-playbook -i inventory.yml playbooks/backup.yml

echo "Lab automation complete!"
```

### Python Automation Script
```python
#!/usr/bin/env python3
# lab_automation.py

# Python automation script example
import subprocess
import time
import json
from netmiko import ConnectHandler

def run_eveng_command(command):
    # Execute EVE-NG MCP command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def configure_device(device_info, commands):
    # Configure device using Netmiko
    try:
        connection = ConnectHandler(**device_info)
        output = connection.send_config_set(commands)
        connection.save_config()
        connection.disconnect()
        return True, output
    except Exception as e:
        return False, str(e)

def main():
    # Start lab automation
    print("Starting lab automation...")

    # Check lab status and configure devices
    # [Implementation details here]

if __name__ == "__main__":
    main()
```

## Phase 8: Monitoring and Maintenance

### Health Check Script
```yaml
# playbooks/health_check.yml
---
- name: Lab Health Check
  hosts: all
  gather_facts: no
  tasks:
    - name: Check device uptime
      ios_command:
        commands: show version | include uptime
      register: uptime

    - name: Check memory usage
      ios_command:
        commands: show memory summary
      register: memory

    - name: Check CPU usage
      ios_command:
        commands: show processes cpu | include CPU
      register: cpu

    - name: Generate health report
      template:
        src: health_report.j2
        dest: "./reports/{{{{ inventory_hostname }}}}_health.txt"
      delegate_to: localhost
```

### Automated Testing
```yaml
# playbooks/connectivity_test.yml
---
- name: Connectivity Testing
  hosts: all
  gather_facts: no
  tasks:
    - name: Ping test to all neighbors
      ios_ping:
        dest: "{{{{ item }}}}"
        count: 5
      loop: "{{{{ ping_targets }}}}"
      register: ping_results

    - name: Verify routing table
      ios_command:
        commands: show ip route summary
      register: routing_summary
```

## Best Practices

### 1. Version Control
- Store all automation code in Git
- Use branching for different lab versions
- Tag releases for stable configurations

### 2. Testing
- Test automation in isolated environment
- Validate configurations before deployment
- Implement rollback procedures

### 3. Documentation
- Document all automation procedures
- Maintain configuration templates
- Keep inventory updated

### 4. Security
- Use encrypted credential storage
- Implement access controls
- Regular security audits

Your lab automation for {lab_name} using {automation_type} is now ready for deployment!
"""

        return [
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=content)
            )
        ]

    @mcp.prompt("analyze_lab_performance")
    async def analyze_lab_performance_prompt(
        lab_name: str = "performance_lab"
    ) -> List[PromptMessage]:
        """Performance analysis guidance for lab optimization."""

        content = f"""# Analyze Lab Performance: {lab_name}

## Overview
Comprehensive performance analysis workflow to optimize your EVE-NG lab for better resource utilization and performance.

## Performance Metrics
- CPU utilization per node
- Memory consumption
- Network throughput
- Disk I/O performance
- Boot times
- Response times

## Phase 1: Baseline Assessment

### 1. Lab Status Overview
```
Tool: get_lab_details
Parameters:
  lab_path: "/{lab_name}.unl"
```

### 2. Node Inventory and Status
```
Tool: list_nodes
Parameters:
  lab_path: "/{lab_name}.unl"
```

### 3. Resource Allocation Review
```
Tool: get_node_details
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "1"  # Repeat for each node
```

**Analyze for each node:**
- Allocated RAM vs. template requirements
- CPU allocation vs. workload
- Interface count vs. actual usage
- Image size and type

## Phase 2: System Resource Monitoring

### EVE-NG Server Performance
Check server-level metrics:

```bash
# CPU usage
top -p $(pgrep -f qemu)
htop

# Memory usage
free -h
cat /proc/meminfo

# Disk I/O
iostat -x 1
iotop

# Network statistics
iftop
netstat -i
```

### Node-Level Performance
For each running node:

```bash
# Check QEMU processes
ps aux | grep qemu
pstree -p $(pgrep qemu)

# Memory mapping
cat /proc/[PID]/status
cat /proc/[PID]/smaps

# CPU affinity
taskset -p [PID]
```

## Phase 3: Network Performance Analysis

### Topology Efficiency
```
Tool: get_lab_topology
Parameters:
  lab_path: "/{lab_name}.unl"
```

**Analyze:**
- Connection complexity
- Redundant paths
- Bottleneck identification
- Broadcast domains

### Network Utilization
```bash
# Interface statistics on nodes
show interfaces
show interfaces summary
show interfaces counters

# Traffic analysis
show ip traffic
show ip route summary
show arp statistics
```

### Bandwidth Testing
```bash
# Between lab nodes
iperf3 -s  # On target node
iperf3 -c [target_ip] -t 60  # On source node

# Throughput testing
ping -f [target_ip]  # Flood ping
ping -s 1472 [target_ip]  # Large packets
```

## Phase 4: Performance Optimization

### Node Resource Optimization

#### Memory Optimization
```
# Reduce RAM for underutilized nodes
Tool: stop_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"

# Edit node configuration (manual)
# Reduce RAM allocation
# Restart node

Tool: start_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"
```

#### CPU Optimization
```bash
# Set CPU affinity for QEMU processes
taskset -cp 0,1 [PID]  # Bind to specific cores

# Adjust CPU priority
nice -n -10 qemu-system-x86_64 [options]
renice -10 [PID]
```

### Network Optimization

#### Reduce Broadcast Traffic
```bash
# On switches
spanning-tree mode rapid-pvst
spanning-tree portfast default
spanning-tree portfast bpduguard default

# VLAN optimization
vlan 999
 name UNUSED
 shutdown
```

#### Interface Optimization
```bash
# Disable unused interfaces
interface range gi0/5-24
 shutdown

# Optimize interface settings
interface gi0/1
 speed 1000
 duplex full
 no negotiation auto
```

### Image Optimization

#### Use Optimized Images
- Prefer smaller image files
- Use compressed images when available
- Remove unnecessary features from images

#### Image Management
```bash
# Check image sizes
ls -lh /opt/unetlab/addons/qemu/

# Compress images
qemu-img convert -O qcow2 -c original.qcow2 compressed.qcow2

# Optimize existing images
qemu-img convert -O qcow2 old.qcow2 optimized.qcow2
```

## Phase 5: Performance Monitoring

### Automated Monitoring Script
```python
#!/usr/bin/env python3
# performance_monitor.py

import psutil
import time
import json
from datetime import datetime

def monitor_lab_performance(lab_name, duration=300):
    # Monitor lab performance for specified duration
    # Collect CPU, memory, disk, and network metrics
    # Save results to JSON file
    pass

if __name__ == "__main__":
    monitor_lab_performance("lab_name", 300)  # 5 minutes
```

### Real-time Dashboard
```bash
#!/bin/bash
# performance_dashboard.sh

while true; do
    clear
    echo "=== Lab Performance Dashboard: {lab_name} ==="
    echo "Timestamp: $(date)"
    echo

    # System resources
    echo "=== System Resources ==="
    echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{{print $2}}' | cut -d'%' -f1)%"
    echo "Memory: $(free | grep Mem | awk '{{printf "%.1f%%", $3/$2 * 100.0}}')"
    echo "Disk: $(df -h / | awk 'NR==2{{print $5}}')"
    echo

    # QEMU processes
    echo "=== Running Nodes ==="
    ps aux | grep qemu | grep -v grep | wc -l | xargs echo "Active nodes:"
    echo

    # Network interfaces
    echo "=== Network Activity ==="
    cat /proc/net/dev | grep -E "(virbr|tap)" | head -5
    echo

    sleep 5
done
```

## Phase 6: Performance Tuning

### EVE-NG Server Tuning

#### Kernel Parameters
```bash
# /etc/sysctl.conf optimizations
vm.swappiness=10
vm.dirty_ratio=15
vm.dirty_background_ratio=5
net.core.rmem_max=134217728
net.core.wmem_max=134217728
net.ipv4.tcp_rmem=4096 87380 134217728
net.ipv4.tcp_wmem=4096 65536 134217728

# Apply changes
sysctl -p
```

#### CPU Governor
```bash
# Set performance governor
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Check current governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

#### Huge Pages
```bash
# Enable huge pages
echo 1024 > /proc/sys/vm/nr_hugepages

# Verify huge pages
cat /proc/meminfo | grep Huge
```

### QEMU Optimization

#### QEMU Parameters
```bash
# Optimized QEMU startup
qemu-system-x86_64 \\
  -enable-kvm \\
  -cpu host \\
  -smp 2 \\
  -m 512 \\
  -machine type=pc,accel=kvm \\
  -netdev tap,id=net0,ifname=tap0,script=no \\
  -device virtio-net-pci,netdev=net0 \\
  -drive file=disk.qcow2,if=virtio,cache=writeback \\
  -nographic
```

#### KVM Optimization
```bash
# Check KVM support
lsmod | grep kvm
cat /proc/cpuinfo | grep vmx

# Optimize KVM
echo 1 > /sys/module/kvm/parameters/ignore_msrs
echo Y > /sys/module/kvm_intel/parameters/nested
```

## Phase 7: Performance Reporting

### Performance Report Template
```python
# generate_report.py

def generate_performance_report(lab_name, metrics):
    # Generate performance analysis report
    # Include CPU, memory, disk, and network metrics
    # Provide optimization recommendations
    return "Performance report generated"
```

### Automated Optimization
```bash
#!/bin/bash
# auto_optimize.sh

echo "Starting automatic optimization for {lab_name}..."

# Stop all nodes
eveng-mcp-server stop-all-nodes --lab_path "/{lab_name}.unl"

# Optimize system settings
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
echo 1024 > /proc/sys/vm/nr_hugepages

# Restart nodes with optimizations
eveng-mcp-server start-all-nodes --lab_path "/{lab_name}.unl"

echo "Optimization complete!"
```

## Best Practices

### 1. Regular Monitoring
- Schedule performance reviews
- Set up alerting for resource thresholds
- Maintain performance baselines

### 2. Capacity Planning
- Plan for peak usage scenarios
- Monitor growth trends
- Scale infrastructure proactively

### 3. Optimization Cycles
- Test optimizations in isolation
- Measure before and after performance
- Document all changes

### 4. Resource Management
- Right-size node allocations
- Use appropriate image types
- Optimize network topology

Your performance analysis for {lab_name} is now complete with actionable optimization recommendations!
"""

        return [
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=content)
            )
        ]

    @mcp.prompt("debug_node_issues")
    async def debug_node_issues_prompt(
        lab_name: str = "debug_lab",
        node_name: str = "R1",
        issue_type: str = "boot_failure"
    ) -> List[PromptMessage]:
        """Node-specific problem solving and debugging workflow."""

        content = f"""# Debug Node Issues: {node_name} in {lab_name}

## Overview
Systematic approach to diagnosing and resolving node-specific issues in EVE-NG labs.

## Issue Type: {issue_type}
Targeted troubleshooting for {node_name} experiencing {issue_type}.

## Phase 1: Initial Assessment

### 1. Check Lab Status
```
Tool: get_lab_details
Parameters:
  lab_path: "/{lab_name}.unl"
```

### 2. Node Status Check
```
Tool: list_nodes
Parameters:
  lab_path: "/{lab_name}.unl"
```

### 3. Detailed Node Information
```
Tool: get_node_details
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"  # Replace with actual node ID for {node_name}
```

**Check for:**
- Current node status (stopped, starting, running, stopping)
- Resource allocation (RAM, CPU)
- Template and image information
- Interface configuration
- Position and connectivity

## Phase 2: Common Issue Diagnosis

### Issue: Node Won't Start

#### Symptoms
- Node stuck in "starting" state
- Node immediately returns to "stopped"
- Boot process hangs

#### Diagnostic Steps
```bash
# Check EVE-NG logs
tail -f /opt/unetlab/data/Logs/unl_wrapper.txt
tail -f /var/log/syslog | grep qemu

# Check available resources
free -h
df -h /opt/unetlab/tmp

# Verify image integrity
ls -la /opt/unetlab/addons/qemu/{node_name}/
qemu-img check /opt/unetlab/addons/qemu/{node_name}/[image_file]
```

#### Solutions
1. **Insufficient Resources**
```
Tool: stop_all_nodes
Parameters:
  lab_path: "/{lab_name}.unl"

# Reduce RAM allocation for {node_name}
# Edit node configuration manually
# Restart node

Tool: start_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"
```

2. **Corrupted Image**
```bash
# Re-download or restore image
cd /opt/unetlab/addons/qemu/{node_name}/
mv corrupted_image.qcow2 corrupted_image.qcow2.bak
# Restore from backup or re-download
```

3. **Template Issues**
```bash
# Check template configuration
cat /opt/unetlab/html/templates/{node_name}.yml

# Verify template syntax
python3 -c "import yaml; yaml.safe_load(open('/opt/unetlab/html/templates/{node_name}.yml'))"
```

### Issue: Node Boots But Unreachable

#### Symptoms
- Node shows "running" status
- Cannot access console
- No network connectivity

#### Diagnostic Steps
```bash
# Check QEMU process
ps aux | grep {node_name}
netstat -tlnp | grep [qemu_pid]

# Check console port
telnet localhost [console_port]

# Verify network interfaces
ip link show | grep tap
brctl show
```

#### Solutions
1. **Console Access Issues**
```bash
# Check console configuration
grep -r {node_name} /opt/unetlab/data/Logs/

# Restart node with console debugging
Tool: stop_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"

Tool: start_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"
```

2. **Network Interface Problems**
```bash
# Check bridge configuration
brctl show vunl0_X_Y

# Verify TAP interfaces
ip tuntap list | grep tap

# Reset network configuration
systemctl restart networking
```

### Issue: Node Performance Problems

#### Symptoms
- Slow boot times
- High CPU usage
- Memory exhaustion
- Unresponsive console

#### Diagnostic Steps
```bash
# Monitor node resources
top -p $(pgrep -f {node_name})
iotop -p $(pgrep -f {node_name})

# Check memory allocation
cat /proc/$(pgrep -f {node_name})/status | grep Vm

# Monitor disk I/O
iostat -x 1 | grep $(df /opt/unetlab/tmp | tail -1 | awk '{{print $1}}' | sed 's|/dev/||')
```

#### Solutions
1. **Resource Optimization**
```
# Reduce resource allocation
Tool: stop_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"

# Edit node configuration:
# - Reduce RAM if over-allocated
# - Adjust CPU count
# - Optimize image type

Tool: start_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"
```

2. **Image Optimization**
```bash
# Convert to optimized format
qemu-img convert -O qcow2 -c original.qcow2 optimized.qcow2

# Reduce image size
qemu-img resize optimized.qcow2 -1G
```

## Phase 3: Advanced Debugging

### QEMU Process Analysis
```bash
# Get detailed process information
ps -eo pid,ppid,cmd,etime,time,pcpu,pmem | grep {node_name}

# Check process limits
cat /proc/$(pgrep -f {node_name})/limits

# Monitor system calls
strace -p $(pgrep -f {node_name}) -e trace=network,file

# Check file descriptors
lsof -p $(pgrep -f {node_name})
```

### Memory Analysis
```bash
# Check memory mapping
cat /proc/$(pgrep -f {node_name})/smaps | grep -E "(Size|Rss|Pss)"

# Monitor memory usage over time
while true; do
  echo "$(date): $(cat /proc/$(pgrep -f {node_name})/status | grep VmRSS)"
  sleep 5
done
```

### Network Debugging
```bash
# Capture network traffic
tcpdump -i vunl0_X_Y -w {node_name}_capture.pcap

# Check ARP tables
arp -a | grep [node_ip]

# Verify routing
ip route show table all | grep vunl
```

## Phase 4: Configuration Recovery

### Backup and Restore
```
# Create node backup before changes
Tool: stop_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"

# Backup node configuration
cp -r /opt/unetlab/tmp/X/Y/{node_name}/ /backup/

# Restore from backup if needed
rm -rf /opt/unetlab/tmp/X/Y/{node_name}/
cp -r /backup/{node_name}/ /opt/unetlab/tmp/X/Y/

Tool: start_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"
```

### Factory Reset
```
# Wipe node to factory state
Tool: wipe_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"

# Restart with clean configuration
Tool: start_node
Parameters:
  lab_path: "/{lab_name}.unl"
  node_id: "X"
```

## Phase 5: Preventive Measures

### Health Monitoring Script
```python
#!/usr/bin/env python3
# node_health_monitor.py

import subprocess
import time
import json
from datetime import datetime

def check_node_health(lab_name, node_id):
    # Monitor node health metrics

    health_data = {{
        'timestamp': datetime.now().isoformat(),
        'node_id': node_id,
        'status': 'unknown',
        'cpu_usage': 0,
        'memory_usage': 0,
        'console_accessible': False,
        'network_reachable': False
    }}

    try:
        # Check node status via MCP
        result = subprocess.run([
            'eveng-mcp-server', 'get-node-details',
            '--lab_path', f'/{lab_name}.unl',
            '--node_id', node_id
        ], capture_output=True, text=True)

        if result.returncode == 0:
            # Parse node status
            # Update health_data based on response
            pass

    except Exception as e:
        health_data['error'] = str(e)

    return health_data

def main():
    lab_name = "{lab_name}"
    node_id = "X"  # Replace with actual node ID

    while True:
        health = check_node_health(lab_name, node_id)

        # Log health data
        with open(f'{{lab_name}}_{{node_id}}_health.log', 'a') as f:
            f.write(json.dumps(health) + '\\n')

        # Alert on issues
        if health.get('status') != 'running':
            print(f"ALERT: Node {{node_id}} status: {{health.get('status')}}")

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
```

### Automated Recovery
```bash
#!/bin/bash
# auto_recovery.sh

NODE_ID="X"
LAB_PATH="/{lab_name}.unl"
MAX_RETRIES=3

check_node_status() {{
    eveng-mcp-server get-node-details --lab_path "$LAB_PATH" --node_id "$NODE_ID" | grep -q "running"
}}

restart_node() {{
    echo "Restarting node $NODE_ID..."
    eveng-mcp-server stop-node --lab_path "$LAB_PATH" --node_id "$NODE_ID"
    sleep 10
    eveng-mcp-server start-node --lab_path "$LAB_PATH" --node_id "$NODE_ID"
}}

# Main recovery loop
for i in $(seq 1 $MAX_RETRIES); do
    if check_node_status; then
        echo "Node $NODE_ID is healthy"
        exit 0
    else
        echo "Node $NODE_ID unhealthy, attempt $i/$MAX_RETRIES"
        restart_node
        sleep 30
    fi
done

echo "Failed to recover node $NODE_ID after $MAX_RETRIES attempts"
exit 1
```

## Phase 6: Documentation and Reporting

### Issue Report Template
```markdown
# Node Issue Report: {node_name}

## Issue Summary
- **Lab**: {lab_name}
- **Node**: {node_name}
- **Issue Type**: {issue_type}
- **Severity**: [High/Medium/Low]
- **Date**: [CURRENT_DATE]

## Symptoms Observed
- [List specific symptoms]
- [Include error messages]
- [Note timing of issues]

## Diagnostic Results
- **Node Status**: [Current status]
- **Resource Usage**: [CPU/Memory/Disk]
- **Log Entries**: [Relevant log excerpts]

## Root Cause Analysis
- **Primary Cause**: [Identified cause]
- **Contributing Factors**: [Additional factors]
- **Impact Assessment**: [Scope of impact]

## Resolution Steps
1. [Step 1 taken]
2. [Step 2 taken]
3. [Final resolution]

## Prevention Measures
- [Preventive actions implemented]
- [Monitoring improvements]
- [Process changes]

## Lessons Learned
- [Key insights]
- [Process improvements]
- [Documentation updates]
```

### Best Practices

#### 1. Systematic Approach
- Follow structured debugging methodology
- Document all steps and findings
- Test solutions in isolation

#### 2. Resource Management
- Monitor resource usage regularly
- Right-size node allocations
- Plan for peak usage scenarios

#### 3. Backup Strategy
- Regular configuration backups
- Image versioning
- Recovery procedures tested

#### 4. Monitoring and Alerting
- Automated health checks
- Proactive issue detection
- Performance trending

Your debugging workflow for {node_name} in {lab_name} is now complete with comprehensive troubleshooting procedures!
"""

        return [
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=content)
            )
        ]
