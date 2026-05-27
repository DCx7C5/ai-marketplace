---
name: soc-hunting-unusual
description: - When proactively hunting for indicators of hunting for unusual network connections in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessment
domain: cybersecurity
---
------|-------------|
| T1071 | Application Layer Protocol |
| T1095 | Non-Application Layer Protocol |
| T1571 | Non-Standard Port |

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

1. **Scenario 1**: Backdoor communicating to C2 on non-standard port
2. **Scenario 2**: Data exfiltration over DNS to attacker nameserver
3. **Scenario 3**: Compromised host scanning internal network
4. **Scenario 4**: Cryptominer connecting to mining pool

## Output Format

```
Hunt ID: TH-HUNTIN-[DATE]-[SEQ]
Technique: T1071
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```