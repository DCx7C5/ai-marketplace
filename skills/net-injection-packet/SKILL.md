---
name: net-injection-packet
description: "Net Injection Packet."
domain: cybersecurity
---

|
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
