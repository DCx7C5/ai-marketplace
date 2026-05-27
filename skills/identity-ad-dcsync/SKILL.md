---
name: identity-ad-dcsync
description: DCSync is an attack technique that abuses the Microsoft Directory Replication Service Remote Protocol (MS-DRSR) to impersonate a Domain Controller and request password data from the target DC. The attack was introduced by Benjamin Delpy (Mimikatz author) and Vincent Le Toux, leveraging the DS-Replication-Get-Changes and DS-Replication-Get-Changes-A
domain: cybersecurity
---
---|---------|----------|
| Mimikatz | DCSync extraction, Golden Ticket creation | Windows |
| secretsdump.py | Remote DCSync (Impacket) | Linux (Python) |
| ticketer.py | Golden Ticket creation (Impacket) | Linux (Python) |
| PowerView | ACL enumeration and modification | Windows (PowerShell) |
| Rubeus | Kerberos ticket manipulation | Windows (.NET) |
| ntlmrelayx.py | DCSync rights escalation via relay | Linux (Python) |

## Critical Hashes to Extract

| Account | Purpose | Persistence Value |
|---------|---------|-------------------|
| krbtgt | Golden Ticket creation | Indefinite domain access |
| Administrator | Direct DA access | Immediate privileged access |
| Service accounts | Lateral movement | Service access across domain |
| Computer accounts | Silver Ticket creation | Service-level impersonation |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| DrsGetNCChanges RPC calls from non-DC sources | Network monitoring for DRSUAPI traffic from unusual IPs |
| Event 4662 with Replicating Directory Changes GUIDs | Windows Security Log on DC (1131f6aa-/1131f6ad- GUIDs) |
| Event 4624 with Golden Ticket anomalies | Logon events with impossible SIDs or non-existent users |
| ACL modifications on domain root object | Event 5136 (directory service changes) |
| Replication traffic volume spike | Network baseline deviation monitoring |

## Validation Criteria

- [ ] Accounts with DCSync rights enumerated
- [ ] KRBTGT hash extracted via DCSync
- [ ] All domain credentials dumped successfully
- [ ] Golden Ticket forged and validated for DA access
- [ ] DCSync rights persistence mechanism established (if in scope)
- [ ] Access to Domain Controller validated with Golden Ticket
- [ ] Evidence documented with hash values and timestamps
- [ ] Remediation recommendations provided (double KRBTGT reset, ACL audit)