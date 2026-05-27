---
name: soc-playbooks-otirplaybook-respond
description: "Soc Playbooks Otirplaybook Respond."
domain: cybersecurity
---

|
| PICERL | SANS incident response lifecycle: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned |
| ICS4ICS | Incident Command System for Industrial Control Systems -- adapts FEMA ICS to OT cybersecurity response |
| Safety Instrumented System (SIS) | Independent safety controller that prevents hazardous conditions; compromising SIS can cause physical harm |
| Manual/Local Mode | Operating PLCs with local panel controls instead of remote SCADA; used when remote access is compromised |
| CIRCIA | Cyber Incident Reporting for Critical Infrastructure Act requiring reporting to CISA within 72 hours |
| Known-Good Backup | Verified, offline copy of PLC programs and configurations used as the trusted baseline for recovery |

## Common Scenarios

### Scenario: Ransomware Spreads from IT to OT Level 3

**Context**: Ransomware encrypts enterprise IT systems and spreads through an inadequately protected IT/OT conduit to Level 3 historian servers. HMIs at Level 2 begin showing connectivity errors.

**Approach**:
1. Activate the OT IR playbook for ransomware immediately
2. Sever IT-OT connectivity at the DMZ firewall (both north and south firewalls)
3. Verify PLCs are still running and process is stable (PLCs run independently of IT)
4. Switch operators to local HMI panels if networked HMIs are affected
5. Assess which Level 2/3 systems are encrypted vs operational
6. Prioritize restoring HMI visibility, then historian, then engineering workstations
7. Restore from offline backups -- never attempt to decrypt using attacker-provided tools without sandbox testing
8. Report to CISA within 72 hours per CIRCIA requirements

**Pitfalls**: Do not shut down PLCs to "protect" them from ransomware -- PLCs run firmware, not Windows, and are typically unaffected by ransomware. Shutting down PLCs disrupts the physical process. Never reconnect IT-OT conduit until the IT side is fully remediated.

## Output Format

```
OT INCIDENT RESPONSE REPORT
==============================
Incident ID: OT-IR-YYYYMMDD-HHMMSS
Severity: SEV[1-5]
Category: [category]
Status: [Active/Contained/Eradicated/Recovered/Closed]

TIMELINE:
  [timestamp] - [phase] - [action] - [actor]

AFFECTED SYSTEMS:
  Safety Systems: [status]
  Process Controllers: [status]
  HMI/SCADA: [status]
  Historian: [status]

DECISIONS LOG:
  [timestamp] - [decision] - [rationale] - [approver]

CONTAINMENT ACTIONS TAKEN:
  1. [action and timestamp]

RECOVERY STATUS:
  [system] - [restored/pending] - [ETA]
```
