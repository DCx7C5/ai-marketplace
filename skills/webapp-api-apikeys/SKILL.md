---
name: webapp-api-apikeys
description: "Webapp Api Apikeys."
domain: cybersecurity
---

--|
| Key Entropy | 256-bit (secrets.token_urlsafe(32)) | Implemented |
| Key Format | sk_live_/sk_test_ prefixed | Implemented |
| Storage | SHA-256 hashed, Redis cached | Implemented |
| Scoping | Per-key endpoint/IP/rate limits | Implemented |
| Rotation | 24-hour grace period API | Implemented |
| Expiration | 365-day max TTL | Implemented |
| Leak Detection | GitHub Secret Scanning + gitleaks | Active |
| Auto-Revocation | Leaked keys revoked within 5 min | Active |

### Key Leakage Stats (Last 30 Days)
- Keys detected in public repos: 23
- Average time to revocation: 3.2 minutes
- Keys detected in CI/CD pre-commit: 7 (prevented)
```
