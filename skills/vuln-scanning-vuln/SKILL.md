---
name: vuln-scanning-vuln
description: Use this skill when: - SOC teams need to establish or improve recurring vulnerability scanning programs - Scan results require prioritization beyond raw CVSS scores using asset context and threat intelligence - Vulnerability data must be integrated into SIEM for correlation with exploitation attempts - Remediation tracking needs formalization with 
domain: cybersecurity
---
-------|-----------|------------|-----|---------|
| **P1 Critical** | 9.0-10.0 + KEV | All assets | 24 hours | Log4Shell, EternalBlue on prod servers |
| **P2 High** | 7.0-8.9 or 9.0+ non-KEV | Business-critical | 7 days | RCE without known exploit |
| **P3 Medium** | 4.0-6.9 | Business-critical | 30 days | Authenticated privilege escalation |
| **P4 Low** | 0.1-3.9 | Standard | 90 days | Information disclosure, low-impact DoS |
| **P5 Informational** | 0.0 | Development | Next cycle | Best practice findings, config hardening |

### Step 4: Integrate with SIEM for Exploitation Detection

Correlate vulnerability scan data with SIEM alerts to detect active exploitation:

```spl
index=vulnerability sourcetype="nessus:scan"
| eval vuln_key = Host.":".CVE
| join vuln_key type=left [
    search index=ids_ips sourcetype="snort" OR sourcetype="suricata"
    | eval vuln_key = dest_ip.":".cve_id
    | stats count AS exploit_attempts, latest(_time) AS last_exploit_attempt by vuln_key
  ]
| where isnotnull(exploit_attempts)
| eval risk = "CRITICAL — Vulnerability being actively exploited"
| sort - exploit_attempts
| table Host, CVE, plugin_name, cvss_score, exploit_attempts, last_exploit_attempt, risk
```

**Alert when KEV vulnerabilities are detected on critical assets:**
```spl
index=vulnerability sourcetype="nessus:scan" severity="Critical"
| lookup cisa_kev_lookup.csv cve_id AS CVE OUTPUT kev_status, due_date
| where kev_status="active"
| lookup asset_criticality_lookup.csv ip AS Host OUTPUT criticality
| where criticality IN ("business-critical", "mission-critical")
| table Host, CVE, plugin_name, cvss_score, kev_status, due_date, criticality
```

### Step 5: Build Remediation Tracking Dashboard

**Splunk Dashboard for Vulnerability Metrics:**
```spl
-- Open vulnerabilities by severity
index=vulnerability sourcetype="nessus:scan" status="open"
| stats count by severity
| eval order = case(severity="Critical", 1, severity="High", 2, severity="Medium", 3,
                    severity="Low", 4, 1=1, 5)
| sort order

-- SLA compliance tracking
index=vulnerability sourcetype="nessus:scan" status="open"
| eval sla_days = case(
    severity="Critical", 1,
    severity="High", 7,
    severity="Medium", 30,
    severity="Low", 90
  )
| eval days_open = round((now() - first_detected) / 86400)
| eval sla_status = if(days_open > sla_days, "OVERDUE", "Within SLA")
| stats count by severity, sla_status

-- Remediation trend over 90 days
index=vulnerability sourcetype="nessus:scan"
| eval is_open = if(status="open", 1, 0)
| eval is_closed = if(status="fixed", 1, 0)
| timechart span=1w sum(is_open) AS opened, sum(is_closed) AS remediated
```

### Step 6: Automate Remediation Ticketing

Create tickets automatically for high-priority findings:

```python
import requests

servicenow_url = "https://company.service-now.com/api/now/table/incident"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {snow_token}"
}

for vuln in vulns:
    if vuln["risk_score"] >= 8.0:
        ticket = {
            "short_description": f"[VULN] {vuln['cve']} — {vuln['plugin_name']} on {vuln['host']}",
            "description": (
                f"Vulnerability: {vuln['plugin_name']}\n"
                f"CVE: {vuln['cve']}\n"
                f"CVSS: {vuln['cvss']}\n"
                f"Host: {vuln['host']}\n"
                f"Asset Criticality: {vuln['asset_criticality']}\n"
                f"CISA KEV: {'YES' if vuln['kev'] else 'NO'}\n"
                f"Risk Score: {vuln['risk_score']}\n"
                f"Remediation SLA: {'24 hours' if vuln['kev'] else '7 days'}"
            ),
            "urgency": "1" if vuln["kev"] else "2",
            "impact": "1" if vuln["asset_criticality"] == "business-critical" else "2",
            "assignment_group": "IT Infrastructure",
            "category": "Vulnerability"
        }
        response = requests.post(servicenow_url, headers=headers, json=ticket)
        print(f"Ticket created: {response.json()['result']['number']}")
```

## Key Concepts

| Term | Definition |
|------|-----------|
| **CVSS** | Common Vulnerability Scoring System — standardized severity rating (0-10) for vulnerabilities |
| **CISA KEV** | Known Exploited Vulnerabilities catalog — CISA-maintained list of vulnerabilities with confirmed active exploitation |
| **Credentialed Scan** | Vulnerability scan using authenticated access for deeper detection than network-only scanning |
| **Asset Criticality** | Business impact classification determining remediation priority (mission-critical, business-critical, standard) |
| **Remediation SLA** | Service Level Agreement defining maximum time allowed to patch vulnerabilities by severity |
| **EPSS** | Exploit Prediction Scoring System — ML-based probability score predicting likelihood of exploitation |

## Tools & Systems

- **Tenable Nessus / Tenable.io**: Enterprise vulnerability scanner with 200,000+ plugin checks and compliance auditing
- **Qualys VMDR**: Cloud-based vulnerability management with asset discovery, prioritization, and patching integration
- **OpenVAS (Greenbone)**: Open-source vulnerability scanner with community-maintained vulnerability feed
- **CISA KEV Catalog**: US government maintained list of actively exploited vulnerabilities requiring mandatory remediation
- **Rapid7 InsightVM**: Vulnerability management platform with live dashboards and remediation project tracking

## Common Scenarios

- **Zero-Day Response**: New CVE published — run targeted scan for affected software, cross-reference with KEV and exploit databases
- **Compliance Audit Prep**: Generate PCI DSS or HIPAA vulnerability report showing scan coverage and remediation status
- **Post-Patch Verification**: Rescan patched systems to confirm vulnerability closure and update tracking dashboard
- **Network Expansion**: New subnet added to infrastructure — onboard to scan scope with appropriate policy
- **Third-Party Risk**: Scan externally-facing assets to validate vendor patch compliance before integration

## Output Format

```
VULNERABILITY SCAN REPORT — Weekly Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scan Date:    2024-03-16 02:00 UTC
Scan Scope:   10.0.0.0/16 (1,247 hosts scanned)
Duration:     4h 23m
Coverage:     98.7% (16 hosts unreachable)

Findings:
  Severity     Count    New    CISA KEV
  Critical     23       5      3
  High         187      34     12
  Medium       892      78     0
  Low          1,456    112    0
  Info         3,891    201    0

Top Priority (P1 — 24hr SLA):
  CVE-2024-21762  FortiOS RCE           3 hosts   KEV: YES
  CVE-2024-1709   ConnectWise RCE       1 host    KEV: YES
  CVE-2024-3400   Palo Alto PAN-OS RCE  2 hosts   KEV: YES

SLA Compliance:
  Critical: 82% within SLA (4 overdue)
  High:     91% within SLA (17 overdue)
  Medium:   88% within SLA (107 overdue)

Tickets Created: 39 (ServiceNow)
```

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "vulnerability" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist