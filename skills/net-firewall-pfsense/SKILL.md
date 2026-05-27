---
name: net-firewall-pfsense
description: - Deploying a perimeter or internal firewall to segment and protect network zones (DMZ, internal, guest, IoT) - Creating granular access control rules to restrict traffic between VLANs and network segments - Configuring NAT rules for port forwarding to internal services exposed to the internet - Setting up site-to-site or remote access VPN tunnels 
domain: cybersecurity
---
---|------------|
| **Stateful Firewall** | Firewall that tracks the state of network connections and automatically allows return traffic for established sessions without explicit rules |
| **Alias** | Named group of IP addresses, networks, or ports in pfSense that simplifies rule management and improves readability |
| **NAT (Network Address Translation)** | Translation of IP addresses between internal and external networks, including port forwarding for inbound access to internal services |
| **Floating Rules** | pfSense rules that apply across multiple interfaces simultaneously, processed before per-interface rules |
| **pfBlockerNG** | pfSense package that integrates IP reputation blocklists and DNS-based blocklists for automated threat blocking |
| **Rule Processing Order** | pfSense evaluates rules top-to-bottom within each interface tab; first match wins, and unmatched traffic is blocked by default |

## Tools & Systems

- **pfSense 2.7+**: Open-source firewall and router platform based on FreeBSD with web-based management and extensive package ecosystem
- **pfBlockerNG**: IP and DNS blocklist package for automated threat intelligence integration
- **Snort/Suricata packages**: IDS/IPS integration available as pfSense packages for inline traffic inspection
- **OpenVPN/IPsec**: Built-in VPN implementations for site-to-site and remote access connectivity
- **Netgate AutoConfigBackup**: Cloud-based configuration backup service for pfSense disaster recovery

## Common Scenarios

### Scenario: Segmenting a Small Business Network with pfSense

**Context**: A medical practice needs to segment its network to meet HIPAA requirements. They have a single internet connection, an electronic health records (EHR) server, staff workstations, a guest WiFi network, and medical IoT devices (vitals monitors, imaging equipment). Budget constraints require an open-source solution.

**Approach**:
1. Deploy pfSense on a Netgate 4100 appliance with four physical interfaces (WAN, LAN, DMZ, MGMT)
2. Create VLANs for staff (VLAN 10), EHR servers (VLAN 20), guest WiFi (VLAN 30), and medical devices (VLAN 40)
3. Configure strict rules: staff VLAN can access EHR servers on HTTPS only; medical devices can communicate only with the EHR server on specific ports; guest WiFi gets internet-only access with no internal routing
4. Enable pfBlockerNG with healthcare-specific threat feeds and malware domain blocking
5. Configure outbound NAT to prevent internal IP addresses from leaking to the internet
6. Enable comprehensive logging and forward all firewall logs to a SIEM via syslog
7. Set up automated configuration backups and document the rule base for audit compliance

**Pitfalls**:
- Creating rules that are too permissive ("allow any any") instead of specific port-based rules
- Forgetting the rule processing order -- placing a broad PASS rule above a specific BLOCK rule
- Not enabling logging on critical rules, making incident investigation impossible
- Allowing IoT devices unrestricted internet access, creating potential data exfiltration paths

## Output Format

```
## pfSense Firewall Configuration Report

**Device**: pfSense 2.7.2 on Netgate 4100
**Interfaces**: WAN (igb0), LAN (igb1), DMZ (igb2), MGMT (igb3)
**VLANs**: 4 configured (Staff, Servers, Guest, IoT)
**Total Rules**: 28 active rules across all interfaces

### Rule Summary by Interface

| Interface | Pass Rules | Block Rules | Logging Enabled |
|-----------|-----------|-------------|-----------------|
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