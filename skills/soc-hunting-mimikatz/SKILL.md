---
name: soc-hunting-mimikatz
description: - When proactively hunting for indicators of detecting mimikatz execution patterns in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessments 
domain: cybersecurity
---
------|-------------|
| T1003.001 | LSASS Memory |
| T1003.006 | DCSync |
| T1558.003 | Kerberoasting |
| T1558.001 | Golden Ticket |

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

1. **Scenario 1**: Standard sekurlsa::logonpasswords credential dump
2. **Scenario 2**: PowerShell Invoke-Mimikatz reflective loading
3. **Scenario 3**: DCSync from non-DC host
4. **Scenario 4**: Golden ticket creation for persistence

## Output Format

```
Hunt ID: TH-DETECT-[DATE]-[SEQ]
Technique: T1003.001
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```