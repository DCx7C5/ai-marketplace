---
name: webapp-headers-cors
description: - During authorized penetration tests when assessing API endpoints for cross-origin access controls - When testing single-page applications that make cross-origin API requests - For evaluating whether sensitive data can be exfiltrated from a victim's browser session - When assessing microservice architectures with multiple domains sharing data - Du
domain: cybersecurity
---
------|-------------|
| **Same-Origin Policy** | Browser security model preventing scripts from one origin accessing data from another |
| **CORS** | Mechanism allowing servers to specify which origins can access their resources |
| **Origin Reflection** | Server mirrors the request Origin header in the ACAO response header (dangerous) |
| **Null Origin** | Special origin value from sandboxed iframes, data URIs, and redirects |
| **Preflight Request** | OPTIONS request sent before certain cross-origin requests to check permissions |
| **Credentialed Requests** | Cross-origin requests that include cookies, requiring explicit ACAO + ACAC headers |
| **Wildcard CORS** | `Access-Control-Allow-Origin: *` allows any origin but prohibits credentials |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Intercepting requests and modifying Origin headers |
| **CORScanner** | Automated CORS misconfiguration scanner (`pip install corscanner`) |
| **cors-scanner** | Node.js-based CORS testing tool |
| **Browser DevTools** | Monitoring CORS errors and network requests in real browser context |
| **Python http.server** | Hosting CORS exploit PoC pages |
| **OWASP ZAP** | Automated CORS misconfiguration detection |

## Common Scenarios

### Scenario 1: Full Origin Reflection
The API reflects any Origin header in `Access-Control-Allow-Origin` with `Access-Control-Allow-Credentials: true`. Any website can read authenticated API responses, stealing user data.

### Scenario 2: Null Origin Allowed
The server allows `Origin: null` with credentials. Using a sandboxed iframe, an attacker page sends credentialed requests to the API and reads the response data.

### Scenario 3: Subdomain Wildcard Trust
The CORS policy allows `*.target.example.com`. An attacker finds XSS on `forum.target.example.com` and uses it to make cross-origin requests to `api.target.example.com`, stealing user data through the trusted subdomain.

### Scenario 4: Regex Bypass on Origin Validation
The server uses regex `target\.example\.com` to validate origins, but fails to anchor the regex. `attackertarget.example.com` matches and is allowed access.

## Output Format

```
## CORS Misconfiguration Finding

**Vulnerability**: CORS Origin Reflection with Credentials
**Severity**: High (CVSS 8.1)
**Location**: All /api/* endpoints on api.target.example.com
**OWASP Category**: A01:2021 - Broken Access Control

### CORS Configuration Observed
| Header | Value |
|--------|-------|
| Access-Control-Allow-Origin | [Reflects request Origin] |
| Access-Control-Allow-Credentials | true |
| Access-Control-Allow-Methods | GET, POST, PUT, DELETE |
| Access-Control-Expose-Headers | X-Auth-Token |

### Origin Validation Results
| Origin Tested | Reflected | Credentials |
|---------------|-----------|-------------|
| https://evil.com | Yes | Yes |
| null | Yes | Yes |
| http://localhost | Yes | Yes |
| https://evil.target.example.com | Yes | Yes |

### Impact
- Any website can read authenticated API responses in victim's browser
- User profile data (email, phone, address) exfiltrable
- Session tokens exposed via X-Auth-Token header
- CSRF protection bypassed (attacker can read and submit anti-CSRF tokens)

### Recommendation
1. Implement a strict allowlist of trusted origins
2. Never reflect arbitrary Origin values in Access-Control-Allow-Origin
3. Do not allow Origin: null with credentials
4. Validate origins with exact string matching, not regex substring matching
5. Set Access-Control-Max-Age to a reasonable value (600 seconds)
```