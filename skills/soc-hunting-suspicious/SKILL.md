---
name: soc-hunting-suspicious
description: "Soc Hunting Suspicious."
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

1. **Scenario 1**: Base64 encoded PowerShell command launched by macro document
2. **Scenario 2**: IEX download cradle fetching payload from C2 server
3. **Scenario 3**: AMSI bypass via reflection patching before payload execution
4. **Scenario 4**: PowerShell Empire agent communicating with C2

## Output Format

```
Hunt ID: TH-DETECT-[DATE]-[SEQ]
Technique: T1059.001
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```
