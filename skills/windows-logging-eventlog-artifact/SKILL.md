---
name: windows-logging-eventlog-artifact
description: - When investigating security incidents on Windows systems through event log analysis - For detecting lateral movement, privilege escalation, and persistence mechanisms - When performing threat hunting across Windows event log data - During compliance audits requiring review of authentication and access events - When building forensic timelines fro
domain: cybersecurity
---
------|-------------|
| EVTX format | Binary XML-based Windows Event Log format introduced in Vista/Server 2008 |
| Event ID | Numeric identifier for specific event types (e.g., 4624 = successful logon) |
| Logon types | Classification of authentication methods (2=interactive, 3=network, 10=RDP) |
| Sigma rules | Generic detection signatures that map to specific SIEM/log queries |
| Sysmon | Microsoft system monitoring driver providing detailed process and network events |
| Audit policy | GPO settings controlling which events Windows records |
| Event forwarding (WEF) | Windows mechanism for centralized event log collection |
| EVTX channels | Separate log files for different event categories and applications |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Chainsaw | Sigma-based EVTX analysis and threat hunting tool |
| Hayabusa | Fast Windows Event Log forensic timeline generator |
| EvtxECmd | Eric Zimmerman command-line EVTX parser with CSV/JSON output |
| python-evtx | Python library for EVTX file parsing |
| LogParser | Microsoft SQL-like query engine for Windows logs |
| Event Log Explorer | GUI tool for browsing and analyzing EVTX files |
| KAPE | Automated triage collection including event logs |
| Velociraptor | Endpoint agent with EVTX collection and hunting artifacts |

## Common Scenarios

**Scenario 1: Detecting Lateral Movement**
Filter for Event 4624 with Logon Type 3 (network) and Type 10 (RDP), identify unusual source-destination pairs, check for Event 4648 (explicit credentials) indicating pass-the-hash, correlate with process creation events (4688) on target systems.

**Scenario 2: Privilege Escalation Detection**
Search for Event 4672 (special privileges assigned) for unexpected users, check for Event 4728/4732 (group membership changes) adding users to admin groups, look for Event 4697 (service installed) indicating new system-level access, correlate with 4720 (account creation).

**Scenario 3: PowerShell Attack Detection**
Analyze PowerShell Operational log for Script Block Logging (Event 4104), search for encoded commands in Event 4688 (process creation with command line), detect AMSI bypass attempts, identify download cradles and invocation of known attack tools.

**Scenario 4: Ransomware Incident Reconstruction**
Build timeline starting from initial access (4624 from external IP), trace privilege escalation through group membership changes, identify service installations for persistence, find process creation events for encryption executable, detect volume shadow copy deletion in System log.

## Output Format

```
Windows Event Log Analysis Summary:
  System: DC01.corp.local (Windows Server 2019)
  Log Files Analyzed: 15 EVTX files
  Total Events: 2,456,789
  Analysis Period: 2024-01-10 to 2024-01-20

  Chainsaw Detections:
    Critical:  12 (Mimikatz usage, PsExec, log clearing)
    High:      34 (Network NTLM logons, encoded PowerShell)
    Medium:    89 (Unusual service installations, scheduled tasks)
    Low:       234 (Informational)

  Hayabusa Timeline:
    Total Alerts: 369
    Unique Rules Triggered: 45
    Top Rules:
      - Suspicious NTLM Authentication (34 hits)
      - PowerShell Download Cradle (12 hits)
      - Service Installation Suspicious Path (8 hits)

  Critical Findings:
    2024-01-15 14:32 - RDP brute force (234 failed, 1 success from 203.0.113.45)
    2024-01-15 14:45 - Admin account created (svcbackup) - Event 4720
    2024-01-16 02:30 - PsExec service installed on DC01 - Event 4697
    2024-01-18 03:00 - Security log cleared - Event 1102

  Reports:
    Chainsaw: /analysis/chainsaw_results/
    Hayabusa: /analysis/hayabusa_timeline.csv
    Critical Events: /analysis/critical_events.json
```