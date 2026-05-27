---
name: soc-hunting-email
description: - When proactively hunting for indicators of detecting email forwarding rules attack in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessment
domain: cybersecurity
---
------|-------------|
| T1114.003 | Email Forwarding Rule |
| T1114.002 | Remote Email Collection |
| T1098.002 | Additional Email Delegate Permissions |

## Tools & Systems

| Tool | Purpose |
|------|---------|
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