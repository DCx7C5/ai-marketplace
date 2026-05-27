---
name: webapp-api-mobile
description: "Webapp Api Mobile."
domain: cybersecurity
---

--|
| **BOLA/IDOR** | Broken Object Level Authorization - accessing resources by changing identifiers without server-side authorization checks |
| **JWT** | JSON Web Token - self-contained authentication token with header, payload, and signature components |
| **PKCE** | Proof Key for Code Exchange - OAuth 2.0 extension preventing authorization code interception in mobile apps |
| **Token Refresh** | Mechanism for obtaining new access tokens using long-lived refresh tokens without re-authentication |
| **Session Fixation** | Attack where adversary sets a known session ID before victim authenticates, then hijacks the session |

## Tools & Systems

- **Burp Suite**: HTTP proxy for intercepting and modifying authentication requests
- **jwt_tool**: Python tool for testing JWT vulnerabilities (none algorithm, key confusion, claim manipulation)
- **Postman**: API testing client for crafting authentication requests
- **hashcat**: Password/JWT secret cracking tool for testing HMAC signing key strength
- **Autorize**: Burp Suite extension for automated authorization testing

## Common Pitfalls

- **Rate limiting masks issues**: API may rate-limit test requests. Use delays between requests and test from the tester's authorized perspective first.
- **Token in URL**: Some mobile APIs pass tokens in URL query parameters, exposing them in server logs and browser history. Flag as finding even if authorization works correctly.
- **Refresh token rotation**: Some APIs rotate refresh tokens on each use. If your test invalidates the refresh token, you may lock out your test account.
- **Mobile-specific OAuth**: Mobile apps use custom URI schemes for OAuth redirects, which can be intercepted by malicious apps registered for the same scheme.
