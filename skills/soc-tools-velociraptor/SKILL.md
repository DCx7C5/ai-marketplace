---
name: soc-tools-velociraptor
description: Velociraptor is an advanced open-source endpoint monitoring, digital forensics, and incident response platform developed by Rapid7. It uses the Velociraptor Query Language (VQL) to create custom artifacts that collect, query, and monitor almost any aspect of an endpoint. Velociraptor enables incident response teams to rapidly collect and examine fo
domain: cybersecurity
---
--------|-------------|
| T1059 - Command Scripting | Windows.EventLogs.EvtxHunter (4104, 4688) |
| T1053 - Scheduled Task | Windows.System.TaskScheduler |
| T1547 - Boot/Logon Autostart | Windows.Persistence.PermanentWMIEvents |
| T1003 - OS Credential Dumping | Windows.Detection.Yara.Process |
| T1021 - Remote Services | Windows.EventLogs.EvtxHunter (4624 Type 3/10) |
| T1070 - Indicator Removal | Windows.EventLogs.Cleared |

## References

- [Velociraptor Official Documentation](https://docs.velociraptor.app/)
- [Rapid7 Velociraptor Product Page](https://www.rapid7.com/products/velociraptor/)
- [CISA Velociraptor Resource](https://www.cisa.gov/resources-tools/services/velociraptor)
- [Velociraptor GitHub Repository](https://github.com/Velocidex/velociraptor)
- [Pen Test Partners: Large-Scale Velociraptor](https://www.pentestpartners.com/security-blog/using-velociraptor-for-large-scale-endpoint-visibility-and-rapid-threat-hunting/)