---
name: identity-serviceaccount-service
description: - When proactively hunting for indicators of detecting service account abuse in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessments and pu
domain: cybersecurity
---
------|-------------|
| T1078.002 | Domain Accounts |
| T1078.001 | Default Accounts |
| T1021 | Remote Services |

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

1. **Scenario 1**: Service account RDP to domain controller
2. **Scenario 2**: SQL service accessing file shares outside scope
3. **Scenario 3**: Backup service lateral movement off-hours
4. **Scenario 4**: Compromised svc with DA privileges used for DCSync

## Output Format

```
Hunt ID: TH-DETECT-[DATE]-[SEQ]
Technique: T1078.002
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```