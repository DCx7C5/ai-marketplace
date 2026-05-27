---
name: webapp-tls-ctaudit
description: - Monitoring owned domains for unauthorized or unexpected certificate issuance by unknown Certificate Authorities - Discovering subdomains and hidden services through certificates logged in public CT logs - Detecting phishing infrastructure that uses look-alike domain certificates (typosquatting, homograph attacks) - Auditing Certificate Authority 
domain: cybersecurity
---
---|------------|
| **Certificate Transparency (CT)** | An open framework (RFC 6962) requiring Certificate Authorities to log all issued certificates in publicly auditable append-only logs, enabling domain owners to detect unauthorized issuance |
| **Signed Certificate Timestamp (SCT)** | A promise from a CT log that a certificate will be included within the Maximum Merge Delay (typically 24 hours); browsers require SCTs from multiple logs before trusting a certificate |
| **Merkle Tree** | The cryptographic data structure used by CT logs where leaf nodes are certificate hashes and parent nodes are hashes of their children, enabling efficient consistency and inclusion proofs |
| **Precertificate** | A certificate submitted to CT logs before final issuance, containing a poison extension (OID 1.3.6.1.4.1.11129.2.4.3) that prevents it from being used for TLS but reserves its place in the log |
| **crt.sh** | A free web service operated by Sectigo that aggregates certificates from all major CT logs into a searchable PostgreSQL database, providing both web and API access |
| **Subdomain Takeover** | A vulnerability where a subdomain's DNS record points to a decommissioned service (cloud provider, CDN) that an attacker can reclaim, made discoverable through expired CT certificates |
| **Maximum Merge Delay (MMD)** | The maximum time (typically 24 hours) a CT log has to incorporate a submitted certificate into its Merkle tree after returning an SCT |
| **CAA Record** | DNS Certification Authority Authorization record that specifies which CAs are permitted to issue certificates for a domain; CT monitoring detects violations of CAA policy |

## Tools & Systems

- **crt.sh**: Primary CT log aggregator providing JSON API access at `https://crt.sh/?q=<query>&output=json` with support for wildcard queries, identity filtering, and certificate detail retrieval
- **ct-woodpecker**: Open-source CT log monitoring tool from Let's Encrypt that integrates with Prometheus and Grafana for operational monitoring of log health and consistency
- **certspotter**: SSLMate's CT log monitor that watches for newly issued certificates and sends notifications; available as hosted service or self-hosted tool
- **Google Argon / Xenon / Icarus**: Google-operated CT logs that are among the most widely used, queryable via the RFC 6962 API at their respective log URLs
- **OpenSSL**: Command-line tool for parsing certificate details, verifying chains, and extracting SAN lists from certificates retrieved through CT monitoring

## Common Scenarios

### Scenario: Detecting Unauthorized Certificate Issuance for a Financial Services Company

**Context**: A bank monitors its primary domain (`bank.example.com`) and discovers via CT logs that a certificate has been issued by a CA they have never used, covering `secure-login.bank.example.com` -- a subdomain that does not exist in their DNS.

**Approach**:
1. CT monitoring agent detects a new certificate from "FreeSSL CA" for `secure-login.bank.example.com` in crt.sh results, which is not in the authorized CA list (DigiCert, Sectigo)
2. Alert fires as unauthorized CA + new subdomain, escalating to the security team within 15 minutes of CT log entry
3. Investigate the certificate: extract the public key, check if the domain validated via HTTP-01 or DNS-01 challenge, query WHOIS for the issuing organization
4. DNS lookup for `secure-login.bank.example.com` reveals it resolves to an IP address in a hosting provider not used by the bank -- confirming this is attacker infrastructure
5. Initiate incident response: request certificate revocation from FreeSSL CA, file a domain abuse report, add the IP to blocklists, and notify the anti-phishing team
6. Implement CAA DNS records (`bank.example.com. CAA 0 issue "digicert.com"`) to prevent unauthorized CAs from issuing future certificates

**Pitfalls**:
- Not monitoring wildcard patterns (`%.bank.example.com`) and missing certificates for subdomains
- Ignoring precertificates that appear in CT logs before the actual certificate is issued, losing the early warning advantage
- Failing to verify that CAA records are properly configured on all domains after an incident
- Over-alerting on legitimate certificate renewals because the baseline database was not updated after authorized changes

### Scenario: Attack Surface Mapping Through CT Log Subdomain Discovery

**Context**: A penetration tester uses CT logs as the first phase of external reconnaissance to map the target organization's internet-facing services before active scanning.

**Approach**:
1. Query crt.sh for `%.target.com` and all known subsidiary domains, collecting 2,400 unique certificates spanning 8 years
2. Extract 347 unique subdomains from SAN fields across all certificates, including expired ones
3. DNS-resolve all 347 subdomains, finding 189 currently active with A/AAAA records
4. Identify 12 subdomains pointing to decommissioned cloud services (CNAME to S3 buckets, Azure endpoints) that are candidates for subdomain takeover
5. Discover `staging-api.target.com` and `dev-portal.target.com` which are not in the target's documented scope but are reachable and running older software versions
6. Present findings to the target organization showing the gap between their known asset inventory and the CT-derived attack surface

**Pitfalls**:
- Assuming all CT-discovered subdomains are in scope without confirming with the asset owner
- Not checking for wildcard DNS responses that make it appear subdomains exist when they resolve to a catch-all
- Relying solely on CT data without cross-referencing with passive DNS databases for comprehensive coverage

## Output Format

```
## CT Log Monitoring Report

**Domain**: example.com
**Monitoring Period**: 2026-03-01 to 2026-03-19
**Total Certificates Tracked**: 142
**New Certificates Detected**: 7
**Alerts Generated**: 2

### Alert: Unauthorized CA Issuance
- **Severity**: Critical
- **Certificate CN**: secure-login.example.com
- **SANs**: secure-login.example.com, www.secure-login.example.com
- **Issuer**: Unknown Free CA (NOT in authorized CA list)
- **Serial**: 04:A3:B7:2F:...:9E
- **Not Before**: 2026-03-18T00:00:00Z
- **Not After**: 2026-06-16T00:00:00Z
- **CT Log**: Google Argon 2026
- **SCT Timestamp**: 2026-03-17T22:15:33Z
- **Action Required**: Investigate immediately, request revocation

### Subdomain Discovery Summary
- **Total Unique Subdomains**: 89
- **New Subdomains This Period**: 3
  - api-v3.example.com (DigiCert, valid)
  - staging-new.example.com (Let's Encrypt, valid)
  - old-portal.example.com (expired 2025-12-01, CNAME to Azure -- takeover risk)

### Typosquatting Alerts
| Domain | Certificate Count | Issuer | Action Required |
|--------|-------------------|--------|-----------------|
| exarnple.com | 2 | Let's Encrypt | Investigate phishing |
| examp1e.com | 1 | ZeroSSL | Investigate phishing |
```