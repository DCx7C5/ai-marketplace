---
name: webapp-api-injection-inject
description: - Testing API endpoints that accept user input for database queries, system commands, or external requests - Assessing APIs that interact with SQL databases, NoSQL stores (MongoDB, Redis), LDAP directories, or external URLs - Evaluating input validation and parameterized query usage across all API endpoints - Testing for SSRF where API parameters a
domain: cybersecurity
---
---|------------|
| **SQL Injection** | Inserting SQL code into API parameters that are concatenated into database queries, enabling data extraction or modification |
| **NoSQL Injection** | Injecting NoSQL operators ($ne, $gt, $regex) into MongoDB queries or manipulating Redis/Elasticsearch queries through API parameters |
| **SSRF** | Server-Side Request Forgery (OWASP API7:2023) - forcing the server to make HTTP requests to attacker-specified destinations including internal services |
| **Command Injection** | Injecting OS commands through API parameters that are passed to shell execution functions (exec, system, popen) |
| **Parameterized Queries** | Using prepared statements with bound parameters to prevent SQL injection by separating code from data |
| **Input Validation** | Server-side verification that user input conforms to expected format, type, length, and character set before processing |

## Tools & Systems

- **SQLMap**: Automated SQL injection detection and exploitation tool supporting all major database types
- **Burp Suite Professional**: Active scanner with injection detection for SQL, NoSQL, SSRF, and command injection
- **NoSQLMap**: Automated NoSQL injection detection and exploitation tool focused on MongoDB
- **SSRFmap**: SSRF detection and exploitation framework with cloud metadata extraction modules
- **Commix**: Automated OS command injection detection and exploitation tool

## Common Scenarios

### Scenario: E-Commerce API Injection Assessment

**Context**: An e-commerce API uses PostgreSQL for the product catalog, MongoDB for user sessions, and accepts webhook URLs for order notifications. The API is built with Node.js/Express.

**Approach**:
1. Test product search endpoint `GET /api/v1/products?search=test` with SQL payloads - discover error-based SQLi revealing PostgreSQL 14 backend
2. Exploit union-based SQLi to extract all table names, then dump user credentials from the `users` table
3. Test login endpoint with NoSQL operators - `{"username":{"$ne":""},"password":{"$ne":""}}` bypasses authentication
4. Test webhook URL endpoint for SSRF - `POST /api/v1/webhooks {"url":"http://169.254.169.254/latest/meta-data/"}` returns AWS instance metadata
5. Extract AWS IAM role credentials via SSRF, gaining access to S3 buckets containing customer data
6. Test file export endpoint for command injection - `GET /api/v1/export?filename=report;cat /etc/passwd` returns passwd file contents

**Pitfalls**:
- Only testing SQL injection when the backend uses multiple data stores (SQL, NoSQL, Redis, Elasticsearch)
- Missing injection points in HTTP headers (User-Agent, Referer, X-Forwarded-For) that may be logged to SQL databases
- Not testing SSRF bypass techniques when the initial payload is blocked by URL validation
- Assuming JSON API bodies are safe from SQL injection (JSON values are still concatenated into queries)
- Not testing time-based injection when error messages are suppressed

## Output Format

```
## Finding: SQL Injection in Product Search API Enables Full Database Access

**ID**: API-INJ-001
**Severity**: Critical (CVSS 9.8)
**OWASP API**: API8:2023 - Security Misconfiguration / Injection
**Affected Endpoints**:
  - GET /api/v1/products?search= (SQL injection)
  - POST /api/v1/auth/login (NoSQL injection)
  - POST /api/v1/webhooks (SSRF)

**Description**:
The product search API concatenates user input directly into a PostgreSQL
query without parameterization. An attacker can extract all database
contents including user credentials, payment information, and admin
secrets. Additionally, the login endpoint is vulnerable to MongoDB
NoSQL operator injection, and the webhook endpoint allows SSRF to
internal services and cloud metadata.

**Impact**:
- Full database read/write access via SQL injection
- Authentication bypass via NoSQL operator injection
- AWS IAM credential theft via SSRF to instance metadata
- Potential remote code execution via SQL injection stacked queries

**Remediation**:
1. Use parameterized queries for all database operations
2. Validate and sanitize NoSQL operator characters in JSON input
3. Implement URL allowlisting for webhook and callback URLs
4. Block access to cloud metadata endpoints (169.254.169.254) from application servers
5. Use an ORM with parameterized queries and disable raw query methods
6. Implement WAF rules for common injection patterns as defense in depth
```