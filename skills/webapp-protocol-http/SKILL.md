---
name: webapp-protocol-http
description: "Webapp Protocol Http."
domain: cybersecurity
---

-|
| 1 | POST /checkout | price | Price manipulation | Critical |
| 2 | GET /oauth/authorize | redirect_uri | Token theft | High |
| 3 | POST /api/search | q | WAF bypass (SQLi) | High |

### Remediation
- Implement strict parameter validation rejecting duplicate parameters
- Use the first occurrence of any parameter and ignore subsequent duplicates
- Apply WAF rules that detect duplicate parameter patterns
- Validate all parameters server-side regardless of client-side checks
```
