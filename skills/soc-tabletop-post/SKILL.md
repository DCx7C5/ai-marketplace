---
name: soc-tabletop-post
description: - After any security incident has been fully resolved and recovery completed - Following tabletop exercises or IR simulations - After significant near-miss events - Quarterly review of accumulated incident trends - When IR playbooks need updating based on real-world experience
domain: cybersecurity
---
------|-------------|
| Blameless Post-Mortem | Reviewing incidents focusing on systems, not blaming individuals |
| Root Cause Analysis | Identifying the fundamental reason the incident occurred |
| 5 Whys | Iterative questioning technique to find root cause |
| MTTD | Mean Time to Detect - time from compromise to detection |
| MTTC | Mean Time to Contain - time from detection to containment |
| MTTR | Mean Time to Recover - time from eradication to full recovery |
| Continuous Improvement | Iterating on IR processes based on real incident data |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| TheHive/ServiceNow | Incident timeline and documentation |
| Jira/Azure DevOps | Action item tracking |
| Confluence/SharePoint | Lessons learned documentation |
| Splunk/Elastic | Incident metrics and detection improvement |
| Sigma | Detection rule development |

## Common Scenarios

1. **Ransomware Post-Mortem**: Review entire kill chain from initial access to encryption. Identify detection gaps and backup failures.
2. **Phishing Campaign Review**: Analyze why users clicked, why email filters missed it, and how to improve training.
3. **Cloud Misconfiguration Incident**: Review IaC pipeline, CSPM coverage, and change management process.
4. **Insider Threat Review**: Examine DLP effectiveness, access control gaps, and user monitoring capabilities.
5. **Third-Party Breach Impact**: Review vendor risk assessment process and data sharing agreements.

## Output Format
- Post-incident review meeting minutes
- Root cause analysis document
- Incident metrics report (MTTD, MTTC, MTTR)
- Action items list with owners and deadlines
- Updated IR playbooks and detection rules
- Executive summary for leadership