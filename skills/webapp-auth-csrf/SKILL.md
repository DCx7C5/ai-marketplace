---
name: webapp-auth-csrf
description: - During authorized web application penetration tests to identify state-changing actions vulnerable to CSRF - When testing the effectiveness of anti-CSRF token implementations - For validating SameSite cookie attribute enforcement across different browsers - When assessing applications that perform sensitive operations (password change, fund transf
domain: cybersecurity
---
------|-------------|
| **CSRF** | Attack that tricks an authenticated user's browser into making unintended requests to a vulnerable site |
| **Anti-CSRF Token** | A unique, unpredictable value tied to the user's session that must be included in state-changing requests |
| **SameSite Cookie** | Browser attribute (Strict, Lax, None) controlling when cookies are sent in cross-site requests |
| **Origin Header** | HTTP header indicating the origin of the request, used for CSRF validation |
| **Referer Header** | HTTP header containing the URL of the referring page, sometimes used for CSRF checks |
| **Double Submit Cookie** | CSRF defense that compares a cookie value with a request parameter value |
| **Synchronizer Token Pattern** | Server generates and validates a unique token per session or per request |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | CSRF PoC generator and request analysis |
| **OWASP ZAP** | Anti-CSRF token detection and CSRF testing |
| **XSRFProbe** | Automated CSRF vulnerability scanner (`pip install xsrfprobe`) |
| **Python http.server** | Local web server for hosting CSRF PoC pages |
| **Browser DevTools** | Inspecting cookies, SameSite attributes, and network requests |
| **CSRFTester (OWASP)** | Legacy tool for crafting and testing CSRF attacks |

## Common Scenarios

### Scenario 1: Email Change Without CSRF Token
The email change form does not include a CSRF token. An attacker hosts a page that auto-submits a form changing the victim's email to the attacker's address, enabling account takeover via password reset.

### Scenario 2: Fund Transfer with Token Bypass
The banking application has CSRF tokens but does not validate them if the parameter is omitted entirely. Removing the `csrf_token` field from the transfer form allows cross-site fund transfer.

### Scenario 3: JSON API CSRF via Content-Type Manipulation
A JSON API endpoint does not require a custom header. Using `enctype="text/plain"` in an HTML form, the attacker crafts a valid JSON body that changes the victim's account settings.

### Scenario 4: SameSite=Lax Bypass on GET State Change
A settings page changes state via GET request (`/settings?disable_2fa=true`). Since `SameSite=Lax` allows cookies on top-level GET navigations, linking the victim to this URL disables their 2FA.

## Output Format

```
## CSRF Vulnerability Finding

**Vulnerability**: Cross-Site Request Forgery (Email Change)
**Severity**: High (CVSS 8.0)
**Location**: POST /api/account/change-email
**OWASP Category**: A01:2021 - Broken Access Control

### Reproduction Steps
1. Authenticate as victim at https://target.example.com
2. Host the following HTML on an attacker-controlled server
3. Trick victim into visiting the attacker page while authenticated
4. The victim's email is changed to attacker@evil.com without consent

### Anti-CSRF Defenses Tested
| Defense | Present | Enforced |
|---------|---------|----------|
| CSRF Token | No | N/A |
| SameSite Cookie | Lax | Partial (GET bypass) |
| Origin Validation | No | N/A |
| Referer Validation | No | N/A |
| Custom Header Required | No | N/A |

### Impact
- Account takeover via email change + password reset chain
- Unauthorized fund transfers
- Settings modification (2FA disable, notification change)

### Recommendation
1. Implement synchronizer token pattern (anti-CSRF tokens) for all state-changing requests
2. Set SameSite=Strict on session cookies where possible
3. Validate Origin and Referer headers as defense-in-depth
4. Require re-authentication for sensitive operations (password change, fund transfer)
5. Use custom request headers (X-Requested-With) for AJAX endpoints
```