---
name: webapp-headers-security
description: - During authorized web application security assessments as a standard configuration review - When evaluating browser-level protections against XSS, clickjacking, and data leakage - For compliance assessments requiring security header implementation (PCI DSS, SOC 2) - When performing initial reconnaissance to identify easy-win security improvements
domain: cybersecurity
---
------|-------------|
| **HSTS** | Forces browsers to only use HTTPS for the domain, preventing protocol downgrade attacks |
| **CSP** | Restricts which resources (scripts, styles, images) can load on the page |
| **X-Frame-Options** | Controls whether the page can be embedded in iframes (clickjacking defense) |
| **X-Content-Type-Options** | Prevents MIME type sniffing; forces browser to respect declared Content-Type |
| **Referrer-Policy** | Controls how much referrer information is sent with cross-origin requests |
| **Permissions-Policy** | Restricts browser features (camera, microphone, geolocation) available to the page |
| **SameSite Cookie** | Controls when cookies are sent in cross-site contexts (Strict, Lax, None) |
| **HSTS Preloading** | Hardcoding HSTS policy in browser source code for first-visit protection |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **SecurityHeaders.com** | Online scanner providing letter-grade security header assessment |
| **Mozilla Observatory** | Comprehensive web security scanner with scoring and recommendations |
| **CSP Evaluator (Google)** | Analyzes Content Security Policy for weaknesses and bypasses |
| **Burp Suite Professional** | Inspecting response headers across all application pages |
| **securityheaders (CLI)** | Command-line security header scanner |
| **Hardenize** | TLS and security header monitoring service |

## Common Scenarios

### Scenario 1: Complete Header Absence
A legacy application returns no security headers at all. No HSTS, CSP, X-Frame-Options, or cookie security flags. Every page is vulnerable to clickjacking, XSS has no browser-level mitigation, and cookies are sent over HTTP.

### Scenario 2: Weak CSP with unsafe-inline
The CSP header includes `script-src 'self' 'unsafe-inline'`. While it restricts external script loading, the `unsafe-inline` directive allows any inline script to execute, rendering the CSP ineffective against XSS.

### Scenario 3: Session Cookie Without Secure Flag
The session cookie is set without the `Secure` flag. On mixed HTTP/HTTPS sites, the session token can be intercepted by a network attacker via a plain HTTP request.

### Scenario 4: Missing HSTS Enabling SSL Stripping
No HSTS header is present. An attacker on the network can perform an SSL stripping attack, downgrading the victim's HTTPS connection to HTTP and intercepting all traffic.

## Output Format

```
## Security Headers Audit Report

**Target**: target.example.com
**Grade**: D (SecurityHeaders.com)
**Assessment Date**: 2024-01-15

### Headers Assessment
| Header | Status | Current Value | Recommended |
|--------|--------|---------------|-------------|
| Strict-Transport-Security | MISSING | - | max-age=31536000; includeSubDomains; preload |
| Content-Security-Policy | WEAK | script-src 'self' 'unsafe-inline' | script-src 'self' 'nonce-{random}' |
| X-Frame-Options | MISSING | - | DENY |
| X-Content-Type-Options | PRESENT | nosniff | nosniff (OK) |
| Referrer-Policy | MISSING | - | strict-origin-when-cross-origin |
| Permissions-Policy | MISSING | - | camera=(), microphone=(), geolocation=() |
| X-XSS-Protection | MISSING | - | 0 (with strong CSP) |

### Cookie Security
| Cookie | Secure | HttpOnly | SameSite | Path |
|--------|--------|----------|----------|------|
| session | NO | YES | Not set | / |
| user_pref | NO | NO | Not set | / |
| csrf_token | YES | NO | Strict | / |

### Information Disclosure
| Header | Value | Risk |
|--------|-------|------|
| Server | Apache/2.4.52 | Technology fingerprinting |
| X-Powered-By | PHP/8.1.2 | Version-specific exploit targeting |

### Recommendation Priority
1. **Critical**: Add Secure and SameSite flags to session cookie
2. **High**: Implement HSTS with min 1-year max-age
3. **High**: Replace 'unsafe-inline' in CSP with nonce-based policy
4. **Medium**: Add X-Frame-Options: DENY
5. **Medium**: Add Referrer-Policy: strict-origin-when-cross-origin
6. **Low**: Remove Server and X-Powered-By version information
7. **Low**: Add Permissions-Policy to restrict unused browser features
```