---
name: ics-ics-assetmgmt-claroty-assess
description: - When conducting scheduled OT vulnerability assessments per IEC 62443 or NERC CIP requirements - When deploying Claroty xDome for the first time and performing initial asset discovery and risk assessment - When correlating newly published ICS-CERT advisories against your OT asset inventory - When prioritizing OT vulnerability remediation with limi
domain: cybersecurity
---
{sev.upper()} RISK ({len(findings)}) ---")
                for ra in findings[:10]:
                    report.append(f"\n  Risk Score: {ra.risk_score}/10.0")
                    report.append(f"  Asset: {ra.asset.name} ({ra.asset.vendor} {ra.asset.model})")
                    report.append(f"  Zone: {ra.asset.zone} ({ra.asset.purdue_level})")
                    report.append(f"  CVE: {ra.vulnerability.cve_id} (CVSS: {ra.vulnerability.cvss_score})")
                    report.append(f"  Title: {ra.vulnerability.title}")
                    if ra.vulnerability.patch_available:
                        report.append(f"  Patch: Available - schedule for next maintenance window")
                    else:
                        report.append(f"  Patch: Not available - apply compensating controls")

        return "\n".join(report)

    def export_json(self, output_file):
        """Export assessment to JSON."""
        data = {
            "assessment_date": datetime.now().isoformat(),
            "asset_count": len(self.assets),
            "vulnerability_count": len(self.vulnerabilities),
            "risk_assessments": [
                {
                    "asset_name": ra.asset.name,
                    "asset_ip": ra.asset.ip_address,
                    "cve": ra.vulnerability.cve_id,
                    "risk_score": ra.risk_score,
                    "risk_rating": ra.risk_rating,
                    "priority": ra.remediation_priority,
                }
                for ra in sorted(self.risk_assessments, key=lambda x: -x.risk_score)
            ],
        }
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    assessment = OTVulnerabilityAssessment()
    advisories = assessment.fetch_ics_advisories()
    print(f"Fetched {len(advisories)} ICS advisories from CISA KEV catalog")
```

## Key Concepts

| Term | Definition |
|------|------------|
| Claroty xDome | Cyber-physical systems protection platform providing asset discovery, vulnerability management, and threat detection for OT/IoT environments |
| Passive Discovery | Identifying OT assets by analyzing network traffic without sending any packets, safe for production environments |
| Safe Active Query | Querying OT devices using native industrial protocols at safe rates to collect detailed asset information without disrupting operations |
| OT Risk Score | Risk rating that factors CVSS base score, asset criticality, Purdue level, and compensating controls for OT-appropriate prioritization |
| ICS-CERT Advisory | CISA-published security advisories for industrial control system vulnerabilities with vendor-specific remediation guidance |
| Virtual Patching | Deploying IPS/firewall rules to block exploitation of known vulnerabilities when firmware patches cannot be immediately applied |

## Tools & Systems

- **Claroty xDome**: Comprehensive OT/IoT asset discovery, vulnerability management, and continuous threat detection platform
- **Claroty CTD**: Continuous Threat Detection sensor for passive network monitoring in OT environments
- **CISA ICS-CERT**: US government advisory service publishing ICS vulnerability notifications and mitigation guidance
- **Dragos Platform**: Alternative OT security platform with asset visibility and vulnerability management capabilities
- **Nozomi Networks Guardian**: OT monitoring platform with vulnerability correlation and risk scoring

## Output Format

```
OT Vulnerability Assessment Report
=====================================
Tool: Claroty xDome / Manual Assessment
Date: YYYY-MM-DD
Assets Scanned: [N]

RISK SUMMARY:
  Critical Risk: [N] vulnerabilities on [N] assets
  High Risk: [N] vulnerabilities on [N] assets
  Medium Risk: [N] vulnerabilities on [N] assets
  Low Risk: [N] vulnerabilities on [N] assets

TOP RISKS:
  [Risk Score] [CVE-ID] on [Asset Name] ([Zone])
    Remediation: [Patch/Compensating Control]
    Timeline: [Next maintenance window / Immediate]
```