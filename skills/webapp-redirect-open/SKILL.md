---
name: webapp-redirect-open
description: - When testing login/logout flows that redirect users to specified URLs - During assessment of OAuth authorization endpoints with redirect_uri parameters - When auditing applications with URL parameters (next, url, redirect, return, goto, target) - During phishing simulation to chain open redirects with credential harvesting - When testing SSO impl
domain: cybersecurity
---
------|-------------|
| Unvalidated Redirect | Application redirects to user-supplied URL without checking destination |
| URL Parsing Inconsistency | Different libraries parse URLs differently, enabling bypass |
| Protocol-Relative URL | Using // prefix to redirect while inheriting current protocol |
| Userinfo Abuse | Using @ symbol to make URL appear to belong to trusted domain |
| Open Redirect Chain | Combining multiple open redirects or chaining with other vulnerabilities |
| DOM-Based Redirect | Client-side JavaScript performing redirect using attacker-controlled input |
| Meta Refresh Redirect | HTML meta tag performing redirect without server-side 302 |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| OpenRedireX | Automated open redirect vulnerability testing tool |
| Burp Suite | HTTP proxy for intercepting and modifying redirect parameters |
| gf (tomnomnom) | Pattern matcher to extract redirect parameters from URL lists |
| nuclei | Template-based scanner with open redirect detection templates |
| ffuf | Fuzzer for mass-testing redirect parameter payloads |
| OWASP ZAP | Automated scanner with open redirect detection |

## Common Scenarios

1. **Phishing Amplification** — Use open redirect on a trusted domain to lend credibility to phishing URLs targeting users
2. **OAuth Token Theft** — Exploit open redirect as redirect_uri in OAuth flows to steal authorization codes and access tokens
3. **SSO Bypass** — Redirect SSO authentication responses to attacker-controlled servers to capture session tokens
4. **XSS via Redirect** — Chain open redirect with javascript: protocol to achieve cross-site scripting
5. **Referer Leakage** — Use open redirect to leak sensitive tokens in Referer headers when redirecting to external sites

## Output Format

```
## Open Redirect Assessment Report
- **Target**: http://target.com
- **Vulnerable Parameters Found**: 3
- **Bypass Techniques Required**: URL encoding, userinfo abuse

### Findings
| # | Endpoint | Parameter | Payload | Impact |
|---|----------|-----------|---------|--------|
| 1 | /login | next | //evil.com | Phishing |
| 2 | /oauth/authorize | redirect_uri | https://target.com@evil.com | Token Theft |
| 3 | /logout | return | https://evil.com%00.target.com | Session Redirect |

### Remediation
- Implement allowlist of permitted redirect destinations
- Validate redirect URLs server-side using strict URL parsing
- Reject any redirect URL containing external domains
- Use indirect reference maps instead of direct URL parameters
```