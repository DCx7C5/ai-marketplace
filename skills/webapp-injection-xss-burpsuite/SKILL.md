---
name: webapp-injection-xss-burpsuite
description: - During authorized web application penetration testing to find reflected, stored, and DOM-based XSS - When validating XSS findings reported by automated vulnerability scanners - For testing the effectiveness of Content Security Policy (CSP) and XSS filters - When assessing client-side security of single-page applications (SPAs) - During bug bounty
domain: cybersecurity
---
------|-------------|
| **Reflected XSS** | Payload is included in the server response immediately from the current HTTP request |
| **Stored XSS** | Payload is persisted on the server (database, file) and served to other users |
| **DOM-based XSS** | Payload is processed entirely client-side by JavaScript without server reflection |
| **XSS Sink** | A JavaScript function or DOM property that executes or renders untrusted input |
| **XSS Source** | A location where attacker-controlled data enters the client-side application |
| **CSP** | Content Security Policy header that restricts which scripts can execute on a page |
| **Context-aware encoding** | Applying the correct encoding (HTML, JS, URL, CSS) based on output context |
| **Mutation XSS (mXSS)** | XSS that exploits browser HTML parser inconsistencies during DOM serialization |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Primary testing platform with scanner, intruder, repeater, and DOM Invader |
| **DOM Invader** | Burp's built-in browser extension for DOM XSS testing |
| **Hackvertor** | Burp BApp for advanced payload encoding and transformation |
| **XSS Hunter** | Blind XSS detection platform that captures execution evidence |
| **Dalfox** | CLI-based XSS scanner with parameter analysis (`go install github.com/hahwul/dalfox/v2@latest`) |
| **CSP Evaluator** | Google tool for analyzing Content Security Policy effectiveness |

## Common Scenarios

### Scenario 1: Search Function Reflected XSS
A search page reflects the query parameter in the results heading without encoding. Inject `<script>alert(document.domain)</script>` in the search parameter and demonstrate cookie theft via reflected XSS.

### Scenario 2: Comment System Stored XSS
A blog comment form sanitizes `<script>` tags but allows `<img>` tags. Use `<img src=x onerror=alert(document.domain)>` to achieve stored XSS that fires for every visitor loading the page.

### Scenario 3: SPA with DOM-based XSS
A React/Angular SPA reads `window.location.hash` and injects it into the DOM via `innerHTML`. Use DOM Invader to trace the source-to-sink flow and craft a payload in the URL fragment.

### Scenario 4: XSS Behind WAF with Strict CSP
A WAF blocks common XSS patterns and CSP restricts inline scripts. Discover a JSONP endpoint on a whitelisted domain and use it as a script gadget to bypass CSP.

## Output Format

```
## XSS Vulnerability Finding

**Vulnerability**: Stored Cross-Site Scripting (XSS)
**Severity**: High (CVSS 8.1)
**Location**: POST /api/comments → `body` parameter
**Type**: Stored XSS
**OWASP Category**: A03:2021 - Injection

### Reproduction Steps
1. Navigate to https://target.example.com/blog/post/123
2. Submit a comment with body: <img src=x onerror=alert(document.domain)>
3. Reload the page; the payload executes in the browser

### Impact
- Session hijacking via cookie theft for all users viewing the page
- Account takeover through session token exfiltration
- Defacement of the blog post page
- Phishing via injected login forms

### CSP Status
- No Content-Security-Policy header present
- X-XSS-Protection header not set

### Recommendation
1. Implement context-aware output encoding (HTML entity encoding for HTML context)
2. Deploy Content Security Policy with strict nonce-based script allowlisting
3. Use DOMPurify library for sanitizing user-generated HTML content
4. Set HttpOnly and Secure flags on session cookies
5. Add X-Content-Type-Options: nosniff header
```