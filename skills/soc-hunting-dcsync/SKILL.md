---
name: soc-hunting-dcsync
description: - When hunting for DCSync credential theft (MITRE ATT&CK T1003.006) - After detecting Mimikatz or similar tools in the environment - During incident response involving Active Directory compromise - When monitoring for unauthorized domain replication requests - During purple team exercises testing AD attack detection
domain: cybersecurity
---
------|-------------|
| DCSync | Technique abusing AD replication protocol to extract password hashes |
| Event ID 4662 | Directory Service Access audit event |
| DS-Replication-Get-Changes | GUID 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2 |
| DS-Replication-Get-Changes-All | GUID 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2 |
| AccessMask 0x100 | Control Access right indicating extended rights verification |
| T1003.006 | OS Credential Dumping: DCSync |

## Tools & Systems

| Tool | Purpose |
|------|---------|
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