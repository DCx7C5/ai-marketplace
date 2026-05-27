---
name: soc-workflow-ticketing-integrate
description: "Soc Workflow Ticketing Integrate."
domain: cybersecurity
---

--|
| **Incident Ticket** | Formal tracking record for a confirmed security incident with lifecycle management |
| **SLA** | Service Level Agreement defining maximum response and resolution times by severity |
| **Escalation Path** | Defined routing from Tier 1 to Tier 2/3 based on severity, time elapsed, or analyst request |
| **Disposition** | Final classification of a closed incident (true positive, false positive, duplicate, policy violation) |
| **MTTR** | Mean Time to Resolve — average time from ticket creation to resolution across all incidents |
| **Case Management** | Structured approach to managing complex incidents with tasks, observables, and audit trails |

## Tools & Systems

- **ServiceNow ITSM**: Enterprise IT service management platform with security incident module and SLA tracking
- **Jira Service Management**: Atlassian's service management platform with customizable incident workflows
- **TheHive**: Open-source security incident response platform with case management and Cortex integration
- **PagerDuty**: On-call management and incident notification platform for SOC analyst alerting
- **Splunk ITSI**: IT Service Intelligence module for SLA tracking and service health dashboards

## Common Scenarios

- **SIEM-to-Ticket Automation**: Auto-create ServiceNow ticket for every critical/high notable event in Splunk ES
- **Multi-Team Coordination**: Route malware incidents to SOC for triage, IT for remediation, Legal for notification
- **Compliance Documentation**: Generate incident reports from ticket data for PCI DSS, HIPAA audit evidence
- **On-Call Alerting**: Page on-call analyst via PagerDuty when critical ticket created after hours
- **Post-Incident Review**: Query closed tickets to identify recurring incident types and systemic gaps

## Output Format

```
INCIDENT TICKET — INC0012567
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:        [SEC] Cobalt Strike C2 Beacon Detected — WORKSTATION-042
Category:     Security > Malware Infection
Severity:     Critical (P1)
SLA:          Response: 15 min | Resolution: 4 hours

Timeline:
  14:23  Ticket created (auto from Splunk ES NE-2024-08921)
  14:25  Assigned to analyst_jdoe (Tier 2)
  14:28  Work note: "VT confirms Cobalt Strike beacon, hash a1b2c3..."
  14:35  Work note: "Host isolated via CrowdStrike, C2 domain blocked"
  15:00  Work note: "Enterprise IOC scan — 2 additional hosts found"
  15:30  Escalated to Tier 3 for forensic analysis
  16:00  Work note: "All affected hosts contained and cleaned"
  18:00  Resolved: "Malware eradicated, systems restored, monitoring for 72h"

Metrics:
  Time to Acknowledge: 2 minutes
  Time to Contain:     12 minutes
  Time to Resolve:     3 hours 37 minutes
  SLA Status:          MET (within 4-hour resolution target)
```
