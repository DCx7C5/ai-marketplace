---
name: webapp-auth-jwt-tokensec
description: - During authorized penetration tests when the application uses JWT for authentication or authorization - When assessing API security where JWTs are passed as Bearer tokens or in cookies - For evaluating SSO implementations that use JWT/JWS/JWE tokens - When testing OAuth 2.0 or OpenID Connect flows that issue JWTs - During security audits of micro
domain: cybersecurity
---
------|-------------|
| **Algorithm None Attack** | Removing signature verification by setting `alg` to `none` |
| **Algorithm Confusion** | Switching from RS256 to HS256 and signing with the public key as HMAC secret |
| **HMAC Brute Force** | Cracking weak HS256 signing secrets using wordlists or brute force |
| **JKU/x5u Injection** | Pointing JWT header URLs to attacker-controlled key servers |
| **KID Injection** | Exploiting SQL injection or path traversal in the Key ID header parameter |
| **Claim Tampering** | Modifying payload claims (role, sub, permissions) after compromising the signing key |
| **Token Revocation** | The ability (or inability) to invalidate tokens before their expiration |
| **JWE vs JWS** | JSON Web Encryption (confidentiality) vs JSON Web Signature (integrity) |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **jwt_tool** | Comprehensive JWT testing toolkit with automated attack modules |
| **Burp JWT Editor** | Burp Suite extension for real-time JWT manipulation |
| **Hashcat** | GPU-accelerated HMAC secret brute-forcing (mode 16500) |
| **John the Ripper** | CPU-based JWT secret cracking |
| **PyJWT** | Python library for programmatic JWT creation and manipulation |
| **jwt.io** | Online JWT decoder for quick analysis (do not paste production tokens) |

## Common Scenarios

### Scenario 1: Algorithm None Bypass
The JWT library accepts `"alg":"none"` tokens, allowing any user to forge admin tokens by simply removing the signature and changing the algorithm header.

### Scenario 2: Weak HMAC Secret
The application uses HS256 with a dictionary word as the signing secret. Hashcat cracks the secret in minutes, enabling complete token forgery and admin impersonation.

### Scenario 3: Algorithm Confusion on SSO
An SSO provider uses RS256 but the consumer application also accepts HS256. The attacker signs a forged token with the publicly available RSA public key using HS256.

### Scenario 4: KID SQL Injection
The `kid` header parameter is used in a SQL query to look up signing keys. Injecting `' UNION SELECT 'attacker_secret' --` allows the attacker to control the signing key.

## Output Format

```
## JWT Security Finding

**Vulnerability**: JWT Algorithm Confusion (RS256 to HS256)
**Severity**: Critical (CVSS 9.8)
**Location**: Authorization header across all API endpoints
**OWASP Category**: A02:2021 - Cryptographic Failures

### JWT Configuration
| Property | Value |
|----------|-------|
| Algorithm | RS256 (also accepts HS256) |
| Issuer | auth.target.example.com |
| Expiration | 24 hours |
| Public Key | Available at /.well-known/jwks.json |
| Revocation | Not implemented |

### Attacks Confirmed
| Attack | Result |
|--------|--------|
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