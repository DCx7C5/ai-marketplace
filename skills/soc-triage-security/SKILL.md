---
name: soc-triage-security
description: "Soc Triage Security."
domain: cybersecurity
---

|
| **Triage** | Rapid assessment process to classify and prioritize security incidents based on severity and business impact |
| **PICERL** | SANS incident response framework: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned |
| **Dwell Time** | Duration between initial compromise and detection; average is 10 days per Mandiant M-Trends 2025 |
| **True Positive Rate** | Percentage of alerts from a detection rule that represent genuine security incidents |
| **Crown Jewel Assets** | Systems and data critical to business operations whose compromise would cause severe organizational impact |
| **Alert Fatigue** | Degraded analyst performance caused by high volumes of low-fidelity or false-positive alerts |
| **Mean Time to Acknowledge (MTTA)** | Average time from alert generation to analyst acknowledgment; key SOC performance metric |

## Tools & Systems

- **Splunk Enterprise Security**: SIEM platform for alert aggregation, correlation, and triage workflow management
- **CrowdStrike Falcon**: EDR platform providing endpoint telemetry, detection, and one-click host containment
- **TheHive**: Open-source incident response platform for case management, task tracking, and team collaboration
- **MISP**: Threat intelligence sharing platform for IOC enrichment during triage
- **Cortex XSOAR**: SOAR platform for automating enrichment playbooks and triage decision trees

## Common Scenarios

### Scenario: Encoded PowerShell from Email Client

**Context**: SOC analyst receives a P2 alert showing `powershell.exe` with a Base64-encoded command spawned as a child process of `outlook.exe` on a finance department workstation.

**Approach**:
1. Decode the Base64 payload to determine the command intent
2. Check the parent process chain for anomalies (Outlook spawning PowerShell is abnormal)
3. Query VirusTotal for the decoded payload hash
4. Correlate with email gateway logs to identify the triggering email and sender
5. Check if other recipients in the organization received the same email
6. Isolate the endpoint and escalate to Tier 2 with full triage context

**Pitfalls**:
- Dismissing encoded PowerShell as a false positive without decoding the payload
- Failing to check for lateral spread to other recipients of the same phishing email
- Remediating the endpoint before capturing volatile memory evidence

## Output Format

```
INCIDENT TRIAGE REPORT
======================
Ticket:          INC-[YYYY]-[NNNN]
Date/Time:       [ISO 8601 timestamp]
Triage Analyst:  [Name]
Time to Triage:  [minutes from alert to classification]

CLASSIFICATION
Type:            [NIST category]
Severity:        [P1-P4] - [Critical/High/Medium/Low]
Confidence:      [High/Medium/Low]
MITRE ATT&CK:   [Technique ID and name]

AFFECTED SCOPE
Assets:          [hostname(s), IP(s)]
Users:           [account(s)]
Data at Risk:    [classification level]
Business Unit:   [department]

EVIDENCE SUMMARY
[Bullet list of key observations]

ENRICHMENT RESULTS
TI Matches:      [Yes/No - details]
Historical:      [Related prior incidents]
Asset Criticality: [rating]

RECOMMENDED ACTIONS
1. [Immediate action]
2. [Investigation step]
3. [Escalation target]

ESCALATION
Routed To:       [Team/Individual]
SLA Target:      [Containment deadline]
```
