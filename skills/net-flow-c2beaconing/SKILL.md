---
name: net-flow-c2beaconing
description: "Net Flow C2Beaconing."
domain: cybersecurity
---

|
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
