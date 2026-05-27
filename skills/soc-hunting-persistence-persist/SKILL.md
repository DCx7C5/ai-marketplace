---
name: soc-hunting-persistence-persist
description: "Soc Hunting Persistence Persist."
domain: cybersecurity
---

-|
| T1546.003 | Event Triggered Execution: WMI Event Subscription |
| __EventFilter | WMI class defining the trigger condition |
| __EventConsumer | WMI class defining the action to perform |
| __FilterToConsumerBinding | Links a filter to a consumer |
| ActiveScriptEventConsumer | Consumer that runs VBScript or JScript |
| CommandLineEventConsumer | Consumer that executes command lines |
| WmiPrvSe.exe | WMI Provider Host that executes subscription actions |
| MOF File | Managed Object Format used to define WMI objects |

## Detection Queries

### Splunk -- WMI Subscription Creation via Sysmon
```spl
index=sysmon (EventCode=19 OR EventCode=20 OR EventCode=21)
| eval event_type=case(EventCode=19, "EventFilter", EventCode=20, "EventConsumer", EventCode=21, "FilterToConsumerBinding")
| table _time Computer User event_type EventNamespace Name Query Destination Operation
```

### Splunk -- WMI Subscription via Windows Event 5861
```spl
index=wineventlog source="Microsoft-Windows-WMI-Activity/Operational" EventCode=5861
| table _time Computer NamespaceName Operation PossibleCause
```

### PowerShell -- Enumerate WMI Subscriptions
```powershell
Get-WmiObject -Namespace root\subscription -Class __EventFilter
Get-WmiObject -Namespace root\subscription -Class __EventConsumer
Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding
```

### KQL -- WmiPrvSe.exe Spawning Suspicious Children
```kql
DeviceProcessEvents
| where Timestamp > ago(7d)
| where InitiatingProcessFileName =~ "wmiprvse.exe"
| where FileName in~ ("cmd.exe", "powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe", "rundll32.exe")
| project Timestamp, DeviceName, FileName, ProcessCommandLine
```

### Sigma Rule
```yaml
title: WMI Event Subscription Persistence
status: stable
logsource:
    product: windows
    category: wmi_event
detection:
    selection_consumer:
        EventID: 20
        Destination|contains:
            - 'ActiveScriptEventConsumer'
            - 'CommandLineEventConsumer'
    condition: selection_consumer
level: high
tags:
    - attack.persistence
    - attack.t1546.003
```

## Common Scenarios

1. **APT29 WMI Persistence**: Creates an ActiveScriptEventConsumer that executes a VBScript backdoor on system startup, surviving reboots and credential resets.
2. **Turla WMI Backdoor**: Uses Win32_ProcessStartTrace filter combined with CommandLineEventConsumer for covert command execution.
3. **FIN8 WMI Timer**: Interval-based __IntervalTimerEvent triggering encoded PowerShell downloads every 30 minutes.
4. **MOF-Based Installation**: Adversary drops a .mof file and compiles it with `mofcomp.exe` to silently create persistent subscriptions.

## Output Format

```
Hunt ID: TH-WMI-[DATE]-[SEQ]
Host: [Hostname]
Subscription Name: [Filter/Consumer name]
Filter Query: [WQL trigger condition]
Consumer Type: [ActiveScript/CommandLine]
Consumer Action: [Script content or command]
Binding: [Filter-to-Consumer link]
Created: [Timestamp]
User Context: [SYSTEM/User]
Risk Level: [Critical/High/Medium/Low]
```
