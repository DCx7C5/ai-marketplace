---
name: webapp-auth-oauth-misconfig
description: "Webapp Auth Oauth Misconfig."
domain: cybersecurity
---

-|
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
