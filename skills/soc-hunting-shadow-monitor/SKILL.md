---
name: soc-hunting-shadow-monitor
description: - When proactively hunting for indicators of hunting for shadow copy deletion in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessments and p
domain: cybersecurity
---
------|-------------|
| T1490 | Inhibit System Recovery |
| T1486 | Data Encrypted for Impact |
| T1485 | Data Destruction |

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

1. **Scenario 1**: Ransomware deleting shadow copies before encryption
2. **Scenario 2**: vssadmin delete shadows /all /quiet pre-encryption
3. **Scenario 3**: WMIC shadowcopy delete via PowerShell
4. **Scenario 4**: bcdedit disabling recovery mode before impact

## Output Format

```
Hunt ID: TH-HUNTIN-[DATE]-[SEQ]
Technique: T1490
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```