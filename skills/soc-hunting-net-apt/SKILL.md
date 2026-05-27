---
name: soc-hunting-net-apt
description: Network-layer APT hunting on Linux. Checks ARP table for duplicate MAC entries (spoofing), active connections for unusual ports/destinations, DNS queries for tunneling indicators, and optionally captures raw traffic via tcpdump for post-analysis. All findings written to session findings.md.
domain: cybersecurity
---
|---|---|
| ARP table | `ip neigh` | Duplicate IPs with different MACs |
| Active connections | `ss -tnp` | Unusual ports, foreign IPs, suspicious processes |
| DNS | `/etc/resolv.conf`, `ss` | Non-standard DNS servers, high-volume lookups |
| Traffic capture | `tcpdump` | Beaconing intervals, large outbound transfers |

## MITRE Coverage

| Technique | Description |
|---|---|
| T1071 | Application Layer Protocol C2 |
| T1071.001 | C2 over HTTP/HTTPS |
| T1041 | Exfiltration Over C2 Channel |
| T1090 | Proxy / Traffic Tunneling |
| T1557.002 | ARP Cache Poisoning |