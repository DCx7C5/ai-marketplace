---
name: net-capture-zeek-zeekanomaly
description: "| | DNS_Tunneling_Detected | 10.10.3.45 | 8.8.8.8 | 847 queries to suspect-domain."
domain: cybersecurity
---

|
| DNS_Tunneling_Detected | 10.10.3.45 | 8.8.8.8 | 847 queries to suspect-domain.xyz in 5 min |
| Possible_Beaconing | 10.10.5.12 | 203.0.113.50:443 | 62 connections with 59.8s avg interval |
| SSL::Invalid_Server_Cert | 10.10.8.22 | 198.51.100.33:443 | Self-signed cert, CN=localhost |
| SSH::Password_Guessing | 45.33.32.156 | 10.10.20.11:22 | 487 failed attempts in 30 min |

### Recommendations
1. Isolate 10.10.3.45 and investigate for DNS tunneling malware
2. Block 203.0.113.50 at firewall and forensically image 10.10.5.12
3. Investigate self-signed TLS certificate on 198.51.100.33
4. Block 45.33.32.156 and enforce SSH key-only authentication
```
