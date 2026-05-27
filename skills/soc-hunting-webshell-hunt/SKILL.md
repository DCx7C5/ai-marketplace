---
name: soc-hunting-webshell-hunt
description: - When proactively hunting for indicators of hunting for webshell activity in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessments and purp
domain: cybersecurity
---
------|-------------|
| T1505.003 | Web Shell |
| T1190 | Exploit Public-Facing Application |
| T1059.001 | PowerShell |

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

1. **Scenario 1**: China Chopper web shell via IIS vulnerability
2. **Scenario 2**: ASPXSpy through vulnerable upload
3. **Scenario 3**: PHP shell hidden in image file
4. **Scenario 4**: JSP shell via Tomcat manager console

## Output Format

```
Hunt ID: TH-HUNTIN-[DATE]-[SEQ]
Technique: T1505.003
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```