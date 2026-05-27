---
name: webapp-ui-clickjacking
description: - During authorized penetration tests when assessing UI redressing vulnerabilities - When testing whether sensitive actions (delete account, transfer funds, change settings) can be performed via clickjacking - For evaluating the effectiveness of X-Frame-Options and Content-Security-Policy frame-ancestors directives - When assessing applications tha
domain: cybersecurity
---
------|-------------|
| **Clickjacking** | UI redressing attack that tricks users into clicking hidden elements by overlaying decoy content |
| **X-Frame-Options** | HTTP header controlling whether a page can be embedded in iframes (DENY, SAMEORIGIN) |
| **frame-ancestors** | CSP directive specifying valid parents for iframe embedding (supersedes X-Frame-Options) |
| **Frame Busting** | JavaScript-based defense that attempts to break out of iframes (easily bypassable) |
| **Likejacking** | Clickjacking variant targeting social media "Like" or "Share" buttons |
| **Cursorjacking** | Variant using CSS to offset the visible cursor from the actual click position |
| **Multi-step Clickjacking** | Attack requiring multiple clicks, with decoy content changing at each step |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Examining X-Frame-Options and CSP headers on responses |
| **Clickjack Tester (browser)** | Browser-based iframe embedding test tool |
| **Browser DevTools** | Inspecting frame embedding behavior and console errors |
| **Python http.server** | Hosting clickjacking PoC pages locally |
| **OWASP ZAP** | Automated detection of missing anti-framing headers |
| **securityheaders.com** | Online scanner for missing security headers |

## Common Scenarios

### Scenario 1: Account Deletion via Clickjacking
The account deletion page at `/account/delete` has no X-Frame-Options header. An attacker creates a page with a "Win a prize" button positioned over the "Delete My Account" button in a transparent iframe.

### Scenario 2: One-Click Fund Transfer
A banking application performs transfers via a single button click on a pre-filled form. Without frame protection, the attacker embeds the transfer page in an iframe and overlays a decoy "Play Game" button.

### Scenario 3: 2FA Disable via Multi-Step Clickjacking
Disabling two-factor authentication requires two clicks (settings link, then disable button). A multi-step clickjacking PoC guides the victim through two decoy clicks that align with the real buttons.

### Scenario 4: OAuth Authorization Clickjack
An OAuth consent screen allows framing. The attacker embeds the consent page and tricks the victim into clicking "Authorize", granting the attacker's application access to the victim's account.

## Output Format

```
## Clickjacking Vulnerability Finding

**Vulnerability**: Clickjacking - Missing Frame Embedding Protection
**Severity**: Medium (CVSS 6.1)
**Location**: /account/settings, /account/delete, /transfer
**OWASP Category**: A04:2021 - Insecure Design

### Headers Analysis
| Page | X-Frame-Options | CSP frame-ancestors | Vulnerable |
|------|----------------|--------------------|-|
| / | Not set | Not set | Yes |
| /account/settings | Not set | Not set | Yes |
| /account/delete | Not set | Not set | Yes |
| /transfer | Not set | Not set | Yes |
| /login | SAMEORIGIN | - | No |

### Sensitive Actions Exploitable
1. Account deletion (single click, no re-authentication)
2. Email change (single click, no confirmation)
3. 2FA disable (two clicks, multi-step PoC)
4. Fund transfer (pre-filled form, single click)

### Impact
- Account takeover via email change clickjacking
- Account destruction via delete clickjacking
- Financial loss via transfer clickjacking
- Security downgrade via 2FA disable clickjacking

### Recommendation
1. Add `Content-Security-Policy: frame-ancestors 'none'` to all pages
2. Set `X-Frame-Options: DENY` as fallback for older browsers
3. Require re-authentication for sensitive actions (delete, transfer)
4. Add confirmation dialogs that cannot be pre-filled or auto-submitted
5. Implement SameSite=Strict cookies to reduce session availability in frames
```