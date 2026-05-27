---
name: vuln-remediation-endpoint
description: Use this skill when: - Remediating vulnerabilities identified by scanners (Nessus, Qualys, Rapid7) - Responding to zero-day CVE advisories requiring immediate patching - Maintaining compliance with patch management SLAs (critical within 14 days, high within 30 days) - Building a prioritized remediation plan from vulnerability scan results **Do not 
domain: cybersecurity
---
---|-----------|
| **CVSS** | Common Vulnerability Scoring System; 0-10 severity scale for vulnerabilities |
| **EPSS** | Exploit Prediction Scoring System; probability (0-1) that a CVE will be exploited in the wild within 30 days |
| **CISA KEV** | CISA Known Exploited Vulnerabilities catalog; federal mandate to patch these CVEs within specified timeframes |
| **SLA** | Service Level Agreement for remediation timelines based on vulnerability severity |
| **MTTR** | Mean Time To Remediate; average days from vulnerability discovery to confirmed fix |
| **Compensating Control** | Alternative security measure when direct remediation is not feasible |

## Tools & Systems

- **Nessus/Tenable.io**: Vulnerability scanning and remediation tracking
- **Qualys VMDR**: Vulnerability management, detection, and response platform
- **Rapid7 InsightVM**: Vulnerability assessment with live dashboards
- **WSUS/SCCM/Intune**: Microsoft patch deployment infrastructure
- **Automox**: Cloud-native patch management for Windows, macOS, Linux
- **CISA KEV Catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

## Common Pitfalls

- **Patching without testing**: Apply patches to a test group first. Some patches cause application compatibility issues or BSOD.
- **Ignoring EPSS scores**: A CVSS 9.8 vulnerability with EPSS 0.01 may be less urgent than a CVSS 7.5 with EPSS 0.95 (actively exploited).
- **Not validating remediation**: Deploying a patch does not guarantee installation. Always re-scan to confirm closure.
- **Excluding critical servers from patching**: Servers that "cannot be rebooted" accumulate critical vulnerabilities. Schedule maintenance windows.
- **Treating all CVEs equally**: Risk-based prioritization (CVSS + EPSS + asset criticality + exposure) is more effective than patching all criticals first.

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "endpoint" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist