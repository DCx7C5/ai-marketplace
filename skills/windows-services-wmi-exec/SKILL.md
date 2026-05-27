---
name: windows-services-wmi-exec
description: "--| | Win32_Process.Create WMI calls | Event 4688 (process creation) with WMI parent process | | WMI temporary output files on ADMIN$ | File monitoring on ADMIN$ share for temp files | | Remote WMI connections (DCOM/135) | Network monitoring for DCOM traffic to workstations | | WmiPrvSE."
domain: cybersecurity
---

--|
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
