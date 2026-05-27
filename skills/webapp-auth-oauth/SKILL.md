---
name: webapp-auth-oauth
description: "Webapp Auth Oauth."
domain: cybersecurity
---

-|
| Access Control | AC-3 | Token-based access enforcement |
| Authentication | IA-5 | Client credential management |
| Session Management | SC-23 | Token lifecycle management |
| Audit | AU-3 | Log all token issuance and revocation |
| Cryptographic Protection | SC-13 | PKCE and token signing |

## Common Pitfalls
- Using implicit grant (removed in OAuth 2.1) instead of authorization code + PKCE
- Storing tokens in localStorage (XSS vulnerable) instead of httpOnly cookies
- Not validating state parameter enabling CSRF attacks
- Using wildcard redirect URIs allowing open redirect exploitation
- Not implementing refresh token rotation allowing token theft persistence

## Verification
- [ ] Authorization Code + PKCE flow completes successfully
- [ ] PKCE code_challenge validated at token endpoint
- [ ] State parameter prevents CSRF
- [ ] Access tokens expire within configured lifetime
- [ ] Refresh token rotation issues new refresh token each use
- [ ] Token revocation invalidates both access and refresh tokens
- [ ] Client Credentials flow works for service-to-service calls
- [ ] Scopes correctly enforced at resource server
