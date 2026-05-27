---
name: soc-playbooks-otirplaybook-respond
description: - When building OT-specific incident response procedures for the first time - When existing IT IR playbooks do not address ICS/SCADA-specific requirements - When preparing for OT ransomware scenarios like EKANS or LockerGoga - When aligning IR procedures with IEC 62443 and NERC CIP incident reporting requirements - When conducting post-incident rev
domain: cybersecurity
---
IMMEDIATE ACTIONS (Execute within first 15 minutes) ---")
        for i, action in enumerate(playbook["immediate_actions"], 1):
            print(f"  {i}. {action}")

        print(f"\n--- CONTAINMENT STEPS ---")
        for i, step in enumerate(playbook["containment_steps"], 1):
            print(f"  {i}. {step}")

        print(f"\n--- RECOVERY PRIORITY ORDER ---")
        for item in playbook["recovery_priority"]:
            print(f"  {item}")

        print(f"\n--- REPORTING REQUIREMENTS ---")
        for req in playbook["reporting"]:
            print(f"  - {req}")

        # Print PICERL phase guidance
        print(f"\n--- PICERL PHASE CHECKLIST ---")
        for phase, info in PICERL_PHASES.items():
            print(f"\n  [{phase.upper()}] {info['description']}")
            for item in info["ot_specific"][:3]:
                print(f"    - {item}")

if __name__ == "__main__":
    engine = OTPlaybookEngine()

    # Example: OT Ransomware incident
    incident = OTIncident(
        title="Ransomware detected on Level 3 historian servers",
        severity=OTIncidentSeverity.SEV2_PROCESS,
        category=OTIncidentCategory.RANSOMWARE,
        affected_systems=["HIST-01", "HIST-02", "ENG-WS-03", "HMI-AREA1"],
    )

    engine.execute_playbook(incident)
```

## Key Concepts

| Term | Definition |
|------|------------|
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