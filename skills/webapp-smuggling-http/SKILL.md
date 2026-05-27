---
name: webapp-smuggling-http
description: "--| | Admin bypass | Accessed /admin without authentication | | Request capture | Stole session cookies from other users | | XSS escalation | Delivered reflected XSS to arbitrary users | | Cache poisoning | Poisoned CDN cache with malicious response |  ### Recommendation 1."
domain: cybersecurity
---

--|
| Admin bypass | Accessed /admin without authentication |
| Request capture | Stole session cookies from other users |
| XSS escalation | Delivered reflected XSS to arbitrary users |
| Cache poisoning | Poisoned CDN cache with malicious response |

### Recommendation
1. Ensure front-end and back-end use the same HTTP parsing behavior
2. Reject ambiguous requests with both Content-Length and Transfer-Encoding
3. Upgrade to HTTP/2 end-to-end (no protocol downgrade)
4. Use HTTP/2 between proxy and origin server
5. Normalize requests at the front-end before forwarding
```
