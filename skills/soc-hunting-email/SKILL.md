---
name: soc-hunting-email
description: "Soc Hunting Email."
domain: cybersecurity
---

|
| CrowdStrike Falcon | EDR telemetry and threat detection |
| Microsoft Defender for Endpoint | Advanced hunting with KQL |
| Splunk Enterprise | SIEM log analysis with SPL queries |
| Elastic Security | Detection rules and investigation timeline |
| Sysmon | Detailed Windows event monitoring |
| Velociraptor | Endpoint artifact collection and hunting |
| Sigma Rules | Cross-platform detection rule format |

## Common Scenarios

1. **Scenario 1**: BEC actor creating forwarding rule to external email
2. **Scenario 2**: Compromised account with rule deleting security alerts
3. **Scenario 3**: Inbox rule forwarding CEO emails to attacker mailbox
4. **Scenario 4**: OAuth app abuse creating transport rules for data collection

## Output Format

```
Hunt ID: TH-DETECT-[DATE]-[SEQ]
Technique: T1114.003
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```
