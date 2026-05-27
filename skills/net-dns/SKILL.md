---
name: net-dns
description: - Mapping the external attack surface of a target organization during authorized penetration tests - Discovering hidden subdomains, internal hostnames, and IP addresses exposed via DNS records - Testing whether DNS servers allow unauthorized zone transfers that leak the entire zone file - Identifying mail servers, name servers, and service records 
domain: cybersecurity
---
---|------------|
| **Zone Transfer (AXFR)** | DNS mechanism that replicates the complete zone file from a primary to secondary server; unauthorized transfers expose all records in the zone |
| **Subdomain Enumeration** | Process of discovering valid subdomains through brute force, certificate transparency logs, search engines, and passive DNS databases |
| **DNSSEC** | DNS Security Extensions that add cryptographic signatures to DNS responses, preventing cache poisoning and spoofing attacks |
| **SPF/DKIM/DMARC** | Email authentication protocols defined in DNS TXT records that prevent email spoofing and domain impersonation |
| **Wildcard DNS** | A DNS record using an asterisk (*) that matches any query for non-existent subdomains, potentially masking enumeration results |
| **PTR Record** | Reverse DNS record that maps an IP address to a hostname, often revealing internal naming conventions and server roles |

## Tools & Systems

- **dig**: Standard DNS lookup utility with full support for all record types, DNSSEC validation, and zone transfer queries
- **dnsrecon**: Comprehensive DNS enumeration tool supporting zone transfers, brute force, reverse lookup, cache snooping, and Google dork queries
- **subfinder**: Fast passive subdomain discovery tool that queries certificate transparency logs, search engines, and DNS databases
- **Amass (OWASP)**: Advanced attack surface mapping tool with both passive and active DNS enumeration, graph analysis, and data source integration
- **gobuster**: Fast brute-force tool for DNS subdomain enumeration using configurable wordlists and concurrent threads

## Common Scenarios

### Scenario: External Reconnaissance for a Web Application Penetration Test

**Context**: A security consultant is performing external reconnaissance for a web application penetration test. The client's primary domain is example.com, and the scope includes all subdomains and related infrastructure. The consultant has authorization to enumerate DNS records and probe discovered web services.

**Approach**:
1. Query NS, MX, TXT, and SOA records for example.com to map the DNS infrastructure
2. Attempt zone transfers against both nameservers -- ns2 succeeds, revealing 347 DNS records including internal staging environments
3. Run subfinder and amass in passive mode to discover 89 additional subdomains from certificate transparency logs
4. Brute-force subdomains with a 20,000-word list using gobuster, discovering 12 more subdomains not found in passive sources
5. Resolve all subdomains and identify 15 that resolve to internal RFC1918 addresses (information disclosure)
6. Probe all web-accessible subdomains with httpx, discovering a staging environment (staging.example.com) with default credentials
7. Report zone transfer vulnerability, internal IP disclosure, and exposed staging environment to the client

**Pitfalls**:
- Sending thousands of DNS queries per second and triggering rate limiting or DNS-based DDoS protection
- Not checking for wildcard DNS records, resulting in false positive subdomain discoveries
- Missing subdomains that use separate DNS providers or CDN-specific CNAME records
- Overlooking TXT records that contain API keys, verification tokens, or internal comments

## Output Format

```
## DNS Enumeration Report

**Target Domain**: example.com
**Authorized Nameservers**: ns1.example.com (203.0.113.10), ns2.example.com (203.0.113.11)

### Zone Transfer Status
| Nameserver | AXFR Result | Records Obtained |
|------------|-------------|------------------|
| ns1.example.com | REFUSED | 0 |
| ns2.example.com | SUCCESS | 347 records |

### Subdomain Discovery Summary
| Method | Subdomains Found |
|--------|-----------------|
| Zone Transfer | 347 |
| Passive (subfinder + amass) | 89 |
| Active Brute Force | 12 |
| **Total Unique** | **412** |

### Critical Findings
1. **Zone Transfer Allowed** (High): ns2.example.com allows AXFR from any source
2. **Internal IP Disclosure** (Medium): 15 subdomains resolve to RFC1918 addresses
3. **Exposed Staging Environment** (High): staging.example.com accessible with default credentials
4. **Missing DMARC Policy** (Medium): No DMARC record found, enabling email spoofing
5. **Weak SPF Record** (Low): SPF uses ~all (soft fail) instead of -all (hard fail)
```