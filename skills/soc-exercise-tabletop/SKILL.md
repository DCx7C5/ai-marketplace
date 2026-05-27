---
name: soc-exercise-tabletop
description: "Soc Exercise Tabletop."
domain: cybersecurity
---

--|
| **Tabletop Exercise** | Discussion-based simulation where participants walk through incident scenarios without executing technical actions |
| **Inject** | Scenario update introducing new information, complications, or decisions for participants to address |
| **Hot Wash** | Immediate post-exercise debrief where participants share observations and initial lessons learned |
| **After-Action Report (AAR)** | Formal document capturing exercise findings, gaps, strengths, and remediation action items |
| **Facilitator** | Exercise leader who presents injects, guides discussion, and ensures objectives are met |
| **Decision Point** | Moment in the scenario requiring participants to choose between options with trade-offs |

## Tools & Systems

- **FEMA HSEEP**: Homeland Security Exercise and Evaluation Program providing exercise planning methodology
- **Tabletop Exercise Framework (NIST SP 800-84)**: NIST guide for planning and conducting IT security exercises
- **Immersive Labs**: Platform for cybersecurity crisis simulation and tabletop exercise management
- **Infection Monkey**: Open-source breach simulation for technical validation of tabletop findings
- **Archer**: GRC platform for tracking exercise findings and remediation action items

## Common Scenarios

- **Ransomware Attack**: Multi-phase scenario testing detection, containment, ransom decision, and recovery
- **Data Breach**: Customer PII exposure testing notification requirements, legal obligations, and PR response
- **Supply Chain Compromise**: Third-party vendor breach impacting organizational systems and data
- **Insider Threat**: Employee data theft scenario testing HR, Legal, and security team coordination
- **Business Email Compromise**: CEO fraud wire transfer attempt testing financial controls and verification procedures

## Output Format

```
TABLETOP EXERCISE SUMMARY — TTX-2024-Q1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scenario:     Operation Dark Harvest (Ransomware)
Date:         2024-03-22 (09:00-12:00 UTC)
Participants: 10 (SOC: 5, IT: 1, Legal: 1, Comms: 1, Exec: 2)
Duration:     3 hours (6 injects delivered)

SCORES:
  Detection & Triage:    85/100  Excellent
  Containment:           80/100  Good
  Communication:         60/100  Needs Improvement
  Recovery Planning:     65/100  Needs Improvement
  Overall:               72/100  Adequate

KEY FINDINGS:
  [+] Strong: Ransomware indicators correctly identified immediately
  [+] Strong: EDR isolation procedure well understood
  [-] Gap: No after-hours CISO notification procedure
  [-] Gap: Backup recovery untested for 6 months
  [-] Gap: No pre-approved media statement templates
  [-] Gap: Service account over-privileged (Domain Admin)
  [-] Gap: Ransom payment decision authority undefined

ACTION ITEMS: 5 (Critical: 2, High: 2, Medium: 1)
NEXT EXERCISE: TTX-2024-Q2 (June 2024) — Insider Threat Scenario
```
