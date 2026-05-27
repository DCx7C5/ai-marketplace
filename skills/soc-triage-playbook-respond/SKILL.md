---
name: soc-triage-playbook-respond
description: "Soc Triage Playbook Respond."
domain: cybersecurity
---

|
| Splunk/Elastic/QRadar | SIEM alert correlation and querying |
| TheHive/SIRP | Incident case management and playbook tracking |
| VirusTotal/AbuseIPDB | IOC reputation and enrichment |
| PagerDuty/OpsGenie | On-call management and alerting |
| MITRE ATT&CK | Technique classification and mapping |
| Cortex XSOAR | SOAR platform for automated triage workflows |

## Common Scenarios

1. **Brute Force Alert**: Multiple failed logins from single IP. Enrich IP reputation, check geo-location, verify if account was compromised, assign P3 if unsuccessful.
2. **Malware Detection on Endpoint**: AV/EDR quarantined malware. Verify quarantine success, check for lateral movement, assign P2 if persistence detected.
3. **Suspicious Outbound Traffic**: Large data transfer to unknown external IP. Check if known cloud service, verify data classification, assign P1 if exfiltration confirmed.
4. **Phishing Email Reported**: User reports suspicious email. Extract IOCs, check if others received it, assign P2 if credentials were entered.
5. **Privilege Escalation**: User gained admin rights unexpectedly. Verify if authorized change, check for exploitation, assign P1 if unauthorized.

## Output Format
- Triage decision document with severity justification
- Incident ticket with assigned playbook and team
- IOC enrichment summary attached to case
- Escalation notification to appropriate stakeholders
- Initial timeline of events from alert data
