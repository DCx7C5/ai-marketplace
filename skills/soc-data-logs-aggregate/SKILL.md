---
name: soc-data-logs-aggregate
description: - When reconstructing the timeline of a security incident from available log sources - During post-breach investigation to identify initial access, lateral movement, and exfiltration - When correlating events across multiple systems and log sources - For establishing evidence of unauthorized access or policy violations - When preparing forensic rep
domain: cybersecurity
---
------|-------------|
| Event correlation | Linking related events across multiple log sources by time, IP, user, or session |
| Log normalization | Converting diverse log formats into a common schema for unified analysis |
| Timeline analysis | Chronological ordering of events to reconstruct incident sequence |
| Log integrity | Verifying logs have not been tampered with using hashes and chain of custody |
| Logon types | Windows categorization of authentication methods (2=interactive, 3=network, 10=RDP) |
| Audit policy | System configuration determining which events are recorded in logs |
| Log rotation | Automatic archiving of log files that affects evidence availability |
| Anti-forensics | Attacker techniques for clearing or modifying logs to cover tracks |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| python-evtx | Python library for parsing Windows EVTX event log files |
| evtxexport | Command-line EVTX export utility from libevtx |
| LogParser | Microsoft SQL-like query engine for Windows logs |
| ausearch | Linux audit log search utility |
| jq | JSON query tool for parsing structured log formats |
| ELK Stack | Elasticsearch, Logstash, Kibana for log aggregation and visualization |
| Chainsaw | Sigma-based Windows Event Log analysis tool |
| Hayabusa | Fast Windows Event Log forensic timeline generator |

## Common Scenarios

**Scenario 1: Brute Force Attack Detection**
Filter Security.evtx for Event ID 4625 (failed logons), group by source IP and target account, identify patterns of rapid successive failures, find the successful logon (4624) that followed, trace subsequent activity from the compromised account.

**Scenario 2: Insider Threat Investigation**
Collect all log sources from the suspect's workstation and accessed servers, correlate file access events with authentication events, build timeline of data access during non-business hours, identify data transfers to external media or cloud storage.

**Scenario 3: Web Application Compromise**
Parse web server access logs for SQLi, XSS, and path traversal patterns, identify the attack IP and timeline, correlate with application logs for successful exploitation, trace post-exploitation activity through system and auth logs.

**Scenario 4: Ransomware Incident Timeline**
Identify the initial execution through process creation events (4688), trace privilege escalation through service installation (4697), map lateral movement via network logons (4624 Type 3), identify encryption start from file system activity, find the earliest IoC for remediation scoping.

## Output Format

```
Log Analysis Summary:
  Investigation Period: 2024-01-15 00:00 to 2024-01-20 23:59 UTC
  Total Events Analyzed: 894,567
  Log Sources: 6 (3 Windows, 3 Linux)

  Critical Events:
    Failed Logons:       1,234 (from 5 unique IPs)
    Successful Logons:   456 (3 anomalous)
    Account Changes:     12 (1 unauthorized admin creation)
    Process Creations:   8,234 (15 suspicious)
    Log Clearings:       2 (Security log cleared at 2024-01-18 03:00 UTC)
    Service Installs:    3 (1 unknown service)

  Attack Timeline:
    2024-01-15 14:32 - Initial access via RDP brute force
    2024-01-15 14:45 - Admin account "svcbackup" created
    2024-01-16 02:15 - Lateral movement to 3 servers
    2024-01-17 03:00 - Data staging in C:\ProgramData\temp\
    2024-01-18 01:30 - 4.2 GB exfiltrated to 185.x.x.x
    2024-01-18 03:00 - Security logs cleared

  Report: /cases/case-2024-001/analysis/log_analysis_report.txt
```