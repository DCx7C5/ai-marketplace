---
name: windows-registry-artifact
description: "Windows Registry Artifact."
domain: cybersecurity
---

|
| RegRipper | Automated registry artifact extraction with plugin architecture |
| Registry Explorer | Eric Zimmerman GUI tool for interactive registry analysis |
| python-registry | Python library for programmatic registry hive parsing |
| RECmd | Eric Zimmerman command-line registry analysis tool |
| yarp | Yet Another Registry Parser for Python-based analysis |
| AppCompatCacheParser | Dedicated ShimCache/AppCompatCache parser |
| AmcacheParser | Dedicated AmCache.hve analysis tool |
| ShellBags Explorer | Specialized tool for analyzing ShellBag artifacts |

## Common Scenarios

**Scenario 1: Malware Persistence Investigation**
Extract SOFTWARE and NTUSER.DAT hives, check all Run/RunOnce keys for unauthorized entries, examine services for suspicious additions, check scheduled tasks registry keys, correlate autorun timestamps with malware execution timeline.

**Scenario 2: User Activity Reconstruction**
Analyze UserAssist for program execution history, examine RecentDocs for accessed files, check TypedPaths for Explorer navigation, extract ShellBags for folder access patterns, build a timeline of user activity around the incident window.

**Scenario 3: Unauthorized Software Detection**
Parse Uninstall keys for all installed applications, compare against approved software baseline, check BAM/DAM for recently executed programs not in approved list, examine AppCompatCache for execution evidence even after uninstallation.

**Scenario 4: USB Data Exfiltration Investigation**
Extract USBSTOR entries from SYSTEM hive for connected devices, correlate device serial numbers with MountedDevices, check NTUSER.DAT MountPoints2 for user access to removable media, examine SetupAPI logs for first-connection timestamps.

## Output Format

```
Registry Analysis Summary:
  System: DESKTOP-ABC123 (Windows 10 Pro Build 19041)
  Timezone: Eastern Standard Time (UTC-5)
  Last Shutdown: 2024-01-18 23:45:12 UTC

  Autorun Entries:
    HKLM Run:     5 entries (1 suspicious: "updater.exe" -> C:\ProgramData\svc\updater.exe)
    HKCU Run:     3 entries (all legitimate)
    Services:     142 entries (2 unknown: "WinDefSvc", "SysMonAgent")

  User Activity (NTUSER.DAT):
    UserAssist Programs:  234 entries
    Recent Documents:     89 entries
    Typed URLs:           45 entries
    Typed Paths:          12 entries

  USB Devices Connected:
    - Kingston DataTraveler (Serial: 0019E06B4521) - First: 2024-01-10, Last: 2024-01-18
    - WD My Passport (Serial: 575834314131) - First: 2024-01-15, Last: 2024-01-15

  Installed Software:     127 applications
  Suspicious Findings:    3 items flagged for review
```
