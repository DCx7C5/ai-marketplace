---
name: net-lateralmovement-detectionsplunk
description: "Net Lateralmovement Detectionsplunk."
domain: cybersecurity
---

|
| Splunk Enterprise | SIEM for log aggregation and SPL queries |
| Splunk Enterprise Security | Threat detection and notable events |
| Windows Event Forwarding | Centralize Windows logs |
| Sysmon | Detailed process and network telemetry |
| BloodHound | AD attack path analysis |
| PingCastle | AD security assessment |

## Common Scenarios

1. **PsExec Lateral Movement**: Adversary uses PsExec to execute commands on remote systems via SMB, generating Type 3 logon with ADMIN$ share access.
2. **RDP Pivoting**: Attacker RDPs to internal systems using stolen credentials, creating Type 10 logon events.
3. **WMI Remote Execution**: Adversary uses WMIC process call create to spawn processes on remote hosts.
4. **WinRM PowerShell Remoting**: Attacker uses Enter-PSSession or Invoke-Command to execute code on remote systems.
5. **Pass-the-Hash via SMB**: Compromised NTLM hashes used to authenticate to remote systems without knowing the plaintext password.

## Output Format

```
Hunt ID: TH-LATMOV-[DATE]-[SEQ]
Movement Type: [RDP/SMB/WinRM/WMI/DCOM/PsExec]
Source Host: [Hostname/IP]
Destination Host: [Hostname/IP]
Account Used: [Username]
Logon Type: [3/10/other]
First Seen: [Timestamp]
Event Count: [Number of events]
Risk Level: [Critical/High/Medium/Low]
Lateral Movement Path: [A -> B -> C -> D]
```
