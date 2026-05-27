---
name: webapp-owasp-broken
description: - When auditing web applications for references to expired or unclaimed external resources - During supply chain security assessments of third-party script and resource dependencies - When testing for subdomain takeover opportunities via dangling CNAME records - During bug bounty hunting for broken link hijacking vulnerabilities - When assessing th
domain: cybersecurity
---
------|-------------|
| Broken Link Hijacking | Claiming control of external resources referenced by target website |
| Dangling CNAME | DNS CNAME record pointing to unclaimed or decommissioned service |
| Subdomain Takeover | Claiming a subdomain by provisioning the service its CNAME points to |
| External Script Hijacking | Registering expired domains that serve JavaScript loaded by target |
| Supply Chain Attack | Compromising external dependencies to inject malicious content |
| Dead Link | URL reference returning 404 or DNS resolution failure |
| Resource Fingerprinting | Identifying specific cloud services from error messages and headers |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| broken-link-checker | Automated broken link discovery via web crawling |
| subjack | Subdomain takeover detection tool |
| nuclei | Template-based takeover detection scanner |
| can-i-take-over-xyz | Community database of services vulnerable to takeover |
| BadDNS | DNS auditing tool for detecting domain/subdomain takeovers |
| Wayback Machine | Historical URL analysis for discovering past external references |

## Common Scenarios

1. **JavaScript Supply Chain** — Register expired domain that serves JavaScript loaded by target; inject malicious code affecting all visitors
2. **S3 Bucket Takeover** — Claim deleted AWS S3 bucket referenced by target; serve malicious content or steal uploaded data
3. **GitHub Pages Hijack** — Create GitHub Pages repository matching dangling CNAME to serve phishing pages on target subdomain
4. **Social Media Impersonation** — Claim unclaimed social media handles linked from target website for brand impersonation
5. **CDN Package Hijack** — Claim deprecated npm packages referenced via CDN URLs to inject malicious JavaScript

## Output Format

```
## Broken Link Hijacking Report
- **Target**: http://target.com
- **Total External Links**: 145
- **Dead Links**: 12
- **Hijackable Resources**: 3

### Findings
| # | Resource | Type | Status | Impact |
|---|----------|------|--------|--------|
| 1 | analytics.expired-domain.com | JavaScript | Domain available | Full XSS |
| 2 | assets.target.com -> S3 bucket | Static assets | Bucket deleted | Content injection |
| 3 | blog.target.com -> GitHub Pages | Subdomain | No GitHub repo | Subdomain takeover |

### Remediation
- Remove references to decommissioned external resources
- Delete dangling CNAME records for unused subdomains
- Implement Subresource Integrity (SRI) for external scripts
- Regularly audit external dependencies for availability
- Use Content Security Policy to restrict allowed script sources
```