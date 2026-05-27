---
name: net-layer2-arp-poison
description: - Testing whether network switches and infrastructure properly implement Dynamic ARP Inspection (DAI) - Demonstrating man-in-the-middle attack risks to stakeholders during authorized security assessments - Validating that network monitoring tools (IDS/IPS, SIEM) detect ARP cache poisoning attempts - Assessing the effectiveness of port security, 802
domain: cybersecurity
---
---|------------|
| **ARP Cache Poisoning** | Technique of sending fraudulent ARP replies to associate the attacker's MAC address with another host's IP address in the target's ARP cache |
| **Gratuitous ARP** | ARP reply sent without a corresponding request, used by ARP spoofing tools to update a target's ARP cache with false entries |
| **Dynamic ARP Inspection (DAI)** | Switch-level security feature that validates ARP packets against the DHCP snooping binding database and drops invalid ARP traffic |
| **IP Forwarding** | Kernel-level setting that allows a host to relay packets between network interfaces, required for transparent man-in-the-middle interception |
| **DHCP Snooping** | Switch security feature that builds a trusted binding table of IP-to-MAC-to-port mappings, serving as the foundation for DAI validation |

## Tools & Systems

- **arpspoof (dsniff suite)**: Simple command-line tool that sends continuous spoofed ARP replies to redirect traffic between two targets
- **Ettercap**: Comprehensive suite for man-in-the-middle attacks supporting ARP spoofing, DNS spoofing, content filtering, and credential capture
- **Scapy**: Python packet manipulation library for crafting custom ARP packets with full control over all header fields
- **arp-scan**: Network scanning tool that sends ARP requests to discover all hosts on a local network segment
- **Wireshark**: Packet analyzer for verifying ARP spoofing success and capturing intercepted traffic for analysis

## Common Scenarios

### Scenario: Testing Dynamic ARP Inspection Effectiveness on Enterprise Switches

**Context**: A network team deployed Cisco DAI on all access-layer switches and needs to validate that ARP spoofing attempts are properly detected and blocked. The test is authorized on a dedicated VLAN (VLAN 100) with three test hosts and one attacker machine connected to the same switch.

**Approach**:
1. Document baseline ARP tables on all hosts and the legitimate MAC-IP bindings in the DHCP snooping database
2. Run arpspoof from the attacker machine targeting the default gateway and a test workstation
3. Verify that the switch drops spoofed ARP packets by checking DAI statistics: `show ip arp inspection statistics vlan 100`
4. Confirm the test workstation's ARP cache still shows the legitimate gateway MAC address
5. Temporarily disable DAI on the test VLAN and repeat the attack to confirm it succeeds without the control
6. Re-enable DAI and document results showing the control is effective
7. Verify that IDS alerts were generated for both the blocked and unblocked attack attempts

**Pitfalls**:
- Running ARP spoofing on a VLAN without DAI and accidentally disrupting legitimate traffic
- Forgetting to enable IP forwarding, causing a denial-of-service instead of transparent interception
- Not restoring ARP tables after testing, leaving hosts with stale cache entries
- Testing on a trunk port instead of an access port, potentially affecting multiple VLANs

## Output Format

```
## ARP Spoofing Simulation Report

**Test ID**: NET-ARP-001
**Date**: 2024-03-15 14:00-15:00 UTC
**Target VLAN**: VLAN 100 (192.168.1.0/24)
**Attacker**: 192.168.1.99 (AA:BB:CC:DD:EE:FF)
**Target**: 192.168.1.50 (00:11:22:33:44:55)
**Gateway**: 192.168.1.1 (00:AA:BB:CC:DD:01)

### Test Results

| Test | DAI Status | ARP Spoof Result | Traffic Intercepted |
|------|------------|-------------------|---------------------|
| Test 1 | Enabled | Blocked (switch dropped 847 packets) | No |
| Test 2 | Disabled | Successful (target ARP cache poisoned) | Yes - 23 HTTP sessions |
| Test 3 | Re-enabled | Blocked | No |

### Detection Coverage
- DAI: PASS - Dropped all spoofed ARP replies when enabled
- IDS (Snort): PASS - Generated alert SID:1000010 within 15 seconds
- SIEM: PASS - Alert correlated and escalated within 2 minutes

### Recommendations
1. Maintain DAI enabled on all access VLANs (currently disabled on VLANs 200, 210)
2. Enable DHCP snooping rate limiting to prevent DHCP starvation attacks
3. Deploy 802.1X port authentication to complement ARP inspection
```