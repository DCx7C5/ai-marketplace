---
name: net-lateralmovement-detectionsplunk
description: - When hunting for adversary movement between compromised systems - After detecting credential theft to trace subsequent lateral activity - When investigating unusual authentication patterns across the network - During incident response to scope the breadth of compromise - When proactively hunting for TA0008 (Lateral Movement) techniques
domain: cybersecurity
---
------|-------------|
| T1021 | Remote Services (parent technique) |
| T1021.001 | Remote Desktop Protocol (RDP) |
| T1021.002 | SMB/Windows Admin Shares |
| T1021.003 | Distributed COM (DCOM) |
| T1021.004 | SSH |
| T1021.006 | Windows Remote Management (WinRM) |
| T1570 | Lateral Tool Transfer |
| T1047 | Windows Management Instrumentation |
| T1569.002 | Service Execution (PsExec) |
| Logon Type 3 | Network logon (SMB, WinRM, mapped drives) |
| Logon Type 10 | Remote Interactive (RDP) |
| Event ID 4624 | Successful logon |
| Event ID 4648 | Explicit credential logon (runas, PsExec) |

## Tools & Systems

| Tool | Purpose |
|------|---------|
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