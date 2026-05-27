---
name: soc-tools-splunk-configure
description: - Investigating a security incident that requires correlation across multiple log sources - Hunting for adversary activity using known TTPs and IOCs - Building detection rules for specific attack patterns - Reconstructing an incident timeline from disparate log sources - Analyzing authentication anomalies, lateral movement, or data exfiltration pat
domain: cybersecurity
---
---|------------|
| **SPL (Search Processing Language)** | Splunk's query language for searching, filtering, transforming, and visualizing machine data |
| **CIM (Common Information Model)** | Splunk's field normalization standard that maps vendor-specific field names to common names for cross-source queries |
| **Notable Event** | An event in Splunk Enterprise Security flagged for analyst review based on a correlation search match |
| **Data Model** | Structured representation of indexed data in Splunk enabling accelerated searches and pivot-based analysis |
| **Sourcetype** | Classification label in Splunk that defines the format and parsing rules for a specific log type |
| **Correlation Search** | Scheduled Splunk search that runs continuously and generates notable events when conditions are met |
| **Timechart** | SPL command that creates time-series visualizations for identifying patterns, anomalies, and trends |

## Tools & Systems

- **Splunk Enterprise Security (ES)**: Premium SIEM application providing correlation searches, risk-based alerting, and investigation workbench
- **Splunk SOAR**: Orchestration platform integrated with Splunk ES for automated response playbooks
- **Sysmon**: Microsoft system monitoring tool providing detailed process, network, and file change telemetry ingested into Splunk
- **Splunk Attack Analyzer**: Automated threat analysis that detonates suspicious files and URLs, feeding results into Splunk
- **BOSS of the SOC (BOTS)**: SANS/Splunk training dataset for practicing incident investigation SPL queries

## Common Scenarios

### Scenario: Investigating Credential Stuffing Leading to Account Takeover

**Context**: Security operations receives an alert for multiple successful logins to a single account from geographically dispersed IP addresses within a 30-minute window.

**Approach**:
1. Query Event ID 4624 for the affected account to map all login sources and times
2. Correlate login IPs against threat intelligence feeds using a Splunk lookup table
3. Check proxy logs for suspicious activity from the authenticated sessions
4. Search for lateral movement from the compromised account (Event ID 4624 Type 3 to other hosts)
5. Build a timeline showing credential stuffing attempts, successful login, and post-compromise activity
6. Create a correlation search to detect similar patterns on other accounts

**Pitfalls**:
- Searching only the last 24 hours when the credential stuffing may have occurred over weeks
- Not checking for VPN logs that may show the same account authenticating from impossible travel distances
- Failing to normalize timestamps across log sources in different time zones

## Output Format

```
SPLUNK INVESTIGATION REPORT
============================
Incident:        INC-2025-1547
Analyst:         [Name]
Investigation Period: 2025-11-14 00:00 UTC - 2025-11-16 00:00 UTC

SEARCH SCOPE
Indexes:         windows, sysmon, proxy, firewall, dns
Hosts:           WKSTN-042, SRV-FILE01
Users:           jsmith, svc-backup
Source IPs:      10.1.5.42, 10.1.10.15

KEY FINDINGS
1. [timestamp] - Initial compromise via phishing (Sysmon Event 1)
2. [timestamp] - C2 established (proxy logs, beacon pattern detected)
3. [timestamp] - Credential theft (Sysmon Event 10, LSASS access)
4. [timestamp] - Lateral movement to SRV-FILE01 (Event 4624 Type 3)
5. [timestamp] - Data staging and exfiltration (proxy bytes_out anomaly)

SPL QUERIES USED
[numbered list of key queries with descriptions]

DETECTION GAPS IDENTIFIED
- No Sysmon deployed on SRV-FILE01 (blind spot)
- Proxy logs missing SSL inspection for C2 domain
- PowerShell ScriptBlock logging not enabled

RECOMMENDED DETECTIONS
1. Correlation search for Office-spawned PowerShell
2. Threshold alert for LSASS access patterns
3. Behavioral rule for beacon-interval network traffic
```