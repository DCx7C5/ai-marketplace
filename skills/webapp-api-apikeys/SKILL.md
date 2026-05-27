---
name: webapp-api-apikeys
description: - Designing secure API key generation with sufficient entropy and identifiable prefixes for leak detection - Implementing server-side API key hashing (never storing keys in plaintext) with SHA-256 or bcrypt - Building key rotation workflows that allow zero-downtime key replacement for API consumers - Configuring per-key scoping to limit each API ke
domain: cybersecurity
---
---|------------|
| **API Key** | A secret string used to authenticate API requests, typically passed in headers or query parameters |
| **Key Hashing** | Storing only the hash (SHA-256) of the API key in the database, never the plaintext key, similar to password hashing |
| **Key Rotation** | Replacing an API key with a new one while maintaining a grace period where both keys work, ensuring zero-downtime transition |
| **Key Scoping** | Limiting each API key to specific endpoints, HTTP methods, IP ranges, and rate limits to minimize blast radius |
| **Key Prefix** | An identifiable prefix (e.g., sk_live_) that enables automated detection of leaked keys in logs, code, and public repositories |
| **Secret Scanning** | Automated monitoring of repositories, logs, and public sources for exposed API keys and credentials |

## Tools & Systems

- **GitHub Secret Scanning**: Built-in GitHub feature that detects exposed secrets in repositories and alerts key providers
- **gitleaks**: Open-source tool for detecting secrets in git repositories using customizable regex patterns
- **truffleHog**: Secret scanning tool that searches entire git history for high-entropy strings and known secret patterns
- **HashiCorp Vault**: Enterprise secret management system for API key storage, rotation, and dynamic credential generation
- **AWS Secrets Manager**: Managed secret storage with automatic rotation support for API keys and credentials

## Common Scenarios

### Scenario: API Key Security Program for Developer Platform

**Context**: A developer platform provides public APIs authenticated with API keys. The platform has 10,000+ API consumers generating 50M+ requests per day. Keys are frequently leaked in public GitHub repositories.

**Approach**:
1. Implement prefixed API keys (sk_live_, sk_test_) with 256-bit entropy for leak detection
2. Store only SHA-256 hashes of keys in the database, cache validated keys in Redis
3. Implement per-key scoping: each key restricted to specific endpoints, rate limits, and optional IP allowlists
4. Build key rotation API with 24-hour grace period for seamless transitions
5. Integrate with GitHub Secret Scanning to automatically detect and revoke leaked keys within minutes
6. Run gitleaks in CI/CD pipelines to prevent key commits in first place
7. Implement anomaly detection: alert on keys used from unusual IPs or with abnormal traffic patterns
8. Add key expiration policy: all keys expire after 365 days with 30-day advance notification

**Pitfalls**:
- Storing API keys in plaintext in the database (use SHA-256 hashing)
- Using predictable or low-entropy key generation (use cryptographically secure random generators)
- Not implementing key prefixes, making it impossible to identify leaked keys in automated scans
- Allowing API keys in URL query parameters where they leak in logs, browser history, and Referer headers
- Not implementing rate limiting per key, allowing a single compromised key to abuse the entire API

## Output Format

```
## API Key Security Implementation Report

**Platform**: Developer API v3
**Total Active Keys**: 12,450
**Daily Key Validations**: 52M

### Security Controls

| Control | Implementation | Status |
|---------|---------------|--------|
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