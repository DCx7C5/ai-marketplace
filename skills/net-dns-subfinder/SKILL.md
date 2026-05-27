---
name: net-dns-subfinder
description: - During the reconnaissance phase of penetration testing or bug bounty hunting - When mapping the external attack surface of a target organization - Before performing vulnerability scanning on discovered subdomains - When building an asset inventory for continuous security monitoring - During red team engagements requiring passive information gathe
domain: cybersecurity
---
------|-------------|
| Passive Enumeration | Discovering subdomains without directly querying target DNS servers |
| Certificate Transparency | Public logs of SSL/TLS certificates revealing subdomain names |
| DNS Aggregation | Collecting subdomain data from multiple passive DNS databases |
| Recursive Enumeration | Discovering subdomains of subdomains for deeper coverage |
| Source Providers | External APIs and databases queried for subdomain intelligence |
| CNAME Records | Canonical name records that may reveal additional infrastructure |
| Wildcard DNS | DNS configuration returning results for any subdomain query |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Subfinder | Primary passive subdomain enumeration engine |
| httpx | HTTP probe tool for validating live subdomains |
| dnsx | DNS resolution and validation toolkit |
| Nuclei | Template-based vulnerability scanner for discovered hosts |
| Amass | Complementary subdomain enumeration with active/passive modes |
| gowitness | Web screenshot utility for visual reconnaissance |
| Shodan | Internet-wide scanning database for subdomain intelligence |
| crt.sh | Certificate transparency log search engine |

## Common Scenarios

1. **Bug Bounty Reconnaissance** — Enumerate all subdomains of a target program scope to identify forgotten or misconfigured assets that may contain vulnerabilities
2. **Attack Surface Mapping** — Build a comprehensive inventory of externally accessible subdomains for ongoing security monitoring and risk assessment
3. **Cloud Asset Discovery** — Identify subdomains pointing to cloud services (AWS, Azure, GCP) that may be vulnerable to subdomain takeover
4. **CI/CD Integration** — Automate subdomain monitoring in pipelines to detect new subdomains and alert on changes to the attack surface
5. **Merger & Acquisition Due Diligence** — Map the complete external footprint of an acquisition target during security assessment

## Output Format

```
## Subdomain Enumeration Report
- **Target Domain**: example.com
- **Total Subdomains Found**: 247
- **Live Hosts**: 183
- **Unique IP Addresses**: 42
- **Sources Used**: crt.sh, VirusTotal, Shodan, SecurityTrails, Censys

### Discovered Subdomains
| Subdomain | IP Address | Status Code | Technology |
|-----------|-----------|-------------|------------|
| api.example.com | 10.0.1.5 | 200 | Nginx, Node.js |
| staging.example.com | 10.0.2.10 | 403 | Apache |
| dev.example.com | 10.0.3.15 | 200 | Express |

### Recommendations
- Remove DNS records for decommissioned subdomains
- Investigate subdomains with CNAME pointing to unclaimed services
- Restrict access to development and staging environments
```