---
name: windows-logging-splunk
description: Use this skill when: - SOC analysts investigate alerts related to Windows authentication, process execution, or AD changes - Detection engineers build SPL queries for Windows-based threat detection - Incident responders need forensic timelines of Windows endpoint or domain controller activity - Periodic threat hunting targets Windows-specific ATT&C
domain: cybersecurity
---
---|-----------|
| **EventCode 4624** | Successful logon event — Logon_Type 2 (interactive), 3 (network), 10 (RDP), 7 (unlock) |
| **EventCode 4625** | Failed logon event — Status code indicates failure reason (bad password, account locked, disabled) |
| **Sysmon EventCode 1** | Process creation with full command line, parent process, and hash information |
| **Sysmon EventCode 3** | Network connection initiated by a process — source/dest IP, port, and process context |
| **Logon Type 3** | Network logon (SMB, WMI, PowerShell Remoting) — key indicator of lateral movement |
| **Logon Type 10** | Remote interactive logon via RDP/Terminal Services |

## Tools & Systems

- **Splunk Enterprise**: SIEM platform with SPL query engine for Windows event log analysis and correlation
- **Sysmon (System Monitor)**: Microsoft Sysinternals tool providing detailed process, network, and file activity logging
- **Splunk CIM**: Common Information Model mapping Windows events to normalized fields for cross-source queries
- **Windows Event Forwarding (WEF)**: Built-in Windows mechanism for centralizing event logs to a collector server

## Common Scenarios

- **Kerberoasting (T1558.003)**: Detect EventCode 4769 with encryption type 0x17 (RC4) for non-standard service accounts
- **DCSync (T1003.006)**: Detect EventCode 4662 with DS-Replication-Get-Changes from non-DC sources
- **Golden Ticket (T1558.001)**: Detect EventCode 4769 with abnormal ticket properties (long lifetime, non-standard encryption)
- **Pass-the-Hash (T1550.002)**: Detect EventCode 4624 Logon_Type 3 with NTLM authentication from unexpected sources
- **DLL Side-Loading (T1574.002)**: Sysmon EventCode 7 showing unsigned DLLs loaded by legitimate processes

## Output Format

```
WINDOWS EVENT LOG ANALYSIS — HOST: WORKSTATION-042
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Period:     2024-03-14 to 2024-03-15
Events:     12,847 total (Security: 9,231 | Sysmon: 3,616)

Authentication Summary:
  Successful Logons (4624):    487 (Type 3: 312, Type 10: 45, Type 2: 130)
  Failed Logons (4625):        847 (from 192.168.1.105 — BRUTE FORCE)
  Explicit Creds (4648):       12

Suspicious Findings:
  [HIGH]   847 failed logons followed by success at 14:35 from 192.168.1.105
  [HIGH]   New user "backdoor_admin" created (4720) at 14:38
  [HIGH]   User added to Administrators group (4732) at 14:38
  [MEDIUM] schtasks.exe creating persistence task at 14:42
  [MEDIUM] PowerShell encoded command execution at 14:45

ATT&CK Mapping:
  T1110.001 — Password Guessing (847 failed logons)
  T1136.001 — Local Account Creation (backdoor_admin)
  T1053.005 — Scheduled Task (persistence)
  T1059.001 — PowerShell (encoded execution)
```