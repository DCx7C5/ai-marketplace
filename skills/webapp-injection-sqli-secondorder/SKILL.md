---
name: webapp-injection-sqli-secondorder
description: "Webapp Injection Sqli Secondorder."
domain: cybersecurity
---

|
| users | username, password, email | 150 |
| admin_tokens | token, user_id | 3 |

### Remediation
- Use parameterized queries for ALL database operations, including reads
- Never trust data retrieved from the database as safe
- Implement output encoding when displaying database content
- Apply least-privilege database permissions
- Enable SQL query logging for detecting injection attempts
```
