---
name: net-layer2-arp-poison
description: "Net Layer2 Arp Poison."
domain: cybersecurity
---

|
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
