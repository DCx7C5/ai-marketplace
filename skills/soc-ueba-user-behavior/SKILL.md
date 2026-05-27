---
name: soc-ueba-user-behavior
description: Use this skill when: - SOC teams need to detect compromised accounts through abnormal authentication patterns - Insider threat programs require behavioral monitoring beyond rule-based detection - Impossible travel or geographic anomalies indicate credential compromise - Privileged account monitoring requires baseline deviation detection **Do not us
domain: cybersecurity
---
---|-----------|
| **UEBA** | User and Entity Behavior Analytics — behavioral analysis detecting anomalies against established baselines |
| **Impossible Travel** | Login events from geographically distant locations within timeframes making physical travel impossible |
| **Behavioral Baseline** | Statistical profile of normal user activity patterns built from 30-90 days of historical data |
| **Z-Score** | Statistical measure of how many standard deviations an observation is from the mean — values > 3 indicate anomalies |
| **Risk Score** | Composite numerical score aggregating multiple behavioral anomalies weighted by asset criticality |
| **Peer Group Analysis** | Comparing a user's behavior to others in the same department/role to identify outliers |

## Tools & Systems

- **Splunk UBA**: Dedicated User Behavior Analytics module integrating with Splunk ES for ML-driven anomaly detection
- **Microsoft Sentinel UEBA**: Built-in UEBA capability in Azure Sentinel with entity pages and investigation graphs
- **Exabeam Advanced Analytics**: Standalone UEBA platform with session stitching and automatic timeline creation
- **Securonix**: Cloud-native SIEM/UEBA with pre-built behavioral models for insider threat detection

## Common Scenarios

- **Compromised Account**: Impossible travel + off-hours login + unusual app access = likely credential compromise
- **Insider Data Theft**: Employee accessing 10x normal file volume in notice period before departure
- **Privilege Escalation Abuse**: Admin account used from unusual location accessing systems outside normal scope
- **Shared Account Detection**: Service account logging in from multiple geographies simultaneously
- **Dormant Account Reactivation**: Account with no activity for 90+ days suddenly performing privileged operations

## Output Format

```
UEBA ANOMALY REPORT — Weekly Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Period:       2024-03-11 to 2024-03-17
Users Baselined:  2,847
Anomalies Detected: 23

TOP RISK USERS:
#  User          Dept       Risk   Anomalies
1. jsmith        Finance    94.5   Impossible travel (NYC->Moscow, 2h), off-hours access, 15GB download
2. admin_svc01   IT Ops     82.0   Login from 12 new IPs, 47 hosts accessed (baseline: 8)
3. mwilson       HR         67.3   Off-hours file access (2AM), 3x normal download volume

INVESTIGATION STATUS:
  jsmith:      Escalated to Tier 2 — possible account compromise (IR-2024-0445)
  admin_svc01: Under review — may be new automation deployment (checking with IT Ops)
  mwilson:     Pending HR context — employee on notice period, monitoring increased
```