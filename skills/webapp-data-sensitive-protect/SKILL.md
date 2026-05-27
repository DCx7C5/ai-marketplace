---
name: webapp-data-sensitive-protect
description: "--| | GET /api/users | password_hash, internal_id, created_ip | | GET /api/users/{id} | ssn, credit_card_full, date_of_birth | | GET /api/orders | customer_phone, customer_address |  ### Recommendation 1."
domain: cybersecurity
---

--|
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
