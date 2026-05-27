---
name: webapp-auth-jwt-tokensec
description: "Webapp Auth Jwt Tokensec."
domain: cybersecurity
---

--|
| Algorithm None | Blocked |
| Algorithm Confusion (RS256→HS256) | VULNERABLE |
| HMAC Brute Force | N/A (RSA) |
| KID Injection | Not present |
| Expired Token Reuse | Accepted (no revocation) |

### Impact
- Complete authentication bypass via forged admin tokens
- Any user can escalate to any role by forging JWT claims
- Tokens remain valid after logout (no server-side revocation)

### Recommendation
1. Enforce algorithm allowlisting on the server side (reject unexpected algorithms)
2. Use asymmetric algorithms (RS256/ES256) with proper key management
3. Implement token revocation via a blocklist or short expiration with refresh tokens
4. Validate all JWT claims server-side (iss, aud, exp, nbf)
5. Use a minimum key length of 256 bits for HMAC secrets
```
