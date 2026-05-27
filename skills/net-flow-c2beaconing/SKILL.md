---
name: net-flow-c2beaconing
description: - When proactively hunting for compromised systems in the network - After threat intel indicates C2 frameworks targeting your industry - When investigating periodic outbound connections to suspicious domains - During incident response to identify active C2 channels - When DNS query logs show unusual patterns to specific domains
domain: cybersecurity
---
------|-------------|
| T1071 | Application Layer Protocol (HTTP/HTTPS/DNS C2) |
| T1071.001 | Web Protocols (HTTP/S beaconing) |
| T1071.004 | DNS (DNS tunneling C2) |
| T1573 | Encrypted Channel |
| T1572 | Protocol Tunneling |
| T1568 | Dynamic Resolution (DGA, fast-flux) |
| T1132 | Data Encoding in C2 |
| T1095 | Non-Application Layer Protocol |
| Beacon Interval | Time between C2 check-ins |
| Jitter | Random variation in beacon interval |
| DGA | Domain Generation Algorithm |
| Fast-Flux | Rapidly changing DNS resolution |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| RITA (Real Intelligence Threat Analytics) | Automated beacon detection in Zeek logs |
| Splunk | Statistical beacon analysis with SPL |
| Elastic Security | ML-based anomaly detection for beaconing |
| Zeek/Bro | Network connection metadata collection |
| Suricata | Network IDS with JA3/JA4 fingerprinting |
| VirusTotal | Domain and IP reputation checking |
| PassiveDNS | Historical DNS resolution data |
| Flare | C2 profile detection |

## Common Scenarios

1. **Cobalt Strike Beacon**: HTTP/HTTPS beaconing with configurable sleep time and jitter to malleable C2 profiles.
2. **DNS Tunneling C2**: Data exfiltration and command receipt via encoded DNS TXT/CNAME queries to attacker-controlled domains.
3. **Sliver C2 over HTTPS**: Modern C2 framework using HTTPS with configurable beacon intervals and domain fronting.
4. **DGA-based C2**: Malware generating random domains daily, with adversary registering upcoming domains for C2.
5. **Legitimate Service Abuse**: C2 over legitimate cloud services (Azure, AWS, Slack, Discord, Telegram).

## Output Format

```
Hunt ID: TH-C2-[DATE]-[SEQ]
Source IP: [Internal IP]
Source Host: [Hostname]
Destination: [Domain/IP]
Protocol: [HTTP/HTTPS/DNS/Custom]
Beacon Interval: [Average seconds]
Jitter: [Percentage]
Connection Count: [Total connections]
Data Volume: [Bytes sent/received]
First Seen: [Timestamp]
Last Seen: [Timestamp]
Domain Age: [Days]
TI Match: [Yes/No - source]
Risk Level: [Critical/High/Medium/Low]
```