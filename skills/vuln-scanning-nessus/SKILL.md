---
name: vuln-scanning-nessus
description: - Conducting initial vulnerability assessment during the reconnaissance phase of a penetration test - Performing periodic vulnerability scans to maintain compliance with PCI-DSS (requirement 11.2), HIPAA, or SOC 2 standards - Validating that remediation efforts have successfully addressed previously identified vulnerabilities - Establishing a basel
domain: cybersecurity
---
---|------------|
| **Authenticated Scan** | A vulnerability scan that uses valid credentials to log into target hosts and perform local checks, detecting significantly more vulnerabilities than unauthenticated scanning |
| **Plugin** | A Nessus script that checks for a specific vulnerability, misconfiguration, or compliance item; Nessus maintains over 200,000 plugins updated daily |
| **CVSS** | Common Vulnerability Scoring System; a standardized framework for rating the severity of vulnerabilities from 0.0 to 10.0 based on exploitability and impact metrics |
| **False Positive** | A vulnerability reported by the scanner that does not actually exist on the target, often caused by version-based detection without exploit verification |
| **Credentialed Patch Audit** | A scan type focused specifically on identifying missing operating system and application patches by comparing installed versions against known vulnerability databases |
| **Plugin Family** | A logical grouping of Nessus plugins by category (e.g., Windows, Ubuntu Local Security Checks, Web Servers, Databases) |

## Tools & Systems

- **Nessus Professional**: Commercial vulnerability scanner by Tenable with over 200,000 plugins covering CVEs, misconfigurations, and compliance checks
- **Nessus Expert**: Extended version including external attack surface scanning, IaC scanning, and cloud infrastructure assessment
- **Tenable.io**: Cloud-hosted vulnerability management platform for enterprise deployments with asset tracking, trend analysis, and prioritization
- **OpenVAS (Greenbone)**: Open-source alternative vulnerability scanner with community-maintained vulnerability tests for comparison scanning

## Common Scenarios

### Scenario: Quarterly PCI-DSS Vulnerability Scan for a Retail Company

**Context**: A retailer processes credit card payments and must comply with PCI-DSS requirement 11.2, which mandates quarterly internal and external vulnerability scans. The cardholder data environment (CDE) consists of 200 servers across 3 VLANs. All hosts run either Windows Server 2019/2022 or RHEL 8/9.

**Approach**:
1. Configure authenticated scan with domain service account for Windows and SSH key for Linux hosts
2. Use the PCI-DSS scan policy template with all relevant plugin families enabled
3. Scan all 200 CDE hosts during the Saturday maintenance window (02:00-06:00)
4. Identify 847 findings: 12 Critical, 34 High, 189 Medium, 612 Low/Informational
5. Validate Critical findings: 3 are false positives (backported patches on RHEL), 9 are confirmed vulnerabilities
6. Group remaining findings by remediation action: 6 require Windows patches, 2 require Apache upgrades, 1 requires TLS configuration hardening
7. Generate PCI-compliant report showing no Critical or High vulnerabilities remain unaddressed (after remediation and rescan)

**Pitfalls**:
- Running unauthenticated scans and missing the majority of local vulnerabilities, producing an incomplete compliance report
- Not updating Nessus plugins before scanning, missing recently published CVEs
- Scanning fragile legacy systems without reducing scan intensity, causing crashes or service disruption
- Accepting Nessus results at face value without manually validating critical findings for false positives

## Output Format

```
## Vulnerability Scan Summary - CDE Environment

**Scan Date**: 2025-11-15 02:00-05:47 UTC
**Scanner**: Nessus Professional 10.8.3 (Plugins: 2025-11-14)
**Hosts Scanned**: 200 (198 authenticated, 2 authentication failed)
**Scan Policy**: PCI-DSS Internal Scan

### Findings Summary
| Severity | Count | Validated |
|----------|-------|-----------|
| Critical | 12    | 9 (3 FP)  |
| High     | 34    | 31 (3 FP) |
| Medium   | 189   | 178       |
| Low/Info | 612   | N/A       |

### Top Critical Findings

**1. CVE-2024-21762 - Fortinet FortiOS Out-of-Bounds Write (CVSS 9.8)**
- Affected Hosts: fw-cde-01.corp.example.com (10.50.1.1)
- Exploit Available: Yes (Metasploit module)
- Remediation: Upgrade FortiOS to 7.4.3 or later
- Priority: Immediate - internet-facing device protecting CDE

**2. CVE-2024-6387 - OpenSSH regreSSHion (CVSS 8.1)**
- Affected Hosts: 14 Linux servers (see Appendix A)
- Exploit Available: Yes (public PoC)
- Remediation: Upgrade OpenSSH to 9.8p1 or later
- Priority: Within 7 days - authenticated remote code execution
```

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "nessus" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist