---
name: vuln-scanning-otsafescan
description: - When conducting vulnerability assessments in OT environments with legacy controllers - When implementing continuous vulnerability monitoring without impacting process availability - When preparing for IEC 62443 or NERC CIP compliance audits requiring vulnerability data - When evaluating risk-based patching priorities for OT assets - When validati
domain: cybersecurity
---
RISK-PRIORITIZED FINDINGS ---")
        print(f"(Prioritized by CVSS score and OT impact)")
        for i, finding in enumerate(self.findings[:20], 1):
            print(f"\n  {i}. [{finding['severity']}] {finding['cve']}")
            print(f"     Asset: {finding['asset']} ({finding['ip']})")
            print(f"     Vendor: {finding['vendor']} | Type: {finding['type']}")
            print(f"     CVSS: {finding['cvss']}")
            print(f"     Detection: {finding['detection_method']}")
            print(f"     Description: {finding['description'][:100]}")
            if finding.get("remediation"):
                print(f"     Remediation: {finding['remediation'][:100]}")

        # Export to CSV
        if output_file:
            with open(output_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.findings[0].keys())
                writer.writeheader()
                writer.writerows(self.findings)
            print(f"\n[+] Report exported to {output_file}")

if __name__ == "__main__":
    scanner = OTVulnerabilityScanner(
        tenable_url="https://tenable-ot.plant.local",
        api_key="your-api-key-here",
        verify_ssl=True,
    )

    # Always start with passive assessment
    safety_check = scanner.check_safety_prerequisites("passive", "10.10.0.0/16")
    print(f"Safety prerequisites: {json.dumps(safety_check, indent=2)}")

    scanner.run_passive_assessment(site_id="plant-01")
    scanner.generate_prioritized_report("ot_vulnerabilities.csv")
```

## Key Concepts

| Term | Definition |
|------|------------|
| Passive Vulnerability Detection | Identifying vulnerabilities by analyzing mirrored traffic without sending any packets to OT devices |
| Native Protocol Query | Using industrial protocols (Modbus FC43, S7 SZL Read, CIP Get Attribute) to safely extract device information |
| OT-Safe Scan Profile | Vulnerability scanner configuration designed and lab-tested to avoid crashing industrial controllers |
| Compensating Control | Alternative security measure protecting an unpatched OT asset (firewall DPI, network isolation) |
| CVSS in OT Context | Standard CVSS scores adjusted for OT impact considering safety, availability, and physical consequences |
| Tenable OT Security | Purpose-built OT vulnerability management platform using passive and native protocol-based detection |

## Output Format

```
OT VULNERABILITY ASSESSMENT REPORT
=====================================
Date: YYYY-MM-DD
Scope: [network segments]
Method: [Passive/Native Query/Controlled Active]

VULNERABILITY SUMMARY:
  Critical: [count]
  High: [count]
  Medium: [count]
  Low: [count]

TOP RISK FINDINGS:
  1. [CVE] - [CVSS] - [Asset] - [Description]

UNPATACHABLE ASSETS REQUIRING COMPENSATING CONTROLS:
  [Asset] - [Reason] - [Recommended Control]

PATCH PRIORITIZATION:
  Immediate: [list]
  Next Window: [list]
  Acceptable Risk: [list with justification]
```

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "otsafescan" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist