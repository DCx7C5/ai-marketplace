---
name: windows-logs-eventlog
description: Use this skill when: - Configuring Windows Advanced Audit Policy for security monitoring - Enabling process creation auditing with command line logging (Event 4688) - Setting up logon/logoff auditing for authentication monitoring - Sizing event log storage and forwarding to SIEM platforms **Do not use** for Sysmon configuration (separate skill) or 
domain: cybersecurity
---
---|-----------|
| **Advanced Audit Policy** | Granular audit subcategories (58 subcategories vs. 9 basic categories) |
| **Event ID 4688** | Process creation event; essential for tracking execution on endpoints |
| **WEF** | Windows Event Forwarding; centralized log collection without third-party agents |
| **Logon Type** | Numeric code indicating authentication method (2=interactive, 3=network, 10=RDP) |

## Tools & Systems

- **Windows Event Forwarding (WEF)**: Built-in centralized log collection
- **NXLog**: Open-source log forwarding agent for Windows events
- **Winlogbeat**: Elastic Agent for shipping Windows event logs to Elasticsearch
- **Palantir WEF Configuration**: Open-source WEF subscription templates

## Common Pitfalls

- **Using basic audit policy instead of advanced**: Basic and advanced audit policies conflict. Always use advanced audit policy exclusively.
- **Default log size too small**: 20 MB Security log fills in minutes on busy servers. Set minimum 1 GB.
- **Missing command line logging**: Event 4688 without command line content has minimal detection value. Always enable ProcessCreationIncludeCmdLine_Enabled.
- **Not forwarding logs**: Local event logs are lost when endpoints are wiped by ransomware. Forward to centralized SIEM immediately.