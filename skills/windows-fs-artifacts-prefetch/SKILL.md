---
name: windows-fs-artifacts-prefetch
description: - When determining which programs were executed on a Windows system and when - During malware investigations to confirm execution of suspicious binaries - For establishing a timeline of application usage during an incident - When correlating program execution with other forensic artifacts - To identify anti-forensic tools or unauthorized software t
domain: cybersecurity
---
------|-------------|
| Prefetch | Windows performance optimization that pre-loads application data and tracks execution |
| SCCA signature | Magic bytes identifying a valid Prefetch file |
| Path hash | CRC-based hash of the executable path forming part of the .pf filename |
| Run count | Number of times the executable has been launched (may wrap around) |
| Last run timestamps | Windows 8+ stores up to 8 most recent execution timestamps |
| Referenced files | List of files and directories accessed during the first 10 seconds of execution |
| Volume information | Drive serial number and creation date identifying the source volume |
| MAM compression | Windows 10 Prefetch files use MAM4 compression requiring decompression before parsing |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| PECmd | Eric Zimmerman's Prefetch parser with CSV/JSON output |
| WinPrefetchView | NirSoft GUI tool for viewing Prefetch files |
| python-prefetch | Python library for parsing Prefetch files |
| Prefetch Hash Calculator | Tool to calculate expected hash from executable paths |
| KAPE | Automated artifact collection including Prefetch |
| Autopsy | Forensic platform with Prefetch analysis module |
| Plaso/log2timeline | Super-timeline tool that includes Prefetch parser |
| Velociraptor | Endpoint agent with Prefetch collection and analysis artifacts |

## Common Scenarios

**Scenario 1: Confirming Malware Execution**
Search Prefetch directory for the malware executable name, confirm execution via Prefetch existence, extract run count and last run time, identify referenced DLLs to understand malware behavior, correlate with registry autorun entries.

**Scenario 2: Attacker Tool Usage Timeline**
Identify Prefetch files for PsExec, Mimikatz, BloodHound, and other attacker tools, build chronological timeline of tool execution, determine the sequence of the attack (reconnaissance, credential theft, lateral movement), match timestamps with network connection logs.

**Scenario 3: Data Staging and Exfiltration**
Look for Prefetch entries of compression tools (7z, WinRAR, zip), identify execution of file transfer utilities (rclone, FTP clients), check for cloud storage client execution, timeline when data staging and transfer occurred.

**Scenario 4: Anti-Forensics Detection**
Check for execution of known anti-forensic tools (CCleaner, Eraser, SDelete), identify if Prefetch directory was recently cleared (fewer files than expected for active system), note timestamps of anti-forensic tool execution relative to other evidence.

## Output Format

```
Prefetch Analysis Summary:
  System: Windows 10 Pro (Build 19041)
  Prefetch Files: 234
  Analysis Period: All available execution history

  Execution Statistics:
    Total unique executables: 234
    First execution: 2023-06-15 (system install)
    Latest execution: 2024-01-18 23:45 UTC

  Suspicious Executions:
    MIMIKATZ.EXE-5F2A3B1C.pf
      Run Count: 3 | Last: 2024-01-16 02:30:15 UTC
    PSEXEC.EXE-AD70946C.pf
      Run Count: 7 | Last: 2024-01-16 02:45:30 UTC
    RCLONE.EXE-1F3E5A2B.pf
      Run Count: 2 | Last: 2024-01-17 03:15:00 UTC
    POWERSHELL.EXE-022A1004.pf
      Run Count: 145 | Last: 2024-01-18 14:00:00 UTC

  Attack Timeline (from Prefetch):
    2024-01-15 14:32 - POWERSHELL.EXE (initial access)
    2024-01-16 02:30 - MIMIKATZ.EXE (credential theft)
    2024-01-16 02:45 - PSEXEC.EXE (lateral movement)
    2024-01-17 03:15 - RCLONE.EXE (data exfiltration)

  Report: /cases/case-2024-001/analysis/execution_timeline.csv
```