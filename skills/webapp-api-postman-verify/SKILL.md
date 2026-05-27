---
name: webapp-api-postman-verify
description: "Webapp Api Postman Verify."
domain: cybersecurity
---

-|
| 1 | GET /users/1002 | BOLA: Cannot access other user profile | Critical |
| 2 | GET /orders/5003 | BOLA: Cannot access other user order | Critical |
| 3 | GET /admin/users | BFLA: Regular user cannot access admin endpoint | Critical |
| 4 | PUT /users/me | Mass Assignment: Role field not accepted | High |
| 5 | GET /users/me | Data Exposure: No sensitive fields in response | High |
| 6 | POST /auth/login | Auth: No account enumeration | Medium |
| ... | ... | ... | ... |

### Recommendations
1. Fix BOLA on /users/{id} and /orders/{id} - add object-level authorization checks
2. Fix BFLA on /admin/users - enforce role-based access control middleware
3. Fix mass assignment on PUT /users/me - implement field allowlist
4. Remove password_hash and mfa_secret from user serialization
5. Standardize login error messages to prevent account enumeration
```
