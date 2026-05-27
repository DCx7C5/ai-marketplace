---
name: webapp-injection-sqli-nosql
description: - During web application penetration testing of applications using NoSQL databases - When testing authentication mechanisms backed by MongoDB or similar databases - When assessing APIs that accept JSON input for database queries - During bug bounty hunting on applications with NoSQL backends - When performing security code review of database query 
domain: cybersecurity
---
------|-------------|
| Operator Injection | Injecting MongoDB operators ($ne, $gt, $regex) into query parameters |
| Authentication Bypass | Using operators to match any document and bypass login checks |
| Blind Extraction | Character-by-character data extraction using $regex boolean responses |
| $where Injection | Executing arbitrary JavaScript on the MongoDB server via $where operator |
| Type Juggling | Exploiting how NoSQL databases handle different input types (string vs object) |
| BSON Injection | Manipulating Binary JSON serialization in MongoDB wire protocol |
| Server-Side JS | JavaScript execution context available in MongoDB for query evaluation |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| NoSQLMap | Automated NoSQL injection detection and exploitation framework |
| Burp Suite | HTTP proxy for intercepting and modifying JSON requests |
| MongoDB Shell | Direct database interaction for testing query behavior |
| nosqli | Dedicated NoSQL injection scanner and exploitation tool |
| PayloadsAllTheThings | Curated NoSQL injection payload repository |
| Nuclei | Template-based scanner with NoSQL injection detection templates |
| Postman | API testing platform for crafting NoSQL injection requests |

## Common Scenarios

1. **Login Bypass** — Bypass MongoDB-backed authentication using `{"$ne": ""}` operator injection in username and password fields
2. **Data Enumeration** — Extract database contents character by character using `$regex` blind injection when no direct output is visible
3. **Privilege Escalation** — Modify user role fields through NoSQL injection in profile update endpoints
4. **API Key Extraction** — Extract API keys or tokens stored in MongoDB collections through boolean-based blind techniques
5. **Account Takeover** — Enumerate valid usernames via regex injection then brute-force passwords through operator-based authentication bypass

## Output Format

```
## NoSQL Injection Assessment Report
- **Target**: http://target.com/api/login
- **Database**: MongoDB 6.0
- **Vulnerability Type**: Operator Injection (Authentication Bypass)
- **Severity**: Critical (CVSS 9.8)

### Vulnerable Parameters
| Endpoint | Parameter | Injection Type | Impact |
|----------|-----------|---------------|--------|
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