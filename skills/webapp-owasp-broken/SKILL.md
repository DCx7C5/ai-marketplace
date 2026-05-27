---
name: webapp-owasp-broken
description: "--| | 1 | analytics.expired-domain.com | JavaScript | Domain available | Full XSS | | 2 | assets."
domain: cybersecurity
---

--|
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
