---
name: webapp-header-host-poison
description: "-| | 1 | Password Reset Poisoning | Host: evil.com | Token theft | Critical | | 2 | Cache Poisoning | X-Forwarded-Host: evil."
domain: cybersecurity
---

-|
| 1 | Password Reset Poisoning | Host: evil.com | Token theft | Critical |
| 2 | Cache Poisoning | X-Forwarded-Host: evil.com | Stored XSS | High |
| 3 | Virtual Host Access | Host: admin.target.com | Admin panel exposure | High |
| 4 | SSRF | Host: 169.254.169.254 | Metadata access | Critical |

### Remediation
- Validate Host header against a whitelist of expected values
- Do not use Host header for generating URLs in password reset emails
- Configure web server to reject requests with unrecognized Host values
- Set absolute URLs in application configuration instead of deriving from Host
```
