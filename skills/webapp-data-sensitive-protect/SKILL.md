---
name: webapp-data-sensitive-protect
description: - During authorized penetration tests when assessing data protection controls - When evaluating applications for GDPR, PCI DSS, HIPAA, or other data protection compliance - For identifying leaked API keys, credentials, tokens, and secrets in application responses - When testing whether sensitive data is properly encrypted in transit and at rest - D
domain: cybersecurity
---
------|-------------|
| **Sensitive Data Exposure** | Unintended disclosure of PII, credentials, financial data, or health records |
| **Data Over-Exposure** | API returning more data fields than the client needs |
| **Secret Leakage** | API keys, tokens, or credentials exposed in client-side code or logs |
| **Data at Rest** | Sensitive data stored in databases, files, or backups without encryption |
| **Data in Transit** | Sensitive data transmitted over network without TLS encryption |
| **Data Masking** | Replacing sensitive data with redacted values (e.g., showing last 4 digits of credit card) |
| **PII** | Personally Identifiable Information - data that can identify an individual |
| **Information Leakage** | Excessive error messages, stack traces, or debug information in responses |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Response analysis and regex-based sensitive data scanning |
| **trufflehog** | Secret detection across git repos, filesystems, and cloud storage |
| **gitleaks** | Git repository scanning for hardcoded secrets |
| **testssl.sh** | TLS/SSL configuration assessment |
| **git-dumper** | Downloading exposed .git directories from web servers |
| **SecretFinder** | JavaScript file analysis for exposed API keys and tokens |
| **Retire.js** | Detecting JavaScript libraries with known vulnerabilities |

## Common Scenarios

### Scenario 1: API Key in JavaScript Bundle
The application's JavaScript bundle contains a hardcoded Google Maps API key and a Stripe publishable key. The Stripe key has overly broad permissions, allowing the attacker to create charges.

### Scenario 2: User API Returns Password Hashes
The `/api/users` endpoint returns complete user objects including bcrypt password hashes. Attackers can extract hashes and attempt offline cracking.

### Scenario 3: PII in Cached API Responses
The user profile API endpoint returns full SSN and credit card numbers without masking. The endpoint does not set `Cache-Control: no-store`, so responses are cached in the browser and proxy caches.

### Scenario 4: Git Repository with Database Credentials
The `.git` directory is accessible on the production server. Using git-dumper, the attacker downloads the repository history, finding database credentials committed in an early commit that were later "removed" but remain in git history.

## Output Format

```
## Sensitive Data Exposure Assessment Report

**Target**: target.example.com
**Assessment Date**: 2024-01-15
**OWASP Category**: A02:2021 - Cryptographic Failures

### Findings Summary
| Finding | Severity | Data Type |
|---------|----------|-----------|
| API keys in JavaScript source | High | Credentials |
| Password hashes in API response | Critical | Authentication |
| Unmasked SSN in user profile | Critical | PII |
| Credit card number in export | High | Financial |
| .git directory exposed | Critical | Source code + secrets |
| Missing TLS on API endpoint | High | All data in transit |
| Sensitive data in error messages | Medium | Technical info |

### Critical: Exposed Secrets
| Secret Type | Location | Risk |
|-------------|----------|------|
| AWS Access Key (AKIA...) | /static/app.js line 342 | AWS resource access |
| Stripe Secret Key (sk_live_...) | .env (via .git exposure) | Payment processing |
| Database URL with credentials | .git history commit abc123 | Database access |
| JWT Signing Secret | config.json (via .git) | Token forgery |

### Data Over-Exposure in APIs
| Endpoint | Unnecessary Fields Returned |
|----------|-----------------------------|
| GET /api/users | password_hash, internal_id, created_ip |
| GET /api/users/{id} | ssn, credit_card_full, date_of_birth |
| GET /api/orders | customer_phone, customer_address |

### Recommendation
1. Remove all hardcoded secrets from client-side code; use backend proxies
2. Rotate all exposed credentials immediately
3. Remove .git directory from production web root
4. Implement response field filtering; return only required fields
5. Mask sensitive data (SSN, credit card) in all API responses
6. Add Cache-Control: no-store to all sensitive endpoints
7. Enable TLS 1.2+ on all endpoints; redirect HTTP to HTTPS
8. Implement secret scanning in CI/CD pipeline (trufflehog/gitleaks)
```