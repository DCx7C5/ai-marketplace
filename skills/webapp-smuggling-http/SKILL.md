---
name: webapp-smuggling-http
description: - During authorized penetration tests when the application sits behind a reverse proxy, load balancer, or CDN - When testing infrastructure with multiple HTTP processors in the request chain (nginx + Apache, HAProxy + Gunicorn) - For assessing applications for HTTP desynchronization vulnerabilities - When other attack vectors are limited and you ne
domain: cybersecurity
---
------|-------------|
| **CL.TE Smuggling** | Front-end uses Content-Length, back-end uses Transfer-Encoding |
| **TE.CL Smuggling** | Front-end uses Transfer-Encoding, back-end uses Content-Length |
| **TE.TE Smuggling** | Both use Transfer-Encoding but parse obfuscated TE headers differently |
| **HTTP Desync** | State where front-end and back-end disagree on request boundaries |
| **Request Splitting** | One HTTP request is interpreted as two separate requests |
| **Connection Poisoning** | Smuggled data affects the next request on the same TCP connection |
| **H2.CL Smuggling** | HTTP/2 to HTTP/1.1 downgrade with Content-Length discrepancy |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Manual request crafting with disabled auto Content-Length |
| **HTTP Request Smuggler (Burp)** | Automated smuggling detection extension by James Kettle |
| **smuggler.py** | Python-based automated HTTP request smuggling scanner |
| **h2cSmuggler** | HTTP/2 cleartext smuggling tool from Bishop Fox |
| **Turbo Intruder** | High-speed request engine for time-sensitive smuggling tests |
| **curl** | Manual HTTP request crafting with precise byte control |

## Common Scenarios

### Scenario 1: Admin Panel Access Bypass
The front-end proxy blocks `/admin` requests. A CL.TE smuggling attack prepends `GET /admin` to the back-end's request queue, causing the back-end to process the admin request without the front-end's access control check.

### Scenario 2: Cookie Theft via Request Capture
A TE.CL smuggling attack injects a partial POST request to a comment endpoint. The next user's request (including cookies and authorization headers) is appended to the comment body and stored in the database.

### Scenario 3: Cache Poisoning via Smuggling
A smuggled request causes the cache to store a response from a different URL. Combined with cache poisoning, the attacker serves malicious content to all users requesting the legitimate URL.

### Scenario 4: HTTP/2 Desync on CDN
The CDN accepts HTTP/2 and downgrades to HTTP/1.1 for the origin. A header injection via HTTP/2 creates a desync, allowing the attacker to smuggle requests that bypass the CDN's WAF rules.

## Output Format

```
## HTTP Request Smuggling Finding

**Vulnerability**: CL.TE HTTP Request Smuggling
**Severity**: Critical (CVSS 9.1)
**Location**: Front-end (Cloudflare) → Back-end (Nginx + Gunicorn)
**OWASP Category**: A05:2021 - Security Misconfiguration

### Architecture
Front-end: Cloudflare (Content-Length priority)
Back-end: Gunicorn (Transfer-Encoding priority)
Protocol: HTTP/1.1 between proxy and origin

### Reproduction Steps
1. Send POST request with both Content-Length and Transfer-Encoding headers
2. Content-Length set to include smuggled request prefix
3. Transfer-Encoding: chunked with "0\r\n\r\n" ending body
4. Smuggled data becomes prefix of next back-end request

### Confirmed Exploits
| Exploit | Impact |
|---------|--------|
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