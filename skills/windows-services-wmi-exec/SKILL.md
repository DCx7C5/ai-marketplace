---
name: windows-services-wmi-exec
description: WMI (Windows Management Instrumentation) is a legitimate Windows administration framework that red teams abuse for lateral movement because it provides remote command execution without deploying additional services or leaving obvious artifacts like PsExec. Impacket's wmiexec.py creates a semi-interactive shell over WMI by executing commands through
domain: cybersecurity
---
---|---------|----------|
| wmiexec.py | Semi-interactive WMI shell (Impacket) | Linux (Python) |
| dcomexec.py | DCOM-based remote execution (Impacket) | Linux (Python) |
| CrackMapExec | Multi-target WMI execution | Linux (Python) |
| wmic.exe | Native Windows WMI command-line tool | Windows |
| PowerShell CIM | Modern WMI cmdlets | Windows |
| SharpWMI | .NET WMI execution tool | Windows (.NET) |

## WMI Execution Methods Comparison

| Method | Service Created | Output Method | Stealth Level |
|--------|----------------|---------------|---------------|
| wmiexec.py | No | Temp file on ADMIN$ | Medium |
| dcomexec.py | No | Temp file on ADMIN$ | Medium-High |
| wmic.exe | No | None (blind) or redirect | Medium |
| PowerShell WMI | No | None (blind) or redirect | High |
| PsExec (comparison) | Yes | Service output pipe | Low |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| Win32_Process.Create WMI calls | Event 4688 (process creation) with WMI parent process |
| WMI temporary output files on ADMIN$ | File monitoring on ADMIN$ share for temp files |
| Remote WMI connections (DCOM/135) | Network monitoring for DCOM traffic to workstations |
| WmiPrvSE.exe spawning cmd.exe/powershell.exe | EDR process tree analysis |
| Event 5857/5860/5861 | WMI Activity logs in Microsoft-Windows-WMI-Activity |

## Validation Criteria

- [ ] WMIExec shell established on remote target
- [ ] Pass-the-Hash execution validated via WMI
- [ ] Multi-target command execution via CrackMapExec WMI
- [ ] Native PowerShell WMI commands executed remotely
- [ ] Credential harvesting performed via WMI execution chain
- [ ] No service creation artifacts on target systems
- [ ] Evidence documented with command outputs and screenshots