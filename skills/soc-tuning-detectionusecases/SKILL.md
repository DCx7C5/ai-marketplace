---
name: soc-tuning-detectionusecases
description: Use this skill when: - SOC teams need to build or expand their SIEM detection library from scratch - Threat assessments identify ATT&CK technique gaps requiring new detection rules - Detection engineers need a structured process for use case design, testing, and deployment - Compliance requirements mandate specific detection capabilities (PCI DSS, 
domain: cybersecurity
---
------------------------|-----------------------------------------------------------------------------------------------------------|
| **Use Case**              | Formalized detection rule with documented logic, testing, tuning, and lifecycle management                |
| **Detection Engineering** | Practice of designing, testing, and maintaining SIEM detection rules as a software development discipline |
| **Correlation Search**    | SIEM query that combines events from multiple sources to identify attack patterns                         |
| **False Positive Rate**   | Percentage of alerts that are benign activity — target <20% for production use cases                      |
| **Detection Latency**     | Time between event occurrence and alert generation — target <5 minutes for critical detections            |
| **ATT&CK Coverage**       | Percentage of relevant ATT&CK techniques with at least one production detection rule                      |

## Tools & Systems

- **Splunk ES**: Enterprise SIEM with correlation searches, risk-based alerting, and Incident Review
- **Elastic Security**: SIEM with detection rules, EQL sequences, and ML-based anomaly detection
- **Microsoft Sentinel**: Cloud SIEM with KQL analytics rules, Fusion ML engine, and Lighthouse multi-tenant
- **Atomic Red Team**: Open-source attack simulation framework for testing detection rules against ATT&CK techniques
- **ATT&CK Navigator**: MITRE visualization tool for mapping and tracking detection coverage across techniques

## Common Scenarios

- **Post-Incident Use Case**: After a ransomware incident, build detection for the initial access vector discovered during investigation
- **Compliance-Driven**: PCI DSS requires detection of admin account misuse — build use cases for 4672/4720/4732 events
- **Threat-Intel Driven**: New APT group targets your sector — build use cases for their documented TTPs
- **Red Team Findings**: Purple team exercise identifies blind spots — convert findings into production detection rules
- **SIEM Migration**: Migrating from QRadar to Splunk — convert and validate all existing use cases on new platform

## Output Format

```
USE CASE DEPLOYMENT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━
Quarter:      Q1 2024
Total Use Cases: 147 (Production: 128, Staging: 12, Development: 7)

New Deployments This Quarter:
  UC-2024-012  Kerberoasting Detection (T1558.003)     — Production
  UC-2024-013  DLL Side-Loading (T1574.002)            — Production
  UC-2024-014  Scheduled Task Persistence (T1053.005)  — Production
  UC-2024-015  LSASS Memory Access (T1003.001)         — Staging

ATT&CK Coverage:
  Overall: 67% of relevant techniques (up from 61%)
  Initial Access:      78%
  Execution:           82%
  Persistence:         71%
  Credential Access:   65%
  Lateral Movement:    58% (priority gap area)

Health Metrics:
  Avg True Positive Rate:    74% (target: >70%)
  Avg Detection Latency:     2.3 min (target: <5 min)
  Use Cases Deprecated:      3 (replaced by improved versions)
```