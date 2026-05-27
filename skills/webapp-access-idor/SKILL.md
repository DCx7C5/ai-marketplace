---
name: webapp-access-idor
description: "Webapp Access Idor."
domain: cybersecurity
---

--|
| /api/v1/users/{id}/profile | GET | Read PII of any user |
| /api/v1/users/{id}/orders | GET | Read order history of any user |
| /api/v1/users/{id}/profile | PUT | Modify profile of any user |
| /api/v1/invoices/{id}/download | GET | Download any user's invoices |

### Impact
- 15,000+ user profiles accessible (enumerated IDs 1-15247)
- Exposed fields: name, email, phone, address, date_of_birth
- Write IDOR allows profile modification of other users
- Violates GDPR data access controls

### Recommendation
1. Implement object-level authorization: verify the requesting user owns or has permission to access the requested object
2. Use non-enumerable identifiers (UUIDv4) as a defense-in-depth measure
3. Log and alert on sequential ID enumeration patterns
4. Implement rate limiting on resource endpoints
```
