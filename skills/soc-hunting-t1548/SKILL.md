---
name: soc-hunting-t1548
description: - When hunting for privilege escalation via UAC bypass in Windows environments - After threat intelligence indicates use of UAC bypass exploits by active threat groups - When investigating how attackers achieved administrative access without triggering UAC prompts - During security assessments to validate UAC bypass detection coverage - When monito
domain: cybersecurity
---
------|-------------|
| T1548.002 | Bypass User Account Control |
| T1548.001 | Setuid and Setgid (Linux) |
| T1548.003 | Sudo and Sudo Caching |
| T1548.004 | Elevated Execution with Prompt (macOS) |
| UAC Auto-Elevation | Windows binaries that elevate without prompt |
| fodhelper.exe | Common UAC bypass vector via registry hijack |
| eventvwr.exe | MSC file handler UAC bypass |
| Integrity Level | Windows process trust level (Low/Medium/High/System) |

## Detection Queries

### Splunk -- UAC Bypass via Registry Modification
```spl
index=sysmon (EventCode=12 OR EventCode=13)
| where match(TargetObject, "(?i)HKCU\\\\Software\\\\Classes\\\\(ms-settings|mscfile|exefile|Folder)\\\\shell\\\\open\\\\command")
| table _time Computer User EventCode TargetObject Details Image
```

### Splunk -- Auto-Elevating Process Abuse
```spl
index=sysmon EventCode=1
| where match(Image, "(?i)(fodhelper|computerdefaults|eventvwr|sdclt|slui|cmstp)\.exe$")
| where NOT match(ParentImage, "(?i)(explorer|svchost|services)\.exe$")
| table _time Computer User Image CommandLine ParentImage ParentCommandLine
```

### KQL -- UAC Bypass Detection
```kql
DeviceRegistryEvents
| where Timestamp > ago(7d)
| where RegistryKey has_any ("ms-settings\\shell\\open\\command", "mscfile\\shell\\open\\command")
| where ActionType == "RegistryValueSet"
| project Timestamp, DeviceName, RegistryKey, RegistryValueData, InitiatingProcessFileName
```

### Sigma Rule
```yaml
title: UAC Bypass via Registry Modification
status: stable
logsource:
    product: windows
    category: registry_set
detection:
    selection:
        TargetObject|contains:
            - '\ms-settings\shell\open\command'
            - '\mscfile\shell\open\command'
            - '\exefile\shell\open\command'
    condition: selection
level: high
tags:
    - attack.privilege_escalation
    - attack.t1548.002
```

## Common Scenarios

1. **fodhelper.exe Registry Hijack**: Attacker sets `HKCU\Software\Classes\ms-settings\shell\open\command` to a malicious executable, then launches fodhelper.exe which auto-elevates and executes the hijacked command.
2. **eventvwr.exe MSC Bypass**: Modifying `HKCU\Software\Classes\mscfile\shell\open\command` to intercept Event Viewer's auto-elevation behavior.
3. **sdclt.exe Bypass**: Leveraging the Windows Backup utility's auto-elevation to execute arbitrary commands.
4. **CMSTP.exe INF Bypass**: Using Connection Manager Profile Installer with a malicious INF file to bypass UAC via `/s /ni` flags.
5. **DLL Hijacking in Auto-Elevate**: Placing malicious DLLs in search paths of auto-elevating executables.

## Output Format

```
Hunt ID: TH-UAC-[DATE]-[SEQ]
Host: [Hostname]
Bypass Method: [Registry hijack/DLL hijack/Token manipulation]
Auto-Elevate Binary: [fodhelper.exe/eventvwr.exe/etc.]
Registry Key Modified: [Full registry path]
Payload Executed: [Command or binary path]
User Context: [Account]
Risk Level: [Critical/High/Medium]
ATT&CK Technique: [T1548.00x]
```