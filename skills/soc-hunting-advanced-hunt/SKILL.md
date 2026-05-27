---
name: soc-hunting-advanced-hunt
description: "Soc Hunting Advanced Hunt."
domain: cybersecurity
---

--|
| **TTP** | Tactics, Techniques, and Procedures — adversary behavioral patterns as defined in MITRE ATT&CK |
| **Diamond Model** | Analytical framework with four vertices (adversary, capability, infrastructure, victim) used to structure intrusion analysis |
| **Living-off-the-Land (LotL)** | Attacker technique using legitimate OS tools (PowerShell, WMI, certutil) to evade detection |
| **UEBA** | User and Entity Behavior Analytics — ML-based detection of anomalous behavior baselines |
| **Sigma** | Open standard for SIEM-agnostic detection rule format, analogous to YARA for network/log detection |
| **Hunt Hypothesis** | A testable prediction about adversary presence based on threat intelligence and environmental knowledge |

## Tools & Systems

- **Velociraptor**: Open-source DFIR platform with VQL query language for scalable endpoint hunting across thousands of systems
- **osquery**: SQL-based OS instrumentation framework for real-time endpoint telemetry queries
- **MITRE ATT&CK Navigator**: Web-based tool for visualizing ATT&CK coverage and technique prioritization
- **Zeek (formerly Bro)**: Network traffic analyzer producing structured logs (conn, dns, http, ssl) suitable for hunting
- **Elastic Security**: EQL (Event Query Language) enables sequence-based hunting for multi-stage attack patterns
- **Sigma**: Detection rule format with translators for Splunk, QRadar, Sentinel, and Elastic

## Common Pitfalls

- **Confirmation bias**: Starting a hunt expecting to find something and interpreting benign data as malicious. Document null results — they validate controls.
- **Insufficient data retention**: Many APT techniques require 90+ days of log history to identify slow-and-low patterns. Default retention periods are often too short.
- **Hunting without baselines**: Cannot identify anomalies without knowing normal. Spend time on baseline documentation before hunting.
- **Query performance impact**: Broad queries against production SIEM during business hours can degrade analyst workflows. Schedule intensive hunts during off-peak hours.
- **Ignoring false positives systematically**: Track false positive rates per query. Queries with >80% FP rate should be refined or retired before operationalization.
