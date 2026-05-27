---
name: soc-hunting-scheduled-hunt
description: "Soc Hunting Scheduled Hunt."
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
