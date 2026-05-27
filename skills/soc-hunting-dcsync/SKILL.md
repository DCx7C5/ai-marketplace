---
name: soc-hunting-dcsync
description: "| | Windows Event Viewer | Direct event log analysis | | Splunk | SIEM correlation of Event 4662 | | Elastic Security | Detection rules for DCSync patterns | | Mimikatz lsadump::dcsync | Attack tool used to perform DCSync | | Impacket secretsdump."
domain: cybersecurity
---

|
| Windows Event Viewer | Direct event log analysis |
| Splunk | SIEM correlation of Event 4662 |
| Elastic Security | Detection rules for DCSync patterns |
| Mimikatz lsadump::dcsync | Attack tool used to perform DCSync |
| Impacket secretsdump.py | Python-based DCSync implementation |
| BloodHound | Identify accounts with replication rights |

## Output Format

```
Hunt ID: TH-DCSYNC-[DATE]-[SEQ]
Technique: T1003.006
Domain Controller: [DC hostname]
Subject Account: [Account performing replication]
Source IP: [Non-DC IP address]
GUID Accessed: [Replication GUID]
Risk Level: [Critical/High/Medium/Low]
Recommended Action: [Disable account, reset krbtgt, investigate]
```
