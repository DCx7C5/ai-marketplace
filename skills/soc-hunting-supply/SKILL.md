---
name: soc-hunting-supply
description: - When proactively hunting for indicators of hunting for supply chain compromise in the environment - After threat intelligence indicates active campaigns using these techniques - During incident response to scope compromise related to these techniques - When EDR or SIEM alerts trigger on related indicators - During periodic security assessments an
domain: cybersecurity
---
------|-------------|
| T1195.001 | Compromise Software Dependencies |
| T1195.002 | Compromise Software Supply Chain |
| T1199 | Trusted Relationship |

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

1. **Scenario 1**: SolarWinds-style update mechanism compromise
2. **Scenario 2**: Compromised npm/PyPI package with backdoor
3. **Scenario 3**: Tampered build server deploying malicious artifacts
4. **Scenario 4**: Vendor VPN software update delivering malware

## Output Format

```
Hunt ID: TH-HUNTIN-[DATE]-[SEQ]
Technique: T1195.001
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```