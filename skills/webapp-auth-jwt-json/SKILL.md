---
name: webapp-auth-jwt-json
description: - When testing applications using JWT for authentication and session management - During API security assessments where JWTs are used for authorization - When evaluating OAuth 2.0 or OpenID Connect implementations using JWT - During penetration testing of single sign-on (SSO) systems - When auditing JWT library configurations for known vulnerabilit
domain: cybersecurity
---
------|-------------|
| Algorithm Confusion | Switching from asymmetric (RS256) to symmetric (HS256) using public key as secret |
| None Algorithm | Setting alg to "none" to create unsigned tokens accepted by misconfigured servers |
| Kid Injection | Exploiting the Key ID header parameter for SQLi, path traversal, or SSRF |
| JKU/X5U Injection | Pointing key source URLs to attacker-controlled servers for key substitution |
| Weak Secret | HMAC secrets that can be brute-forced using dictionary attacks |
| Claim Tampering | Modifying payload claims (role, sub, admin) after bypassing signature verification |
| Token Replay | Reusing valid JWTs after the intended session should have expired |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| jwt_tool | Comprehensive JWT testing and exploitation toolkit |
| JWT Editor (Burp) | Burp Suite extension for JWT manipulation and attack automation |
| hashcat | GPU-accelerated JWT secret brute-forcing (mode 16500) |
| john the ripper | CPU-based JWT secret cracking |
| jwt.io | Online JWT decoder and debugger for inspection |
| PyJWT | Python library for programmatic JWT creation and verification |

## Common Scenarios

1. **None Algorithm Bypass** — Change JWT algorithm to "none", remove signature, and forge admin tokens on servers that accept unsigned JWTs
2. **Algorithm Confusion RCE** — Switch RS256 to HS256 using leaked public key to forge arbitrary tokens for administrative access
3. **Kid SQL Injection** — Inject SQL payload in kid parameter to extract the signing key from the database
4. **Weak Secret Cracking** — Brute-force HMAC-SHA256 secrets using hashcat to forge arbitrary JWTs for any user
5. **JKU Server Spoofing** — Point JKU header to attacker-controlled JWKS endpoint to sign tokens with attacker's private key

## Output Format

```
## JWT Security Assessment Report
- **Target**: http://target.com
- **JWT Algorithm**: RS256 (claimed)
- **JWKS Endpoint**: http://target.com/.well-known/jwks.json

### Findings
| # | Vulnerability | Technique | Impact | Severity |
|---|--------------|-----------|--------|----------|
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