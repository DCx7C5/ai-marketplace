---
name: webapp-redirect-open
description: "--| | 1 | /login | next | //evil.com | Phishing | | 2 | /oauth/authorize | redirect_uri | https://target."
domain: cybersecurity
---

--|
| 1 | /login | next | //evil.com | Phishing |
| 2 | /oauth/authorize | redirect_uri | https://target.com@evil.com | Token Theft |
| 3 | /logout | return | https://evil.com%00.target.com | Session Redirect |

### Remediation
- Implement allowlist of permitted redirect destinations
- Validate redirect URLs server-side using strict URL parsing
- Reject any redirect URL containing external domains
- Use indirect reference maps instead of direct URL parameters
```
