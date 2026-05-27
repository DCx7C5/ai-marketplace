---
name: net-firewall-pfsense
description: "Net Firewall Pfsense."
domain: cybersecurity
---

--|
| WAN | 2 | 1 (default) | Yes |
| LAN | 4 | 2 | Yes (blocks) |
| DMZ | 3 | 1 (default) | Yes |
| GUEST | 1 | 2 | Yes |
| IOT | 1 | 3 | Yes |

### Security Controls
- pfBlockerNG: 12 IP blocklists + DNSBL enabled
- Snort IDS: Running on WAN and LAN interfaces
- VPN: OpenVPN remote access configured with MFA
- Logging: All traffic forwarded to SIEM (10.10.20.15)
```
