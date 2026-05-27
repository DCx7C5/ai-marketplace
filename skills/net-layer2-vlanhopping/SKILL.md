---
name: net-layer2-vlanhopping
description: "--| | DTP Switch Spoofing | All VLANs | VULNERABLE | Full trunk access gained | | Double Tagging | VLAN 50 | VULNERABLE | Unidirectional access to CDE | | VTP Injection | N/A | NOT VULNERABLE | VTP transparent mode |  ### Root Causes 1."
domain: cybersecurity
---

--|
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
