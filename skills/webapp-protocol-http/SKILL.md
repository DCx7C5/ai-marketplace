---
name: webapp-protocol-http
description: - When testing web applications for input validation bypass vulnerabilities - During WAF evasion testing to split attack payloads across duplicate parameters - When assessing how different technology stacks handle duplicate HTTP parameters - During API security testing to identify parameter precedence issues - When testing OAuth or payment processi
domain: cybersecurity
---
------|-------------|
| Server-Side HPP | Duplicate parameters processed differently by backend causing logic bypass |
| Client-Side HPP | Injected parameters reflected in URLs/links sent to other users |
| Parameter Precedence | Server behavior: first-wins, last-wins, concatenation, or array |
| WAF Evasion | Splitting attack payloads across duplicate parameters to avoid detection |
| Technology-Specific Parsing | Different frameworks handle duplicate parameters uniquely |
| URL Encoding HPP | Using %26 (encoded &) to inject additional parameters within a value |
| Header Pollution | Sending duplicate HTTP headers to exploit forwarding or trust logic |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy for intercepting and duplicating parameters |
| param-miner | Burp extension for discovering hidden and duplicate parameters |
| OWASP ZAP | Automated scanner with HPP detection capabilities |
| Arjun | Hidden HTTP parameter discovery tool |
| ffuf | Fuzzing tool for parameter brute-forcing and duplication testing |
| Wfuzz | Web application fuzzer supporting parameter manipulation |

## Common Scenarios

1. **WAF Bypass** — Split SQL injection or XSS payloads across duplicate parameters where the WAF inspects values individually but the server concatenates them
2. **Payment Manipulation** — Override price or quantity parameters in e-commerce checkout flows by submitting duplicate parameter values
3. **OAuth Redirect Hijacking** — Inject a duplicate redirect_uri parameter to redirect authorization codes to an attacker-controlled server
4. **Access Control Bypass** — Override role or permission parameters in requests to elevate privileges or access restricted resources
5. **Input Validation Bypass** — Circumvent client-side or server-side validation by injecting unexpected duplicate parameters

## Output Format

```
## HTTP Parameter Pollution Assessment Report
- **Target**: http://target.com
- **Server Technology**: ASP.NET/IIS (concatenation behavior)
- **Vulnerability**: Server-Side HPP in payment endpoint

### Parameter Handling Matrix
| Technology | Behavior | Tested |
|-----------|----------|--------|
| Apache/PHP | Last value | Yes |
| IIS/ASP.NET | Comma-concatenated | Yes |
| Node.js | Array | Yes |

### Findings
| # | Endpoint | Parameter | Impact | Severity |
|---|----------|-----------|--------|----------|
| 1 | POST /checkout | price | Price manipulation | Critical |
| 2 | GET /oauth/authorize | redirect_uri | Token theft | High |
| 3 | POST /api/search | q | WAF bypass (SQLi) | High |

### Remediation
- Implement strict parameter validation rejecting duplicate parameters
- Use the first occurrence of any parameter and ignore subsequent duplicates
- Apply WAF rules that detect duplicate parameter patterns
- Validate all parameters server-side regardless of client-side checks
```