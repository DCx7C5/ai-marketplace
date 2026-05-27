---
name: soc-workflow-ticketing-integrate
description: Use this skill when: - SOC teams need to formalize incident tracking beyond SIEM notable event management - Compliance requirements mandate documented incident lifecycle with timestamps and audit trails - Multi-team coordination requires ticket-based workflows with assignment and escalation - SLA tracking needs automated measurement of response and
domain: cybersecurity
---
Active incidents approaching SLA breach
index=servicenow sourcetype="snow:incident" category="Security" state IN ("New", "In Progress")
| eval sla_minutes = case(
    urgency="1", 15,
    urgency="2", 30,
    urgency="3", 120,
    urgency="4", 480
  )
| eval age_minutes = round((now() - strptime(opened_at, "%Y-%m-%d %H:%M:%S")) / 60, 0)
| eval sla_remaining = sla_minutes - age_minutes
| eval sla_status = case(
    sla_remaining < 0, "BREACHED",
    sla_remaining < sla_minutes * 0.25, "AT RISK",
    1=1, "ON TRACK"
  )
| where sla_status IN ("BREACHED", "AT RISK")
| sort sla_remaining
| table number, short_description, urgency, assignment_group, assigned_to,
        age_minutes, sla_minutes, sla_remaining, sla_status
```

**Auto-Escalation Logic:**
```python
def check_sla_breaches(ticket_manager):
    """Check for SLA breaches and auto-escalate"""
    open_incidents = ticket_manager.get_open_incidents()

    for incident in open_incidents:
        age_minutes = (datetime.utcnow() - incident["opened_at"]).total_seconds() / 60
        sla_minutes = {"1": 15, "2": 30, "3": 120, "4": 480}[incident["urgency"]]

        if age_minutes > sla_minutes and incident["state"] == "New":
            ticket_manager.escalate_incident(
                incident["number"],
                f"SLA BREACH: {int(age_minutes)}min elapsed, {sla_minutes}min SLA. Auto-escalating."
            )
```

### Step 5: Build Reporting and Metrics

```spl
--- Monthly incident metrics
index=servicenow sourcetype="snow:incident" category="Security"
opened_at > "2024-03-01" opened_at < "2024-04-01"
| stats count AS total,
        avg(eval((resolved_at - opened_at) / 3600)) AS avg_resolution_hours,
        sum(eval(if(urgency="1", 1, 0))) AS critical,
        sum(eval(if(urgency="2", 1, 0))) AS high,
        sum(eval(if(urgency="3", 1, 0))) AS medium,
        sum(eval(if(urgency="4", 1, 0))) AS low
| eval avg_resolution = round(avg_resolution_hours, 1)

--- SLA compliance rate
index=servicenow sourcetype="snow:incident" category="Security" state="Resolved"
| eval sla_target = case(urgency="1", 4, urgency="2", 8, urgency="3", 24, urgency="4", 72)
| eval resolution_hours = (resolved_at - opened_at) / 3600
| eval sla_met = if(resolution_hours <= sla_target, 1, 0)
| stats sum(sla_met) AS met, count AS total
| eval compliance_pct = round(met / total * 100, 1)
```

## Key Concepts

| Term | Definition |
|------|-----------|
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