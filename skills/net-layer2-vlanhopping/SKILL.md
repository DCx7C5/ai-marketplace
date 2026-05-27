---
name: net-layer2-vlanhopping
description: - Testing the effectiveness of VLAN-based network segmentation during authorized penetration tests - Validating that switch trunk port configurations prevent unauthorized VLAN access - Assessing whether 802.1Q tagging and native VLAN configurations resist double-tagging attacks - Demonstrating to network teams why proper switch hardening is critica
domain: cybersecurity
---
---|------------|
| **VLAN Hopping** | Layer 2 attack technique that allows an attacker to access traffic on VLANs they are not authorized to reach, bypassing network segmentation |
| **DTP (Dynamic Trunking Protocol)** | Cisco proprietary protocol that automatically negotiates trunk links between switches; vulnerable to spoofing when not disabled on access ports |
| **Double Tagging** | Attack that encapsulates a frame with two 802.1Q tags, exploiting the switch's native VLAN processing to forward the inner-tagged frame to a different VLAN |
| **Native VLAN** | VLAN assigned to untagged frames on a trunk port; misconfigurations where the native VLAN matches a user VLAN enable double-tagging attacks |
| **VTP (VLAN Trunking Protocol)** | Cisco protocol for propagating VLAN database changes across switches; in server mode, a rogue VTP message with higher revision can overwrite the VLAN database |
| **802.1Q** | IEEE standard for VLAN tagging that inserts a 4-byte tag into Ethernet frames to identify VLAN membership across trunk links |

## Tools & Systems

- **Yersinia**: Layer 2 attack framework supporting DTP, VTP, STP, CDP, DHCP, and 802.1Q attacks with both GUI and CLI modes
- **Scapy**: Python packet manipulation library for crafting custom 802.1Q double-tagged frames and DTP negotiation packets
- **frogger**: VLAN hopping tool that automates native VLAN discovery and double-tagging attacks
- **Wireshark**: Packet analyzer for verifying VLAN tag contents and confirming frame delivery to target VLANs
- **tcpdump**: Command-line capture tool for monitoring 802.1Q tagged frames and DTP/VTP protocol traffic

## Common Scenarios

### Scenario: Testing VLAN Segmentation in a PCI-DSS Cardholder Data Environment

**Context**: A retailer needs to verify that their cardholder data environment (CDE) on VLAN 50 is properly isolated from the corporate network (VLAN 10) and guest WiFi (VLAN 30). The network uses Cisco Catalyst switches with 802.1Q trunking. The assessment is authorized to test from a port on VLAN 10.

**Approach**:
1. Connect to an access port on VLAN 10 and listen for DTP frames to determine trunk negotiation status
2. Send DTP desirable frames using Yersinia -- the port successfully negotiates a trunk because DTP was not disabled
3. Create a VLAN 50 subinterface and attempt to reach CDE systems (10.10.50.0/24) -- successful, demonstrating segmentation bypass
4. Attempt double tagging from VLAN 1 (native VLAN) to VLAN 50 -- also successful because native VLAN is VLAN 1
5. Document that VLAN segmentation fails as a PCI-DSS control due to DTP misconfiguration
6. Recommend disabling DTP on all access ports, changing native VLAN to an unused VLAN, and enabling port security

**Pitfalls**:
- DTP spoofing can cause spanning-tree topology changes that disrupt network connectivity
- Double tagging may not work if the native VLAN is not VLAN 1 or if the switch is configured properly
- VTP attacks in a production environment can delete VLANs across the entire switching domain, causing widespread outages
- Forgetting to remove VLAN subinterfaces after testing, leaving unauthorized VLAN access available

## Output Format

```
## VLAN Hopping Assessment Report

**Test ID**: VLAN-HOP-2024-001
**Switch Under Test**: Core-SW1 (Cisco Catalyst 9300)
**Attacker Port**: Gi1/0/24 (VLAN 10)
**Target VLANs**: VLAN 20 (Servers), VLAN 50 (CDE)

### Test Results

| Attack | Target VLAN | Result | Impact |
|--------|-------------|--------|--------|
| DTP Switch Spoofing | All VLANs | VULNERABLE | Full trunk access gained |
| Double Tagging | VLAN 50 | VULNERABLE | Unidirectional access to CDE |
| VTP Injection | N/A | NOT VULNERABLE | VTP transparent mode |

### Root Causes
1. DTP not disabled on access port Gi1/0/24 (Administrative mode: dynamic auto)
2. Native VLAN is VLAN 1 (default) on all trunk links
3. Unused ports not shutdown on the switch

### Remediation
1. Disable DTP on all access ports: `switchport nonegotiate`
2. Set all access ports to static mode: `switchport mode access`
3. Change native VLAN to unused VLAN: `switchport trunk native vlan 999`
4. Shutdown all unused ports: `shutdown`
5. Enable port security on access ports
6. Set VTP to transparent mode on all switches
```