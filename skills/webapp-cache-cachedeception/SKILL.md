---
name: webapp-cache-cachedeception
description: "--| | /account/profile/x.css | Full profile page | Email, Name, API Key | | /account/settings/x."
domain: cybersecurity
---

--|
| /account/profile/x.css | Full profile page | Email, Name, API Key |
| /account/settings/x.js | Settings page | 2FA backup codes |

### Remediation
- Configure CDN to respect Cache-Control: no-store on dynamic pages
- Implement Vary: Cookie header on authenticated endpoints
- Use path-based routing rules that reject unexpected extensions
- Enable consistent path normalization between CDN and origin
```
