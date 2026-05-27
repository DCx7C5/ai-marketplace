---
name: soc-splunk-detectionrules
description: "| | T1110.001 | Password Guessing | Threshold on EventCode 4625 by src_ip | | T1059."
domain: cybersecurity
---

|
| T1110.001 | Password Guessing | Threshold on EventCode 4625 by src_ip |
| T1059.001 | PowerShell | Pattern match on EventCode 4104 ScriptBlockText |
| T1021.002 | SMB/Windows Admin Shares | Logon Type 3 with dc(dest) threshold |
| T1048 | Exfiltration Over C2 | bytes_out aggregation over time window |
| T1053.005 | Scheduled Task | EventCode 4698 with suspicious command patterns |
| T1003.001 | LSASS Memory | Process access to lsass.exe via Sysmon EventCode 10 |

## References

- [Splunk ES Correlation Searches Best Practices](https://detect.fyi/splunk-es-correlation-searches-rules-best-cool-practices-06ef94884170)
- [Writing Practical Splunk Detection Rules](https://medium.com/@vitbukac/practical-splunk-detection-rules-how-to-part-1-crawl-a24bc39a4b9d)
- [Configure Correlation Searches - Splunk Documentation](https://help.splunk.com/en/splunk-enterprise-security-8/splunk-app-for-pci-compliance/installation-and-configuration-manual/6.1/configure-correlation-searches/configure-correlation-searches)
- [SOC Prime - Correlation Events in Splunk](https://socprime.com/blog/creating-correlation-events-in-splunk-using-alerts/)
