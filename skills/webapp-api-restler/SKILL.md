---
name: webapp-api-restler
description: "-| | 500 Internal Server Error | 12 | High | | Use After Free | 3 | Critical | | Namespace Rule Violation | 5 | Critical | | Information Leakage | 8 | Medium | | Resource Leak | 4 | Low |  ### Critical Findings  **1."
domain: cybersecurity
---

-|
| 500 Internal Server Error | 12 | High |
| Use After Free | 3 | Critical |
| Namespace Rule Violation | 5 | Critical |
| Information Leakage | 8 | Medium |
| Resource Leak | 4 | Low |

### Critical Findings

**1. Use-After-Free: Deleted user token still valid**
- Sequence: POST /users -> DELETE /users/{id} -> GET /users/{id}
- After deleting user, GET with the deleted user's token returns 200
- Impact: Deleted accounts can still access the API

**2. Namespace Violation: Cross-tenant data access**
- Sequence: POST /users (tenant A) -> GET /users/{id} (tenant B token)
- User created by tenant A is accessible with tenant B's credentials
- Impact: Multi-tenant isolation breach

**3. 500 Error: Unhandled integer overflow**
- Request: POST /orders {"quantity": 2147483648}
- Response: 500 Internal Server Error with stack trace
- Impact: DoS potential, information disclosure via stack trace

### Coverage

- Endpoints covered: 38/42 (90.5%)
- Uncovered: POST /admin/migrate, DELETE /admin/cache,
  PUT /config/advanced, POST /webhooks/test
```
