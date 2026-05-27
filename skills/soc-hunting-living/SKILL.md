---
name: soc-hunting-living
description: - When proactively hunting for indicators of hunting for living off the cloud techniques in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assess
domain: cybersecurity
---
------|-------------|
| T1102 | Web Service |
| T1567 | Exfiltration Over Web Service |
| T1537 | Transfer Data to Cloud Account |

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

1. **Scenario 1**: C2 over Discord webhooks for command delivery
2. **Scenario 2**: Data exfiltration to Telegram bot API
3. **Scenario 3**: Malware using Azure Functions for dynamic C2
4. **Scenario 4**: Staging stolen data on Google Docs or Notion pages

## Output Format

```
Hunt ID: TH-HUNTIN-[DATE]-[SEQ]
Technique: T1102
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```