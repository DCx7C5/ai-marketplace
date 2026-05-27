---
name: net-layer3-ipv6
description: - Testing whether dual-stack networks have consistent security controls for both IPv4 and IPv6 traffic - Demonstrating risks from unmanaged IPv6 on networks where only IPv4 is officially supported - Exploiting SLAAC and Router Advertisement mechanisms to perform man-in-the-middle attacks via IPv6 - Testing IPv6-aware firewall rules and IDS/IPS dete
domain: cybersecurity
---
---|------------|
| **SLAAC (Stateless Address Autoconfiguration)** | IPv6 mechanism where hosts automatically configure addresses from Router Advertisements without a DHCP server, exploitable by rogue RA injection |
| **Router Advertisement (RA)** | ICMPv6 message from routers announcing network prefixes, default gateway, and DNS configuration; rogue RAs enable MITM attacks |
| **NDP (Neighbor Discovery Protocol)** | IPv6 replacement for ARP that uses ICMPv6 for address resolution, router discovery, and duplicate address detection; vulnerable to spoofing |
| **mitm6** | Tool that exploits Windows DHCPv6 preference to become the IPv6 DNS server, enabling DNS spoofing and NTLM credential relay |
| **RA Guard** | Switch-level security feature that filters rogue Router Advertisements, preventing unauthorized hosts from acting as IPv6 routers |
| **IPv6 Tunneling** | Encapsulation of IPv6 packets within IPv4 (6to4, Teredo, ISATAP) that can bypass IPv4-only security controls and firewalls |

## Tools & Systems

- **mitm6**: IPv6 MITM tool that exploits SLAAC and DHCPv6 to become the DNS server for Windows hosts
- **THC-IPv6 Toolkit**: Comprehensive IPv6 attack toolkit including alive6, parasite6, fake_router6, and flood tools
- **Scapy**: Python packet manipulation for crafting custom ICMPv6 Router Advertisements and Neighbor Discovery packets
- **ndpmon**: IPv6 Neighbor Discovery Protocol monitor that detects rogue RAs and NDP spoofing
- **Nmap**: Network scanner with full IPv6 support including multicast discovery and IPv6-specific scripts

## Common Scenarios

### Scenario: Exploiting Unmanaged IPv6 on an IPv4-Only Enterprise Network

**Context**: A company officially only uses IPv4 on their corporate network, but Windows workstations have IPv6 enabled by default. During an internal penetration test, the tester discovers that IPv6 is active on the VLAN and no IPv6 security controls (RA Guard, IPv6 ACLs) are deployed.

**Approach**:
1. Discover that all Windows workstations have link-local IPv6 addresses and are listening for Router Advertisements
2. Run mitm6 to send DHCPv6 responses, becoming the IPv6 DNS server for all Windows hosts on the VLAN
3. Configure ntlmrelayx to relay WPAD-triggered NTLM authentication to the domain controller
4. Within 5 minutes, capture and relay NTLM credentials from 12 workstations, gaining access to file shares
5. Successfully relay a domain admin's NTLM hash to create a new domain admin account
6. Document that the lack of IPv6 security controls enabled full domain compromise without exploiting any traditional vulnerability
7. Recommend disabling IPv6 where not needed, deploying RA Guard on switches, and blocking DHCPv6 at the firewall

**Pitfalls**:
- Flooding the network with Router Advertisements can cause instability on some devices
- mitm6 affects all Windows hosts on the VLAN, not just the target -- ensure scope covers all potentially affected hosts
- Some environments have IPv6-dependent services (SCCM, certain Azure services) that break when IPv6 is disrupted
- Forgetting to check for IPv6 tunneling protocols that could provide alternative attack paths

## Output Format

```
## IPv6 Security Assessment Report

**Test ID**: IPV6-2024-001
**Target Network**: VLAN 10 (10.10.10.0/24, no official IPv6)
**Assessment Date**: 2024-03-15

### IPv6 Discovery

| Finding | Details |
|---------|---------|
| IPv6 Enabled Hosts | 147/150 workstations (Windows default) |
| Link-Local Addresses | Active on all discovered hosts |
| Router Advertisements | None detected (no IPv6 router) |
| DHCPv6 Server | None present |
| RA Guard | NOT configured on switches |
| IPv6 Firewall Rules | NONE (ip6tables empty) |

### Attack Results

| Attack | Result | Impact |
|--------|--------|--------|
| mitm6 DNS Takeover | SUCCESS | Became IPv6 DNS for 147 hosts |
| WPAD NTLM Relay | SUCCESS | Captured 23 NTLM authentications |
| Domain Admin Relay | SUCCESS | Created rogue domain admin account |
| IPv6 Port Scan | SUCCESS | All ports open (no ip6tables rules) |

### Recommendations
1. Deploy RA Guard on all access-layer switches (Critical)
2. Configure IPv6 ACLs mirroring IPv4 firewall rules (Critical)
3. Disable DHCPv6 client via Group Policy where IPv6 is not needed
4. Block IPv6 tunneling protocols (6to4, Teredo) at the firewall
5. Deploy IPv6-aware IDS rules for NDP spoofing detection
```