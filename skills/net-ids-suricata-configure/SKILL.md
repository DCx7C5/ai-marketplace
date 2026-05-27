---
name: net-ids-suricata-configure
description: "-| | 312 | 2024897 | ET POLICY curl User-Agent Outbound | 3 | | 189 | 9000003 | LOCAL Cobalt Strike JA3 Hash | 1 | | 145 | 2028765 | ET SCAN Nmap SYN Scan | 2 | | 98 | 9000002 | LOCAL DNS Tunneling Long Query | 2 |  ### Critical Alerts Requiring Immediate Triage 1."
domain: cybersecurity
---

-|
| 312 | 2024897 | ET POLICY curl User-Agent Outbound | 3 |
| 189 | 9000003 | LOCAL Cobalt Strike JA3 Hash | 1 |
| 145 | 2028765 | ET SCAN Nmap SYN Scan | 2 |
| 98 | 9000002 | LOCAL DNS Tunneling Long Query | 2 |

### Critical Alerts Requiring Immediate Triage
1. SID 9000003: Cobalt Strike JA3 from 10.10.5.12 to 203.0.113.50 (189 alerts)
2. SID 9000002: DNS tunneling from 10.10.3.45 to suspect-domain.xyz (98 alerts)
```
