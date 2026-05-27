---
name: webapp-api-massassign
description: - Testing API endpoints that accept JSON/XML request bodies for user profile updates, registration, or object creation - Assessing whether the API binds all client-supplied properties to the data model without an allowlist - Evaluating if users can set privileged attributes (role, permissions, pricing, balance) through regular update endpoints - Te
domain: cybersecurity
---
---|------------|
| **Mass Assignment** | Vulnerability where an API automatically binds client-supplied parameters to internal object properties without filtering, allowing modification of unintended fields |
| **Auto-Binding** | Framework feature that maps HTTP request parameters directly to object model attributes, enabling mass assignment when no allowlist is configured |
| **Allowlist (Whitelist)** | Server-side list of fields that the API explicitly allows clients to set, rejecting all other parameters |
| **Blocklist (Blacklist)** | Server-side list of fields that the API explicitly blocks from client modification (less secure than allowlist) |
| **Object Property Level Authorization** | OWASP API3:2023 - ensuring that users can only read/write object properties they are authorized to access |
| **DTO (Data Transfer Object)** | Pattern where a separate object defines the allowed input fields, decoupling the API contract from the internal data model |

## Tools & Systems

- **Burp Suite Professional**: Intercept write requests and inject additional parameters using Repeater and Intruder
- **Param Miner (Burp Extension)**: Automatically discovers hidden parameters by fuzzing request bodies and headers
- **Arjun**: Parameter discovery tool that finds hidden HTTP parameters in API endpoints
- **OWASP ZAP**: Active scanner with parameter injection capabilities for mass assignment detection
- **Postman**: API testing platform for crafting requests with injected parameters and verifying responses

## Common Scenarios

### Scenario: SaaS User Registration Mass Assignment

**Context**: A SaaS platform allows user self-registration through a REST API. The registration endpoint accepts name, email, and password. The backend uses an ORM that auto-binds request parameters to the User model.

**Approach**:
1. Register a new user with only expected fields: `POST /api/v1/register {"name":"Test","email":"test@example.com","password":"Pass123!"}` - returns user with `role: "user"`
2. Register another user with injected role: `POST /api/v1/register {"name":"Admin","email":"admin@example.com","password":"Pass123!","role":"admin"}` - returns user with `role: "admin"`
3. Confirm admin access by calling admin endpoints with the new account
4. Test additional fields: `is_verified: true` bypasses email verification, `subscription_plan: "enterprise"` grants premium features
5. Test profile update endpoint: `PUT /api/v1/users/me {"name":"Test","balance":99999}` - wallet balance modified

**Pitfalls**:
- Only testing obvious fields like "role" and missing domain-specific fields like "subscription_plan", "credit_limit", or "verified"
- Not verifying that the injected field was actually saved (some APIs return 200 but silently ignore unknown fields)
- Assuming that blocklisting "role" prevents mass assignment when "isAdmin", "is_admin", or "admin" may also work
- Not testing both creation (POST) and update (PUT/PATCH) endpoints as they may have different filtering
- Missing nested object mass assignment where fields like `user.role` or `address.verified` can be injected

## Output Format

```
## Finding: Mass Assignment Enables Role Elevation via Registration API

**ID**: API-MASS-001
**Severity**: Critical (CVSS 9.8)
**OWASP API**: API3:2023 - Broken Object Property Level Authorization
**Affected Endpoints**:
  - POST /api/v1/register
  - PUT /api/v1/users/me
  - POST /api/v1/orders

**Description**:
The API binds all client-supplied JSON fields directly to the database model
without filtering. An attacker can include undocumented fields in registration
and update requests to elevate their role to admin, bypass email verification,
modify wallet balances, and manipulate order pricing.

**Proof of Concept**:
1. Register with injected role:
   POST /api/v1/register
   {"name":"Attacker","email":"attacker@evil.com","password":"P@ss123!","role":"admin"}
   Response: {"id":5001,"name":"Attacker","role":"admin","is_verified":false}

2. Update profile with injected balance:
   PUT /api/v1/users/me
   {"name":"Attacker","balance":99999.99}
   Response: {"id":5001,"balance":99999.99}

3. Create order with manipulated price:
   POST /api/v1/orders
   {"items":[{"product_id":42,"qty":1}],"total":0.01}
   Response: {"order_id":8001,"total":0.01}

**Impact**:
Any user can gain administrative access, manipulate financial data,
bypass security controls, and purchase products at arbitrary prices.

**Remediation**:
1. Implement DTOs/input schemas that explicitly define allowed fields per endpoint per role
2. Use framework-specific mass assignment protection (Rails: strong parameters, Django: serializer fields)
3. Never bind request parameters directly to the data model
4. Add integration tests that verify undocumented fields are rejected
5. Use an allowlist approach rather than blocklist for writable fields
```