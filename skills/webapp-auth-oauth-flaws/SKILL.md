---
name: webapp-auth-oauth-flaws
description: "Webapp Auth Oauth Flaws."
domain: cybersecurity
---

|
| **Authorization Code Flow** | OAuth 2.0 flow where the client receives an authorization code via redirect, then exchanges it for tokens at the token endpoint |
| **PKCE** | Proof Key for Code Exchange - extension that binds the authorization request to the token request using a code verifier/challenge, preventing authorization code interception |
| **Redirect URI Validation** | Authorization server verification that the redirect_uri matches the registered value exactly, preventing code/token theft via open redirect |
| **State Parameter** | Random value passed in the authorization request and verified in the callback to prevent CSRF attacks on the OAuth flow |
| **Scope Escalation** | Requesting or obtaining more permissions (scopes) than the client is authorized for, enabling unauthorized access |
| **Implicit Flow** | Deprecated OAuth flow that returns tokens directly in the URL fragment, vulnerable to token leakage and replay attacks |

## Tools & Systems

- **Burp Suite Professional**: Intercept and manipulate OAuth redirects, authorization codes, and token exchanges
- **EsPReSSO (Burp Extension)**: Automated testing of OAuth and OpenID Connect implementations for known vulnerabilities
- **oauth2-security-tester**: Dedicated tool for testing OAuth 2.0 flows against common attack patterns
- **OWASP ZAP**: Passive scanner that detects OAuth misconfigurations in intercepted traffic
- **jwt.io**: Online JWT decoder for analyzing OAuth access tokens and ID tokens

## Common Scenarios

### Scenario: Social Login OAuth Implementation Assessment

**Context**: A web application implements "Login with Google" and "Login with GitHub" using OAuth 2.0 Authorization Code flow. The application is a SaaS platform where account takeover has high business impact.

**Approach**:
1. Analyze the OAuth configuration at `/.well-known/openid-configuration` for both providers
2. Test redirect URI validation: discover that the application registers `https://app.example.com/callback` but the server accepts `https://app.example.com/callback/..%2fevil`
3. Test state parameter: authorization request includes state but the callback handler does not validate it (CSRF possible)
4. Test PKCE: not implemented for the authorization code flow, making code interception possible on mobile
5. Test implicit flow: still enabled despite not being used by the application
6. Test scope: application requests `openid profile email` but the authorization server also grants `read:repos` without explicit consent
7. Test authorization code replay: code can be exchanged twice, indicating lack of single-use enforcement
8. Test token audience: access token from Google login accepted by GitHub API endpoint (audience not validated)

**Pitfalls**:
- Only testing the OAuth flow in the browser without intercepting and manipulating redirect parameters
- Not testing both the authorization request and the token exchange independently
- Missing open redirect vulnerabilities in the application that can be chained with OAuth redirect_uri
- Not testing the state parameter validation on the client side (server may include it but client may not check it)
- Assuming PKCE is enforced because the authorization server supports it (client must also send it)

## Output Format

```
## Finding: OAuth2 Redirect URI Bypass Enables Authorization Code Theft

**ID**: API-OAUTH-001
**Severity**: Critical (CVSS 9.3)
**Affected Component**: OAuth 2.0 Authorization Code Flow
**Authorization Server**: auth.example.com

**Description**:
The authorization server's redirect_uri validation uses prefix matching
instead of exact string matching. An attacker can manipulate the redirect_uri
to redirect the authorization code to an attacker-controlled endpoint,
enabling account takeover. Additionally, PKCE is not enforced and the
state parameter is not validated by the client application.

**Proof of Concept**:
1. Craft authorization URL with manipulated redirect_uri:
   https://auth.example.com/authorize?response_type=code&client_id=app
   &redirect_uri=https://app.example.com/callback/../../../evil.com
   &scope=openid+profile+email&state=abc123
2. User authenticates and approves consent
3. Authorization code redirected to https://evil.com?code=AUTH_CODE&state=abc123
4. Attacker exchanges code at token endpoint (no PKCE required)
5. Attacker receives access token and ID token for victim's account

**Impact**:
Complete account takeover for any user who clicks a crafted OAuth login link.
The attacker gains full access to the user's profile, email, and any
resources the OAuth scope grants access to.

**Remediation**:
1. Implement exact string matching for redirect_uri validation (no wildcards, no prefix matching)
2. Enforce PKCE (S256 method) for all authorization code flow requests
3. Validate the state parameter in the callback handler before exchanging the code
4. Disable the implicit flow on the authorization server
5. Enforce single-use authorization codes with a short TTL (max 60 seconds)
6. Validate the audience (aud) claim in tokens before accepting them
```
