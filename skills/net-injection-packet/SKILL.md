---
name: net-injection-packet
description: - Testing IDS/IPS rules by injecting traffic that should trigger specific detection signatures - Validating firewall rules by crafting packets with specific flags, source addresses, and payloads - Assessing network stack resilience to malformed packets, fragmentation attacks, and protocol violations - Simulating spoofed traffic to test anti-spoofin
domain: cybersecurity
---
---|------------|
| **Packet Injection** | Crafting and sending network packets with specific header values, payloads, or flag combinations to test network security controls |
| **IP Spoofing** | Setting a false source IP address in crafted packets to test anti-spoofing controls (BCP38, uRPF) or impersonate another host |
| **TCP RST Injection** | Sending forged TCP RST packets to terminate established connections, testing session resilience and connection reset defenses |
| **Fragmentation Attack** | Exploiting IP fragmentation to split malicious payloads across fragments, evading packet inspection that does not reassemble fragments |
| **uRPF (Unicast Reverse Path Forwarding)** | Router-level anti-spoofing mechanism that drops packets if the source IP would not be routable back through the ingress interface |
| **BCP38 (Network Ingress Filtering)** | Best Current Practice for preventing IP spoofing at network borders by filtering packets with source addresses not belonging to the network |

## Tools & Systems

- **Scapy**: Python packet manipulation library for crafting arbitrary network packets with full control over all protocol headers
- **hping3**: Command-line packet generator supporting TCP, UDP, ICMP with control over flags, TTL, window size, and packet rate
- **Nemesis**: Network packet injection tool supporting Ethernet, ARP, IP, TCP, UDP, ICMP, DNS, and other protocols
- **tcpreplay**: Tool for replaying captured PCAP files at controlled rates for testing IDS rules against known traffic patterns
- **Nping**: Nmap's packet generation tool for crafting probes with arbitrary TCP/UDP/ICMP headers

## Common Scenarios

### Scenario: Validating IDS Rules After Deployment

**Context**: A SOC team deployed new Suricata rules for detecting reconnaissance and evasion techniques. They need to validate that the rules trigger correctly before going live. The testing is performed in a staging environment replicating the production network.

**Approach**:
1. Craft XMAS, NULL, and FIN scan packets using Scapy and send to test targets to verify scan detection rules
2. Generate packets with invalid TCP flag combinations (SYN+FIN, SYN+RST) to test protocol anomaly rules
3. Send oversized ICMP packets and fragmented payloads to test fragmentation detection rules
4. Inject packets with spoofed source IPs to verify anti-spoofing rules fire correctly
5. Send TCP RST injection packets during an active HTTP session to test session disruption detection
6. Verify that all expected Suricata alerts appear in the EVE JSON log with correct severity and metadata
7. Document which rules fired, which did not, and recommend rule tuning for any gaps

**Pitfalls**:
- Sending injection packets too fast and overwhelming the test network or IDS sensor
- Crafting packets with incorrect checksum calculations, causing them to be silently dropped before reaching the IDS
- Not accounting for stateful firewalls that drop out-of-state packets before they reach the IDS for inspection
- Testing from behind a NAT that modifies source ports and breaks crafted TCP sequences

## Output Format

```
## Packet Injection Test Report

**Target**: 10.10.20.10 (test-server-01)
**IDS Sensor**: suricata-staging-01
**Test Date**: 2024-03-15

### Test Matrix

| Test | Packet Type | Expected Detection | Actual Result |
|------|-------------|-------------------|---------------|
| 1 | TCP XMAS Scan | SID 2100330 | DETECTED |
| 2 | TCP NULL Scan | SID 2100331 | DETECTED |
| 3 | SYN+FIN Invalid | SID 2100332 | DETECTED |
| 4 | IP Spoofed Source | SID 2003000 | DETECTED |
| 5 | Land Attack | SID 2100333 | NOT DETECTED |
| 6 | Fragment Overlap | SID 2200001 | DETECTED |
| 7 | Ping of Death | SID 2100334 | DETECTED |
| 8 | TCP RST Injection | Custom SID | NOT DETECTED |

### Detection Rate: 6/8 (75%)

### Gaps Identified
1. Land attack (src==dst) not detected -- add rule SID 2100333
2. TCP RST injection not detected -- create custom rule for out-of-window RST
```