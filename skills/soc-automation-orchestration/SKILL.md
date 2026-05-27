---
name: soc-automation-orchestration
description: "Soc Automation Orchestration."
domain: cybersecurity
---

--|
| **SOAR** | Security Orchestration, Automation, and Response — platform integrating security tools with automated playbooks |
| **Playbook** | Automated workflow defining sequential and parallel actions triggered by security events |
| **Asset** | SOAR configuration for a connected security tool (API endpoint, credentials, connection parameters) |
| **Container** | SOAR event object containing artifacts (IOCs) from an ingested alert or incident |
| **Artifact** | Individual IOC or data point within a container (IP, hash, URL, domain, email) |
| **Approval Gate** | Human-in-the-loop step requiring analyst decision before executing high-impact automated actions |

## Tools & Systems

- **Splunk SOAR (Phantom)**: Enterprise SOAR platform with 300+ app integrations and visual playbook editor
- **Splunk ES**: SIEM platform feeding notable events into SOAR as containers for automated triage
- **CrowdStrike Falcon**: EDR platform integrated via SOAR for automated host isolation and threat hunting
- **ServiceNow**: ITSM platform integrated for automated incident ticket creation and tracking
- **Palo Alto NGFW**: Firewall integrated for automated IP/URL blocking via SOAR playbooks

## Common Scenarios

- **Phishing Triage**: Auto-extract URLs/attachments, detonate in sandbox, block malicious, create ticket
- **Malware Alert Enrichment**: Auto-enrich file hashes across VT/MalwareBazaar, isolate if confirmed malicious
- **Brute Force Response**: Auto-check if attack succeeded, disable account if compromised, block source IP
- **Threat Intel IOC Processing**: Auto-ingest TI feed IOCs, check against internal logs, create blocks for matches
- **Vulnerability Alert Response**: Auto-query asset database for affected systems, create patching ticket with priority

## Output Format

```
SOAR PLAYBOOK EXECUTION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Playbook:     Phishing Triage Automation v2.3
Container:    SOAR-2024-08921
Trigger:      Notable event from Splunk ES (phishing)

Actions Executed:
  [1] URL Reputation (VirusTotal)     — 14/90 engines malicious    [2.1s]
  [2] IP Reputation (AbuseIPDB)       — Confidence: 85%            [1.3s]
  [3] Block URL (Palo Alto)           — Blocked on PA-5260         [0.8s]
  [4] Block IP (Palo Alto)            — Blocked on PA-5260         [0.7s]
  [5] Create Ticket (ServiceNow)      — INC0012345 created         [1.5s]
  [6] Prompt Analyst (Tier 2)         — Response: "Isolate Host"   [4m 12s]
  [7] Quarantine Device (CrowdStrike) — WORKSTATION-042 isolated   [3.2s]

Total Duration:    4m 22s (vs 35min avg manual triage)
Time Saved:        ~31 minutes
Disposition:       True Positive — Escalated to IR
```
