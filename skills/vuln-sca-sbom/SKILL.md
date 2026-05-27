---
name: vuln-sca-sbom
description: - A new regulatory requirement (EO 14028, EU CRA) mandates SBOM analysis for software deliveries - Security team needs to assess third-party risk by scanning vendor-provided SBOMs - CI/CD pipeline requires automated vulnerability checks against generated SBOMs - Incident response needs to determine if a newly disclosed CVE affects deployed software
domain: cybersecurity
---
---|------------|
| **SBOM** | Software Bill of Materials; a formal inventory of all components, libraries, and dependencies in a software product |
| **CycloneDX** | OWASP-maintained SBOM standard supporting JSON, XML, and protobuf formats with dependency graph and vulnerability data |
| **SPDX** | Linux Foundation SBOM standard focused on license compliance with support for package, file, and snippet-level detail |
| **PURL** | Package URL; a standardized scheme for identifying software packages across ecosystems (e.g., pkg:npm/lodash@4.17.21) |
| **CPE** | Common Platform Enumeration; NIST naming scheme for IT products used to correlate with NVD CVE data |
| **NVD** | National Vulnerability Database; US government repository of vulnerability data indexed by CVE identifiers |
| **Transitive Dependency** | A dependency not directly declared but pulled in through the dependency chain of direct dependencies |
| **CISA KEV** | CISA Known Exploited Vulnerabilities catalog; CVEs confirmed to be actively exploited in the wild |

## Tools & Systems

- **syft** (Anchore): Open-source SBOM generator supporting 30+ package ecosystems and CycloneDX/SPDX output
- **grype** (Anchore): Vulnerability scanner that accepts SBOMs as input and correlates against multiple advisory databases
- **cyclonedx-python-lib**: Python library for creating, parsing, and validating CycloneDX SBOMs programmatically
- **lib4sbom**: Python library for parsing both SPDX and CycloneDX format SBOMs
- **nvdlib**: Python wrapper for the NVD 2.0 API supporting CVE and CPE queries with rate limit management
- **OWASP Dependency-Track**: Platform for continuous SBOM analysis, vulnerability tracking, and policy enforcement

## Common Scenarios

### Scenario: Assessing Vendor Software After Log4Shell Disclosure

**Context**: After the Log4Shell (CVE-2021-44228) disclosure, the security team needs to determine which vendor-supplied applications contain vulnerable versions of log4j. Several vendors have provided SBOMs per contractual requirements.

**Approach**:
1. Collect all vendor SBOMs (CycloneDX or SPDX JSON format)
2. Parse each SBOM and search for log4j-core components with versions < 2.17.1
3. Query NVD API for the specific CVEs (CVE-2021-44228, CVE-2021-45046, CVE-2021-45105)
4. Build dependency graphs to identify which application components depend on log4j
5. Calculate blast radius: how many services and endpoints are exposed
6. Generate prioritized remediation report sorted by exposure and business criticality
7. Cross-validate findings with grype scan of the same SBOMs

**Pitfalls**:
- Vendor SBOMs may be incomplete, missing shaded/bundled JAR files that embed log4j
- SPDX and CycloneDX version differences may affect parser compatibility
- NVD API rate limits can slow analysis when scanning hundreds of components without an API key
- CPE names in SBOMs may not exactly match NVD entries, requiring fuzzy matching
- Transitive dependencies may include log4j even when it is not a direct dependency

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "sbom" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist