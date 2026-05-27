---
name: webapp-injection-sqli-nosql
description: "Webapp Injection Sqli Nosql."
domain: cybersecurity
---

--|
| POST /api/login | username | Operator ($ne) | Auth Bypass |
| POST /api/login | password | Regex ($regex) | Data Extraction |
| GET /api/users | id | $where JS Injection | RCE Potential |

### Proof of Concept
- Authentication bypass achieved with: {"username":{"$ne":""},"password":{"$ne":""}}
- Extracted 3 admin passwords via blind regex injection
- JavaScript execution confirmed via $where operator

### Remediation
- Use parameterized queries with MongoDB driver sanitization
- Implement input type validation (reject objects where strings expected)
- Disable server-side JavaScript execution ($where) in MongoDB config
- Apply least-privilege database access controls
```
