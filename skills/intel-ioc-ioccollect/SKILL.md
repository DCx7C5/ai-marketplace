---
name: intel-ioc-ioccollect
description: - During active incident response to identify and block adversary infrastructure - Post-incident to document all observed adversary artifacts for future detection - When sharing threat intelligence with ISACs, sector partners, or law enforcement - When building detection rules in SIEM, EDR, or network security tools - When enriching IOCs with threa
domain: cybersecurity
---
----|-----------------|----------|
| 90-100 | Confirmed Malicious | Multiple TI sources confirm, observed in active attack |
| 70-89  | Highly Suspicious | Single TI source confirms, behavioral analysis supports |
| 50-69  | Suspicious | Limited TI data, contextually suspicious |
| 30-49  | Unconfirmed | No TI matches, but anomalous in environment |
| 0-29   | Likely Benign | False positive indicators or legitimate infrastructure |

### Step 5: Distribute IOCs for Detection and Blocking

Push IOCs to defensive systems for immediate protection:

- **Firewall/IPS**: Block C2 IPs and domains
- **DNS**: Sinkhole malicious domains
- **EDR**: Add file hashes to blocklist, create custom IOC watchlists
- **Email Gateway**: Block sender domains, attachment hashes, malicious URLs
- **SIEM**: Create correlation searches for IOC matches
- **Web Proxy**: Block URLs and domains in web filtering policy

### Step 6: Share IOCs with Partners

Package IOCs in STIX 2.1 format for sharing:

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "created": "2025-11-15T18:00:00Z",
  "modified": "2025-11-15T18:00:00Z",
  "name": "Qakbot C2 Server IP",
  "indicator_types": ["malicious-activity"],
  "pattern": "[ipv4-addr:value = '185.220.101.42']",
  "pattern_type": "stix",
  "valid_from": "2025-11-15T14:23:00Z",
  "confidence": 95,
  "labels": ["c2", "qakbot"],
  "object_marking_refs": ["marking-definition--f88d31f6-486f-44da-b317-01333bde0b82"]
}
```

Submit to MISP, ISAC portals, and TAXII servers per sharing agreements.

## Key Concepts

| Term | Definition |
|------|------------|
| **IOC (Indicator of Compromise)** | Technical artifact observed during a security incident that indicates adversary presence (hash, IP, domain, etc.) |
| **TLP (Traffic Light Protocol)** | Standard for classifying the sharing restrictions of threat intelligence: WHITE, GREEN, AMBER, AMBER+STRICT, RED |
| **STIX (Structured Threat Information Expression)** | Standard language for representing cyber threat intelligence in a structured, machine-readable format |
| **TAXII (Trusted Automated Exchange of Intelligence Information)** | Transport protocol for sharing STIX-formatted threat intelligence between organizations |
| **Confidence Score** | Numerical rating (0-100) indicating the analyst's certainty that an indicator is truly malicious |
| **IOC Lifecycle** | Process of creating, validating, distributing, and eventually retiring indicators as they lose relevance |
| **Defanging** | Practice of modifying malicious URLs and domains in reports to prevent accidental clicks (e.g., evil[.]com) |

## Tools & Systems

- **MISP**: Open-source threat intelligence sharing platform for managing, storing, and distributing IOCs
- **VirusTotal**: Multi-engine malware scanning and threat intelligence platform for IOC enrichment
- **OpenCTI**: Open-source cyber threat intelligence platform supporting STIX 2.1 natively
- **Yeti**: Open-source platform for organizing observables, indicators, and TTPs
- **CyberChef**: GCHQ's data transformation tool useful for decoding, defanging, and formatting IOCs

## Common Scenarios

### Scenario: Post-Incident IOC Package for ISAC Sharing

**Context**: After responding to a Qakbot infection that led to Cobalt Strike deployment, the IR team must package all IOCs for sharing with the Financial Services ISAC (FS-ISAC).

**Approach**:
1. Compile all network, host, and email indicators from the investigation
2. Enrich each IOC with VirusTotal and MISP correlation data
3. Assign confidence scores based on direct observation vs. secondary correlation
4. Mark all IOCs with TLP:AMBER for partner sharing
5. Export as STIX 2.1 bundle and submit to FS-ISAC TAXII feed
6. Create a human-readable IOC summary report for email distribution

**Pitfalls**:
- Including internal IP addresses or hostnames in shared IOC packages (information leakage)
- Sharing IOCs at TLP:WHITE that should be restricted to TLP:AMBER
- Not defanging URLs and domains in human-readable reports
- Sharing IP addresses of legitimate CDNs or cloud providers as malicious IOCs

## Output Format

```
INDICATOR OF COMPROMISE REPORT
================================
Incident:     INC-2025-1547
Date:         2025-11-15
TLP:          AMBER
Sharing:      FS-ISAC, internal SOC

NETWORK INDICATORS
Type     | Value                    | Confidence | Context
---------|--------------------------|------------|--------
IPv4     | 185.220.101[.]42         | 95         | Qakbot C2 server
IPv4     | 91.215.85[.]17           | 90         | Cobalt Strike C2
Domain   | update.evil[.]com        | 95         | Staging domain
URL      | hxxps://185.220[.]101.42/gate.php | 95  | C2 check-in
JA3      | a0e9f5d64349fb13191bc7...| 80         | Qakbot TLS fingerprint

HOST INDICATORS
Type     | Value                    | Confidence | Context
---------|--------------------------|------------|--------
SHA-256  | a1b2c3d4e5f6...         | 100        | Qakbot dropper
SHA-256  | b2c3d4e5f6a7...         | 100        | Cobalt Strike beacon
FilePath | C:\Users\*\AppData\Local\Temp\update.exe | 85 | Dropper location
RegKey   | HKCU\...\Run\svcupdate  | 90         | Persistence
Mutex    | Global\MTX_0x1234ABCD   | 95         | Qakbot instance lock
Task     | WindowsUpdate           | 90         | Scheduled task persistence

EMAIL INDICATORS
Type     | Value                    | Confidence | Context
---------|--------------------------|------------|--------
Sender   | billing@spoofed[.]com   | 95         | Phishing sender
Subject  | "Invoice-Nov2025"       | 70         | Phishing subject line
Hash     | c3d4e5f6a7b8...         | 100        | Malicious .docm attachment

TOTAL: 14 indicators | HIGH confidence avg: 91
```