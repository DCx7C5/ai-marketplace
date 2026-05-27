---
name: soc-hunting-elastic
description: "Soc Hunting Elastic."
domain: cybersecurity
---

--|
| **KQL** | Kibana Query Language — simplified query syntax for filtering data in Kibana Discover and dashboards |
| **EQL** | Event Query Language — Elastic's sequence-aware query language for detecting multi-step attack patterns |
| **ECS** | Elastic Common Schema — standardized field naming convention enabling cross-source correlation |
| **Timeline** | Elastic Security investigation workspace for collaborative event analysis and annotation |
| **Hypothesis-Driven Hunting** | Structured approach starting with a theory about attacker behavior, tested against telemetry data |
| **LOLBins** | Living Off the Land Binaries — legitimate Windows tools (certutil, mshta, rundll32) abused by attackers |

## Tools & Systems

- **Elastic Security**: SIEM platform built on Elasticsearch with detection rules, Timeline, and case management
- **Elastic Agent**: Unified data collection agent replacing Beats for endpoint and network telemetry
- **Elastic Endpoint Security**: EDR capabilities integrated into Elastic Agent for process, file, and network monitoring
- **ATT&CK Navigator**: MITRE tool for tracking detection and hunting coverage across the ATT&CK matrix

## Common Scenarios

- **LOLBin Abuse**: Hunt for mshta.exe, regsvr32.exe, rundll32.exe, certutil.exe with suspicious arguments
- **Persistence Mechanisms**: Query for scheduled task creation, registry run key modification, WMI subscriptions
- **C2 Beaconing**: Analyze network flow data for periodic outbound connections with consistent intervals
- **Data Staging**: Hunt for large file compression (7z, rar, zip) followed by outbound transfers
- **Account Manipulation**: Search for net.exe user creation, group membership changes, or password resets by non-admin users

## Output Format

```
THREAT HUNT REPORT — TH-2024-012
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hypothesis:   Attackers using certutil.exe for tool download (T1105)
Period:       2024-02-15 to 2024-03-15
Data Sources: Elastic Endpoint (process events), Sysmon

Findings:
  Total certutil executions:     342
  With -urlcache flag:           12 (3.5%)
  Suspicious (non-SCCM):        3 confirmed anomalous

Affected Hosts:
  WORKSTATION-042 (Finance)  — certutil downloading payload.exe from external IP
  SERVER-DB-03 (Database)    — certutil decoding base64 encoded binary
  LAPTOP-EXEC-07 (Executive) — certutil downloading script from Pastebin

Actions Taken:
  [DONE] 3 hosts isolated for forensic investigation
  [DONE] Detection rule "Certutil Download Activity" deployed (ID: elastic-th012)
  [DONE] ATT&CK Navigator updated: T1105 coverage = GREEN

Verdict:      HYPOTHESIS CONFIRMED — 3 true positive findings escalated to IR
```
