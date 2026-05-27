---
name: webapp-auth-jwt-json
description: "-|"
domain: cybersecurity
---
-|
| 1 | None algorithm accepted | alg: "none" | Auth bypass | Critical |
| 2 | Algorithm confusion | RS256 -> HS256 | Token forgery | Critical |
| 3 | Weak HMAC secret | Brute-force: "secret123" | Full token forgery | Critical |
| 4 | Kid path traversal | kid: "../../dev/null" | Sign with empty key | High |

### Remediation
- Enforce algorithm whitelist in JWT verification (reject "none")
- Use asymmetric algorithms (RS256/ES256) with proper key management
- Implement strong, random secrets for HMAC algorithms (256+ bits)
- Validate kid parameter against a strict allowlist
- Ignore jku/x5u headers or validate against known endpoints
- Set appropriate token expiration (exp) and implement token revocation
```
