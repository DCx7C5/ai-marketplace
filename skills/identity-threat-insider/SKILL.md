---
name: identity-threat-insider
description: - When proactively hunting for indicators of detecting insider threat behaviors in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessments and
domain: cybersecurity
---
------|-------------|
| T1078 | Valid Accounts |
| T1530 | Data from Cloud Storage Object |
| T1567 | Exfiltration Over Web Service |

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

1. **Scenario 1**: Employee downloading bulk files before resignation
2. **Scenario 2**: IT admin accessing HR data outside job function
3. **Scenario 3**: Service account used for unauthorized data queries
4. **Scenario 4**: Contractor copying source code to personal cloud storage

## Output Format

```
Hunt ID: TH-DETECT-[DATE]-[SEQ]
Technique: T1078
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```