---
name: soc-hunting-threat-hunt
description: "Soc Hunting Threat Hunt."
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

1. **Scenario 1**: Intelligence-driven hunt based on APT campaign report
2. **Scenario 2**: ATT&CK coverage gap analysis driving hypothesis creation
3. **Scenario 3**: Anomaly-driven hypothesis from UEBA alert investigation
4. **Scenario 4**: Situational awareness hunt based on industry sector threats

## Output Format

```
Hunt ID: TH-BUILDI-[DATE]-[SEQ]
Technique: TA0001
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```
