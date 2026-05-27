---
name: soc-operations-escalation-escalate
description: "Soc Operations Escalation Escalate."
domain: cybersecurity
---

|
| P2 unresolved after 4 hours | Escalate to Tier 3 |
| P3 unresolved after 12 hours | Escalate to Tier 2 |
| Any incident unresolved past SLA | Escalate to SOC Manager |
| P1 unresolved after 2 hours | Escalate to CISO |

## Communication Templates

### P1 Initial Notification

```
SUBJECT: [P1 CRITICAL] Security Incident - {Incident_ID}

Incident Summary:
- Type: {incident_type}
- Affected Systems: {systems}
- Affected Users: {users}
- Current Status: {status}
- Assigned To: {analyst}

Impact Assessment:
- Business Impact: {impact}
- Data at Risk: {data_risk}
- Containment Status: {containment}

Next Actions:
- {action_1}
- {action_2}

Next Update: {time} (30-minute intervals)
Bridge Line: {conference_details}
```

## Escalation Matrix Implementation

### SOAR Integration

```yaml
# XSOAR escalation playbook trigger
trigger:
  condition: incident.severity == "critical" AND incident.asset_criticality == "high"
  action:
    - assign_tier: 3
    - notify: [soc_manager, ciso]
    - create_war_room: true
    - start_bridge: true
    - set_sla: 4h

auto_escalation_rules:
  - name: P2 Time-Based Escalation
    condition: incident.severity == "high" AND incident.age > 4h AND incident.status != "resolved"
    action:
      - escalate_tier: 3
      - notify: soc_manager
      - add_comment: "Auto-escalated due to SLA breach"
```

## References

- [Torq - Threat Escalation Matrix for Modern Security Challenges](https://torq.io/blog/escalation-matrix/)
- [ClearFeed - Incident Escalation Matrix](https://clearfeed.ai/blogs/incident-escalation-matrix)
- [Vectra - SOC Operations Guide](https://www.vectra.ai/topics/soc-operations)
- [Runframe - Incident Priority Levels Explained](https://runframe.io/learn/incident-priority)
