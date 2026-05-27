---
name: net-dns-subfinder
description: "| | api.example.com | 10.0.1.5 | 200 | Nginx, Node."
domain: cybersecurity
---

|
| api.example.com | 10.0.1.5 | 200 | Nginx, Node.js |
| staging.example.com | 10.0.2.10 | 403 | Apache |
| dev.example.com | 10.0.3.15 | 200 | Express |

### Recommendations
- Remove DNS records for decommissioned subdomains
- Investigate subdomains with CNAME pointing to unclaimed services
- Restrict access to development and staging environments
```
