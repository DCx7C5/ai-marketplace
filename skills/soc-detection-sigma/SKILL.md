---
name: soc-detection-sigma
description: "Soc Detection Sigma."
domain: cybersecurity
---

--|
| **Sigma** | Vendor-agnostic detection rule format (YAML-based) that compiles to SIEM-specific queries via backends |
| **pySigma** | Python library replacing legacy sigmac for rule conversion, validation, and pipeline processing |
| **Backend** | pySigma plugin that translates Sigma detection logic into a target platform query language (SPL, KQL, Lucene) |
| **Pipeline** | Field mapping configuration that translates generic Sigma field names to SIEM-specific field names |
| **Logsource** | Sigma rule section defining the category (process_creation, network_connection) and product (windows, linux) of the target data |
| **Detection-as-Code** | Practice of managing detection rules in version control with CI/CD testing and automated deployment |

## Tools & Systems

- **SigmaHQ**: Official Sigma rule repository with 3,000+ community-maintained detection rules on GitHub
- **pySigma**: Python-based Sigma rule processing framework with modular backends and pipelines
- **ATT&CK Navigator**: MITRE tool for visualizing detection coverage mapped to ATT&CK techniques
- **Uncoder.IO**: Web-based Sigma rule converter supporting 30+ SIEM platforms for quick translation

## Common Scenarios

- **New CVE Detection**: Write Sigma rule for exploitation indicators (e.g., Log4Shell JNDI lookup patterns in web logs)
- **Hunting Rule Promotion**: Convert ad-hoc Splunk hunting query into Sigma rule for ongoing automated detection
- **Multi-SIEM Migration**: Converting 500+ Splunk correlation searches to Sigma for migration to Elastic Security
- **Purple Team Output**: Convert red team findings into Sigma rules for immediate defensive coverage
- **Threat Intel Operationalization**: Transform IOC-based threat reports into behavioral Sigma rules

## Output Format

```
SIGMA RULE DEPLOYMENT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rule ID:      0d894093-71bc-43c3-8d63-bf520e73a7c5
Title:        Mimikatz Credential Dumping via LSASS Access
ATT&CK:       T1003.001 - LSASS Memory
Severity:     High
Status:       Deployed to Production

Conversions:
  Splunk SPL:    PASS — Saved search "sigma_lsass_access" created
  Elastic EQL:   PASS — Detection rule ID elastic-0d894093 enabled
  Sentinel KQL:  PASS — Analytics rule deployed via ARM template

Testing:
  True Positives:    4/4 test cases matched
  False Positives:   2 in 7-day backtest (svchost edge case — filter added)
  Performance:       Avg execution 3.2s on 50M events/day
```
