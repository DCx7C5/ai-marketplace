---
name: soc-hunting-scheduled-hunt
description: - When proactively hunting for indicators of hunting for scheduled task persistence in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessments
domain: cybersecurity
---
------|-------------|
| T1053.005 | Scheduled Task |
| T1053.003 | Cron |
| T1053.002 | At |

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

1. **Scenario 1**: Cobalt Strike persistence via schtasks creating periodic beacon
2. **Scenario 2**: Ransomware scheduled task for re-execution after reboot
3. **Scenario 3**: APT encoded PowerShell task running every 30 minutes
4. **Scenario 4**: Insider task to periodically copy sensitive files

## Output Format

```
Hunt ID: TH-HUNTIN-[DATE]-[SEQ]
Technique: T1053.005
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```