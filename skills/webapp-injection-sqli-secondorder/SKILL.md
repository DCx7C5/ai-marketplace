---
name: webapp-injection-sqli-secondorder
description: - When first-order SQL injection testing reveals proper input sanitization at storage time - During penetration testing of applications with user-generated content stored in databases - When testing multi-step workflows where stored data feeds subsequent database queries - During assessment of admin panels that display or process user-submitted dat
domain: cybersecurity
---
------|-------------|
| Second-Order Injection | SQL payload stored safely, then executed unsafely in a later operation |
| Storage Point | Application function where malicious input is saved to the database |
| Trigger Point | Separate function that retrieves stored data and uses it in an unsafe query |
| Trusted Data Assumption | Developer assumes database-stored data is safe, skipping parameterization |
| Stored Procedure Chains | Injection through stored procedures that use previously saved user data |
| Deferred Execution | Payload may not execute until hours or days after initial storage |
| Cross-Context Injection | Data stored by one user triggers execution in another user's context |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| SQLMap | Automated SQL injection with --second-url support for second-order attacks |
| Burp Suite | Request tracking and comparison across storage and trigger endpoints |
| OWASP ZAP | Automated scanning with injection detection |
| Commix | Automated command injection tool supporting second-order techniques |
| Custom Python scripts | Building automated storage-and-trigger exploitation chains |
| DBeaver/DataGrip | Direct database access for verifying stored payloads |

## Common Scenarios

1. **Username-Based Attack** — Register with a SQL injection payload as username; the payload executes when an admin views the user list
2. **Password Change Exploitation** — Store injection in username; when changing password, the application uses the stored username in an unsafe UPDATE query
3. **Report Generation Attack** — Inject payload in stored data fields; triggering report generation uses stored data in aggregate queries
4. **Cross-User Injection** — Inject payload in a shared data field (comments, reviews) that triggers when another user or admin processes the data
5. **Export Function Exploit** — Inject payload in profile data that triggers during CSV/PDF export operations

## Output Format

```
## Second-Order SQL Injection Report
- **Target**: http://target.com
- **Storage Point**: POST /register (username field)
- **Trigger Point**: GET /admin/users (admin panel)
- **Database**: MySQL 8.0

### Attack Flow
1. Registered user with username: `admin' UNION SELECT password FROM users--`
2. Application stored username safely using parameterized INSERT
3. Admin panel retrieves usernames with unsafe string concatenation in SELECT
4. Injected SQL executes, revealing all user passwords in admin view

### Data Extracted
| Table | Columns | Records |
|-------|---------|---------|
| users | username, password, email | 150 |
| admin_tokens | token, user_id | 3 |

### Remediation
- Use parameterized queries for ALL database operations, including reads
- Never trust data retrieved from the database as safe
- Implement output encoding when displaying database content
- Apply least-privilege database permissions
- Enable SQL query logging for detecting injection attempts
```