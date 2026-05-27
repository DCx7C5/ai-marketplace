---
name: webapp-injection-sqli-sqlmap
description: - During authorized web application penetration testing engagements - When manual testing reveals potential SQL injection points in parameters, headers, or cookies - For validating SQL injection findings from automated scanners like Burp Suite or OWASP ZAP - When you need to demonstrate the impact of SQL injection by extracting data from backend da
domain: cybersecurity
---
------|-------------|
| **Union-based SQLi** | Uses UNION SELECT to append attacker query results to the original query output |
| **Blind Boolean SQLi** | Infers data one bit at a time by observing true/false application responses |
| **Blind Time-based SQLi** | Uses database sleep functions (e.g., `SLEEP(5)`) to infer data based on response delays |
| **Error-based SQLi** | Extracts data through verbose database error messages returned in HTTP responses |
| **Stacked Queries** | Executes multiple SQL statements separated by semicolons for INSERT/UPDATE/DELETE operations |
| **Out-of-band SQLi** | Exfiltrates data via DNS or HTTP requests initiated by the database server |
| **Tamper Scripts** | sqlmap plugins that modify payloads to bypass WAFs and input sanitization filters |
| **Second-order SQLi** | Injected payload is stored and executed later in a different query context |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **sqlmap** | Automated SQL injection detection and exploitation framework |
| **Burp Suite Professional** | HTTP proxy for intercepting, modifying, and replaying requests |
| **OWASP ZAP** | Free alternative to Burp for web application scanning and proxying |
| **Havij** | Automated SQL injection tool with GUI (Windows) |
| **jSQL Injection** | Java-based GUI tool for SQL injection testing |
| **DBeaver/DataGrip** | Database clients for verifying extracted data structure |

## Common Scenarios

### Scenario 1: E-commerce Product Page SQLi
A product detail page uses `id` parameter directly in SQL query. Use sqlmap to extract the full customer database including payment information to demonstrate critical business impact.

### Scenario 2: Login Form Bypass
A login form concatenates user input into an authentication query. Exploit to bypass authentication and enumerate all user credentials stored in the database.

### Scenario 3: Search Function with WAF Protection
A search feature is vulnerable to SQL injection but protected by a WAF. Use tamper scripts like `space2comment` and `between` to encode payloads and bypass the filter rules.

### Scenario 4: Cookie-based Blind SQL Injection
A session cookie value is used in a database query on the server side. Use time-based blind injection techniques to extract data character by character.

## Output Format

```
## SQL Injection Finding

**Vulnerability**: SQL Injection (Union-based)
**Severity**: Critical (CVSS 9.8)
**Location**: GET parameter `id` at /products?id=1
**Database**: MySQL 8.0.32
**Impact**: Full database read access, 15,000 user records exposed
**OWASP Category**: A03:2021 - Injection

### Evidence
- Injection point: `id` parameter (GET)
- Technique: UNION query-based
- Backend DBMS: MySQL >= 5.0
- Current user: app_user@localhost
- DBA privileges: No

### Databases Enumerated
1. information_schema
2. target_app_db
3. mysql

### Sensitive Data Exposed
- Table: users (15,247 rows)
- Columns: id, username, email, password_hash, created_at

### Recommendation
1. Use parameterized queries (prepared statements) for all database interactions
2. Implement input validation with allowlists for expected data types
3. Apply least-privilege database permissions for the application user
4. Deploy a Web Application Firewall as defense-in-depth
5. Enable database query logging and monitoring for anomalous patterns
```