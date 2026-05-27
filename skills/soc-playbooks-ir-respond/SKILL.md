---
name: soc-playbooks-ir-respond
description: - Establishing or maturing an incident response program from scratch - Documenting procedures for a new incident type after a novel attack - Automating response workflows in a SOAR platform (Cortex XSOAR, Splunk SOAR) - Preparing for compliance audits requiring documented IR procedures (SOC 2, PCI-DSS, HIPAA) - Conducting a gap analysis of existing
domain: cybersecurity
---
---|------------|
| **Playbook** | Documented, repeatable set of procedures for responding to a specific incident type |
| **Runbook** | More granular than a playbook; step-by-step technical instructions for a specific task within a playbook |
| **RACI Matrix** | Responsibility assignment chart defining who is Responsible, Accountable, Consulted, and Informed for each activity |
| **Decision Tree** | Flowchart-based logic defining the response path based on binary conditions at each decision point |
| **Escalation Criteria** | Predefined conditions that trigger notification of higher-level personnel or external parties |
| **SOAR Playbook** | Automated workflow in a Security Orchestration, Automation, and Response platform executing playbook steps |

## Tools & Systems

- **Cortex XSOAR**: SOAR platform with visual playbook editor, 700+ integrations, and collaborative War Room
- **Splunk SOAR**: SOAR platform integrated with Splunk ES, drag-and-drop playbook builder with 2,800+ automated actions
- **TheHive**: Open-source incident response platform with case templates that function as playbook frameworks
- **Confluence / GitLab Wiki**: Documentation platforms for maintaining human-readable playbook documents with version control
- **Tines**: No-code security automation platform for building playbook workflows without programming

## Common Scenarios

### Scenario: Building a Phishing Response Playbook from Scratch

**Context**: An organization with a 5-person SOC has no documented phishing response procedure. Analysts handle phishing reports inconsistently.

**Approach**:
1. Interview SOC analysts to document their current ad hoc process
2. Define the trigger: user reports phishing email via abuse@ mailbox or phishing button
3. Write triage steps: extract email headers, check sender reputation, analyze URLs/attachments in sandbox
4. Define containment: quarantine email from all mailboxes, block sender domain, reset passwords if credentials entered
5. Build SOAR automation: auto-extract IOCs from reported email, enrich via VirusTotal, create case in TheHive
6. Test with simulated phishing email and measure response time improvement

**Pitfalls**:
- Writing overly generic procedures that don't reference specific tool interfaces or commands
- Not including the communication plan for notifying users who received the phishing email
- Forgetting to define the criteria for when a phishing report becomes a full incident investigation
- Not versioning the playbook or scheduling regular review cycles

## Output Format

```
INCIDENT RESPONSE PLAYBOOK
============================
Playbook Name:    Phishing Incident Response
Version:          2.1
Owner:            SOC Manager
Last Reviewed:    2025-11-01
Next Review:      2026-02-01
Trigger:          Phishing email reported via abuse@corp.com or phish button

RACI MATRIX
Activity                    | SOC L1 | SOC L2 | IR Lead | Legal | Comms
Initial Triage              |   R    |   C    |   I     |       |
Email Analysis              |   R    |   A    |   I     |       |
Containment                 |        |   R    |   A     |   I   |
Credential Reset            |        |   R    |   A     |       |
User Notification           |        |   C    |   A     |       |   R
Regulatory Notification     |        |        |   C     |   R   |   A
Lessons Learned             |   C    |   C    |   R     |   I   |   I

PROCEDURE STEPS
[Detailed steps with tool-specific instructions]

DECISION TREE
[Flowchart logic]

ESCALATION MATRIX
[Conditions and contacts]

METRICS
Target MTTA: 15 minutes
Target MTTC: 1 hour
Target MTTR: 4 hours
```