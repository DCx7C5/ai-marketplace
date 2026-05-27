---
name: soc-hunting-lateralmov
description: Distributed Component Object Model (DCOM) enables remote execution of COM objects across a network using RPC. Adversaries abuse specific DCOM objects -- MMC20.Application (CLSID {49B2791A-B1AE-4C90-9B8E-E860BA07F889}), ShellBrowserWindow (CLSID {C08AFD90-F2A1-11D1-8455-00A0C91F3880}), and ShellWindows (CLSID {9BA05972-F6A8-11CF-A442-00A0C90A8F39}) 
domain: cybersecurity
---
---|------------|
| **DCOM (T1021.003)** | Distributed Component Object Model -- extends COM to allow remote object instantiation and method invocation over RPC, abused for lateral movement |
| **MMC20.Application** | COM object (CLSID {49B2791A-B1AE-4C90-9B8E-E860BA07F889}) controlling MMC snap-ins; `ExecuteShellCommand` method enables remote command execution |
| **ShellWindows** | COM object (CLSID {9BA05972-F6A8-11CF-A442-00A0C90A8F39}) that activates within an existing explorer.exe process, executing commands without creating a new COM server process |
| **ShellBrowserWindow** | COM object (CLSID {C08AFD90-F2A1-11D1-8455-00A0C91F3880}) similar to ShellWindows, uses `Document.Application.ShellExecute` for stealthy command execution |
| **RPC Endpoint Mapper** | Service on TCP port 135 that maps RPC interfaces to dynamic ports; all DCOM communication begins with an endpoint mapper query |
| **Sysmon Event ID 1** | Process Create event capturing parent-child process relationships, command lines, and user context -- critical for identifying DCOM-spawned processes |
| **Sysmon Event ID 3** | Network Connection event capturing source/destination IPs and ports -- used to correlate RPC connections with subsequent process creation |
| **DcomLaunch** | Windows service (svchost.exe -k DcomLaunch) that manages DCOM server process activation; parent process of COM servers spawned via remote DCOM calls |
| **WMI-Activity ETW** | Event Tracing for Windows provider that logs WMI method calls, instance creations, and queries -- provides visibility into DCOM-triggered WMI operations |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Sysmon** | Endpoint telemetry for process creation (EID 1), network connections (EID 3), and image loads (EID 7) essential for DCOM detection |
| **Splunk / Elastic SIEM** | Log aggregation and correlation platform for DCOM detection rules and threat hunting queries |
| **Microsoft Sentinel** | Cloud SIEM with built-in KQL queries and analytics rules for DCOM lateral movement detection |
| **Sigma** | Vendor-agnostic detection rule format for portable DCOM detection rules |
| **Zeek** | Network security monitor for DCE-RPC protocol analysis and RPC endpoint mapper traffic monitoring |
| **Atomic Red Team** | MITRE ATT&CK test framework with T1021.003 atomics for validating DCOM detection coverage |
| **Impacket (dcomexec.py)** | Python-based DCOM execution tool used by attackers and red teamers for testing DCOM lateral movement |
| **CIMSession / PowerShell** | Native Windows tooling for DCOM object instantiation used in both legitimate administration and attacks |

## Common Scenarios

### Scenario 1: MMC20.Application Lateral Movement to File Server

**Context**: A SOC analyst receives an alert for mmc.exe spawning cmd.exe on a file server (10.10.20.50) at 03:22 UTC. No administrator activity is scheduled at this time.

**Approach**:
1. Query Sysmon Event ID 1 on 10.10.20.50: confirm mmc.exe (parent: svchost.exe -k DcomLaunch) spawned cmd.exe with command line `/c net user /domain > C:\temp\users.txt`
2. Query Sysmon Event ID 3 on 10.10.20.50: identify inbound TCP connection on port 135 from 10.10.5.30 at 03:22:01, followed by a high-port connection at 03:22:02
3. Correlate Event ID 4624 on 10.10.20.50: find LogonType 3 from 10.10.5.30 at 03:22:00 with admin credentials
4. Investigate 10.10.5.30: check for compromise indicators -- find Mimikatz artifacts in memory, evidence of credential dumping at 03:15
5. Trace the attack chain: initial phishing compromise at 02:45, credential theft at 03:15, DCOM lateral movement at 03:22
6. Contain: isolate 10.10.5.30 and 10.10.20.50, force password reset for compromised admin account, block inbound RPC from non-admin subnets

**Pitfalls**:
- Dismissing mmc.exe activity as legitimate MMC administration without checking the parent process and command line
- Not correlating the network logon (4624) with the process creation to identify the true source host
- Failing to investigate the source host for initial compromise indicators

### Scenario 2: ShellWindows Stealthy Lateral Movement

**Context**: During a threat hunt, an analyst queries for explorer.exe spawning cmd.exe on domain controllers and finds several instances on DC01 with no interactive logon sessions.

**Approach**:
1. Verify no interactive sessions: query Event ID 4624 LogonType 2 or 10 on DC01 -- none found during the time window
2. Query Sysmon Event ID 1: explorer.exe spawning cmd.exe with encoded PowerShell commands at 14:05, 14:12, and 14:18
3. Decode the PowerShell: reveals reconnaissance commands (Get-ADUser, Get-ADGroup, Get-ADComputer)
4. Query Sysmon Event ID 3: inbound RPC connections from 10.10.3.15 preceding each process creation
5. Identify the ShellWindows pattern: no new mmc.exe or dllhost.exe process created -- commands execute through existing explorer.exe, consistent with ShellWindows/ShellBrowserWindow DCOM abuse
6. Investigate 10.10.3.15: compromised workstation with Cobalt Strike beacon artifacts

**Pitfalls**:
- Missing the attack because ShellWindows does not create a separate COM server process -- requires monitoring explorer.exe child processes
- Not having Sysmon Event ID 3 configured to capture network connections from explorer.exe
- Filtering out explorer.exe as a legitimate parent process without considering the server context

## Output Format

```
Hunt ID: TH-DCOM-[DATE]-[SEQ]
Alert Severity: High
MITRE Technique: T1021.003 (Remote Services: DCOM)

Source Host: [IP/Hostname of attacker's machine]
Target Host: [IP/Hostname where DCOM executed]
DCOM Object: [MMC20.Application | ShellWindows | ShellBrowserWindow]
CLSID: [COM object class identifier]

Process Chain:
  Parent: [svchost.exe -k DcomLaunch | explorer.exe | mmc.exe]
  Child:  [cmd.exe | powershell.exe | ...]
  Command Line: [Full command executed]

Network Indicators:
  RPC Connection: [Source IP]:port -> [Target IP]:135 at [timestamp]
  DCOM Port: [Source IP]:port -> [Target IP]:[high-port] at [timestamp]

Authentication Context:
  Event 4624: LogonType 3 from [Source IP] at [timestamp]
  Account: [Domain\Username]
  Logon ID: [Logon session identifier]

Risk Assessment: [Critical/High/Medium]
Recommended Action: [Isolate, investigate source, reset credentials, restrict DCOM]
```