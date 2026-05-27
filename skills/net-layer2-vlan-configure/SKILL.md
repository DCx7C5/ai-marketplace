---
name: net-layer2-vlan-configure
description: - Segmenting an enterprise network into isolated security zones (corporate, servers, DMZ, guest, IoT) - Meeting compliance requirements (PCI-DSS, HIPAA, SOC 2) that mandate network isolation for sensitive data - Reducing blast radius of security incidents by preventing lateral movement between network segments - Isolating high-risk devices (IoT, BY
domain: cybersecurity
---
---|------------|
| **VLAN (Virtual LAN)** | Logical network partition at Layer 2 that groups switch ports into isolated broadcast domains, regardless of physical location |
| **802.1Q Trunking** | IEEE standard for VLAN tagging that adds a 4-byte header to Ethernet frames, identifying which VLAN a frame belongs to across trunk links |
| **Inter-VLAN Routing** | Layer 3 forwarding of traffic between VLANs using a router, Layer 3 switch, or firewall with access control lists |
| **Native VLAN** | VLAN assigned to untagged frames on trunk ports; should be set to an unused VLAN to prevent VLAN hopping attacks |
| **DHCP Snooping** | Switch feature that validates DHCP messages and builds a binding table of IP-MAC-port mappings, preventing rogue DHCP servers |
| **Port Security** | Switch feature that limits the number of MAC addresses per port and takes action (shutdown, restrict) when violated |

## Tools & Systems

- **Cisco Catalyst/Nexus**: Enterprise managed switches with comprehensive VLAN, trunking, and security feature support
- **HP Aruba CX**: Enterprise switches with REST API management and VLAN segmentation capabilities
- **pfSense/OPNsense**: Open-source firewalls for inter-VLAN routing with stateful access control
- **NetBox**: Open-source IPAM and DCIM tool for documenting VLAN assignments, IP addressing, and network topology
- **Nmap**: Network scanner for verifying segmentation effectiveness by testing reachability across VLAN boundaries

## Common Scenarios

### Scenario: Implementing PCI-DSS Compliant Network Segmentation for Retail

**Context**: A retail chain must isolate their payment card processing systems from the general corporate network to meet PCI-DSS requirements. The current flat network has point-of-sale terminals, employee workstations, inventory servers, and guest WiFi on a single VLAN. The environment uses Cisco Catalyst 9300 switches.

**Approach**:
1. Design VLAN architecture: POS terminals on VLAN 50 (CDE), corporate on VLAN 10, servers on VLAN 20, guest on VLAN 40
2. Create VLANs on all access-layer switches and configure access ports by function
3. Configure trunk links between switches with explicit VLAN allowed lists (no "all" trunks)
4. Set native VLAN to 998 (unused) on all trunks and disable DTP on every port
5. Configure ACLs on the Layer 3 switch: CDE VLAN can only reach the payment processor's IP on port 443; no other inter-VLAN traffic to/from CDE
6. Enable DHCP snooping, DAI, and port security on all access ports
7. Verify segmentation with penetration testing from each VLAN, confirming CDE is fully isolated

**Pitfalls**:
- Leaving DTP enabled on access ports, allowing VLAN hopping to reach the CDE
- Using VLAN 1 as the native VLAN, enabling double-tagging attacks
- Not restricting trunk allowed VLANs, carrying all VLANs including CDE to non-essential switches
- Creating ACLs that allow "any" source to reach CDE servers instead of specific POS terminal IPs

## Output Format

```
## Network Segmentation Implementation Report

**Network**: Retail Store #42
**Switch Platform**: Cisco Catalyst 9300
**VLANs Configured**: 8

### VLAN Summary

| VLAN ID | Name | Subnet | Ports | Purpose |
|---------|------|--------|-------|---------|
| 10 | CORPORATE | 10.10.10.0/24 | Gi1/0/1-24 | Employee workstations |
| 20 | SERVERS | 10.10.20.0/24 | Gi1/0/25-36 | Internal servers |
| 30 | DMZ | 10.10.30.0/24 | Gi2/0/1-4 | Internet-facing |
| 40 | GUEST | 10.10.40.0/24 | WiFi AP trunk | Guest WiFi |
| 50 | CDE | 10.10.50.0/24 | Gi2/0/5-12 | POS terminals |
| 100 | MGMT | 10.10.100.0/24 | Gi1/0/48 | Switch management |
| 998 | NATIVE | N/A | Trunks only | Unused native |
| 999 | QUARANTINE | 10.10.99.0/24 | Unused ports | Isolation |

### Security Hardening Status

| Control | Status |
|---------|--------|
| DTP Disabled (nonegotiate) | All ports |
| Native VLAN (998) | All trunks |
| DHCP Snooping | VLANs 10,20,40,50 |
| Dynamic ARP Inspection | VLANs 10,20,40,50 |
| Port Security | Access ports |
| BPDU Guard | Access ports |
| Unused Ports Shutdown | 10 ports in VLAN 999 |
| VTP Transparent Mode | Enabled |
```