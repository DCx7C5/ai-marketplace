---
name: webapp-auth-oauth-misconfig
description: - During authorized penetration tests when the application uses OAuth 2.0 or OpenID Connect for authentication - When assessing "Sign in with Google/Facebook/GitHub" social login implementations - For testing single sign-on (SSO) flows between applications - When evaluating API authorization using OAuth bearer tokens - During security assessments o
domain: cybersecurity
---
------|-------------|
| **Authorization Code Flow** | Most secure OAuth flow; exchanges short-lived code for tokens server-side |
| **Implicit Flow** | Deprecated flow returning tokens directly in URL fragment; vulnerable to leakage |
| **PKCE** | Proof Key for Code Exchange; prevents authorization code interception attacks |
| **Redirect URI Validation** | Server-side validation that the redirect_uri matches registered values |
| **State Parameter** | Random value binding the OAuth request to the user's session, preventing CSRF |
| **Scope Escalation** | Requesting or obtaining more permissions than authorized |
| **Token Leakage** | Exposure of OAuth tokens via Referer headers, logs, or browser history |
| **Open Redirect** | Using OAuth redirect_uri as an open redirect to steal tokens |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Intercepting OAuth redirect chains and modifying parameters |
| **OWASP ZAP** | Automated OAuth flow scanning |
| **Postman** | Manual OAuth flow testing with environment variables |
| **oauth-tools.com** | Online OAuth flow debugging and testing |
| **jwt.io** | JWT token analysis for OAuth access tokens |
| **Browser DevTools** | Monitoring network requests and redirect chains |

## Common Scenarios

### Scenario 1: Redirect URI Subdomain Bypass
The OAuth provider validates `redirect_uri` against `*.example.com`. An attacker finds a subdomain vulnerable to takeover (`old.example.com`), takes it over, and steals authorization codes redirected to it.

### Scenario 2: Missing State Parameter CSRF
The OAuth login flow does not include or validate a `state` parameter. An attacker crafts a link that logs the victim into the attacker's account, enabling account confusion attacks.

### Scenario 3: Implicit Flow Token Theft
The application uses the implicit flow, receiving the access token in the URL fragment. The callback page loads a third-party analytics script, and the token leaks via the Referer header.

### Scenario 4: Authorization Code Reuse
The OAuth provider does not invalidate authorization codes after first use. An attacker who intercepts a code via Referer leakage can exchange it for an access token even after the legitimate user has completed the flow.

## Output Format

```
## OAuth Security Assessment Report

**Vulnerability**: Redirect URI Validation Bypass
**Severity**: High (CVSS 8.1)
**Location**: GET /oauth/authorize - redirect_uri parameter
**OWASP Category**: A07:2021 - Identification and Authentication Failures

### OAuth Configuration
| Property | Value |
|----------|-------|
| Grant Type | Authorization Code |
| PKCE | Not implemented |
| State Parameter | Present but predictable |
| Token Type | JWT (RS256) |
| Token Lifetime | 1 hour |
| Refresh Token | 30 days |

### Findings
| Finding | Severity |
|---------|----------|
| Redirect URI path traversal bypass | High |
| Missing PKCE on public client | High |
| Authorization code reusable | Medium |
| State parameter uses sequential values | Medium |
| Client secret exposed in JavaScript | Critical |
| Token not revoked after password change | Medium |

### Recommendation
1. Implement strict redirect_uri validation with exact string matching
2. Require PKCE for all clients (especially public/mobile clients)
3. Invalidate authorization codes after first use
4. Use cryptographically random state parameters tied to user sessions
5. Migrate from implicit flow to authorization code flow with PKCE
6. Never expose client secrets in client-side code
```