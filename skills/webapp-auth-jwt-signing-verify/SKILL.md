---
name: webapp-auth-jwt-signing-verify
description: "Webapp Auth Jwt Signing Verify."
domain: cybersecurity
---

|
| HS256 | Symmetric (HMAC) | Shared secret | 128-bit |
| RS256 | Asymmetric (RSA) | RSA key pair | 112-bit |
| ES256 | Asymmetric (ECDSA) | P-256 key pair | 128-bit |
| EdDSA | Asymmetric (Ed25519) | Ed25519 pair | 128-bit |

### Common JWT Attacks

- **Algorithm confusion**: Switching from RS256 to HS256, using public key as HMAC secret
- **None algorithm**: Setting alg=none to bypass signature verification
- **Key injection**: Embedding key in JWK header
- **Weak secrets**: Brute-forcing short HMAC secrets
- **Token replay**: Reusing valid tokens without expiration

## Security Considerations

- Always validate the algorithm header against an allowlist
- Never accept alg=none in production
- Use asymmetric algorithms (RS256, ES256) for distributed systems
- Set short expiration times (15 min for access tokens)
- Implement token refresh mechanism
- Store secrets securely (not in source code)

## Validation Criteria

- [ ] JWT signing produces valid tokens for all algorithms
- [ ] Signature verification rejects tampered tokens
- [ ] Expired tokens are rejected
- [ ] Algorithm confusion attack is prevented
- [ ] None algorithm is rejected
- [ ] JWK key rotation works correctly
- [ ] Claims validation enforces all required claims
