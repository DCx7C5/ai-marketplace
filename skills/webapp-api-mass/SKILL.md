---
name: webapp-api-mass
description: - When testing REST APIs that accept JSON input for creating or updating resources - During API security assessments of applications using ORM frameworks (Rails, Django, Laravel, Spring) - When testing user registration, profile update, or account management endpoints - During bug bounty hunting on applications with CRUD API operations - When evalu
domain: cybersecurity
---
------|-------------|
| Mass Assignment | ORM auto-binding of request parameters to model attributes without restriction |
| Autobinding | Framework feature that maps HTTP parameters directly to object properties |
| Allowlist | Server-side list of permitted fields for update operations (strong_parameters in Rails) |
| Denylist | List of forbidden fields (less secure than allowlist approach) |
| Hidden Fields | Server-managed fields (role, balance) not shown in forms but accepted by API |
| DTO (Data Transfer Object) | Pattern using separate objects for input vs. database to prevent mass assignment |
| Parameter Pollution | Sending unexpected extra parameters alongside legitimate ones |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | API request interception and parameter injection |
| Postman | API testing and collection-based mass assignment testing |
| Arjun | Hidden parameter discovery tool for API endpoints |
| param-miner | Burp extension for discovering hidden parameters |
| OWASP ZAP | Automated API scanning with parameter injection |
| swagger-codegen | Generate API clients from OpenAPI specs for testing |

## Common Scenarios

1. **Admin Privilege Escalation** — Inject `"role":"admin"` or `"isAdmin":true` in profile update to gain administrative access
2. **Price Manipulation** — Modify `price` or `discount` fields in order creation endpoints to purchase items at reduced cost
3. **Email Verification Bypass** — Set `email_verified:true` during registration or profile update to bypass verification requirements
4. **Account Takeover** — Modify `email` or `phone` fields to attacker-controlled values, then trigger password reset
5. **Subscription Upgrade** — Inject `plan:"enterprise"` in subscription update to gain premium features without payment

## Output Format

```
## Mass Assignment Vulnerability Report
- **Target**: http://target.com/api/users/me
- **Method**: PATCH
- **Framework**: Ruby on Rails (detected via X-Powered-By)

### Findings
| # | Endpoint | Injected Field | Original | Modified | Impact |
|---|----------|---------------|----------|----------|--------|
| 1 | PATCH /api/users/me | role | "user" | "admin" | Privilege Escalation |
| 2 | POST /api/orders | price | 99.99 | 0.01 | Financial Loss |
| 3 | PATCH /api/users/me | email_verified | false | true | Verification Bypass |

### Remediation
- Implement allowlist (strong_parameters) for all model update operations
- Use DTOs/ViewModels to decouple API input from database models
- Apply field-level authorization checks on sensitive attributes
- Log and alert on attempts to modify restricted fields
```