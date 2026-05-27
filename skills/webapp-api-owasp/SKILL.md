---
name: webapp-api-owasp
description: - During authorized API penetration testing engagements - When assessing REST, GraphQL, or gRPC APIs for security vulnerabilities - Before deploying new API endpoints to production environments - When reviewing API security posture against the OWASP API Security Top 10 (2023) - For validating API gateway security controls and rate limiting effectiv
domain: cybersecurity
---
------|-------------|
| **BOLA (API1)** | Broken Object Level Authorization - accessing objects belonging to other users |
| **Broken Authentication (API2)** | Weak authentication mechanisms allowing credential stuffing or token manipulation |
| **BOPLA (API3)** | Broken Object Property Level Authorization - excessive data exposure or mass assignment |
| **Unrestricted Resource Consumption (API4)** | Missing rate limiting enabling DoS or brute-force attacks |
| **Broken Function Level Auth (API5)** | Regular users accessing admin-level API functions |
| **SSRF (API7)** | Server-Side Request Forgery through API parameters accepting URLs |
| **Security Misconfiguration (API8)** | Missing security headers, verbose errors, permissive CORS |
| **Improper Inventory (API9)** | Undocumented, deprecated, or shadow API endpoints left exposed |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | API interception, scanning, and manual testing |
| **Postman** | API collection management and automated test execution |
| **ffuf** | API endpoint and parameter fuzzing |
| **Kiterunner** | API endpoint discovery using common API path patterns |
| **jwt_tool** | JWT token analysis, manipulation, and attack automation |
| **GraphQL Voyager** | GraphQL schema visualization and introspection analysis |
| **Arjun** | HTTP parameter discovery for API endpoints |

## Common Scenarios

### Scenario 1: BOLA in E-commerce API
User A can access User B's order details by changing the order ID in `/api/v1/orders/{id}`. The API only checks authentication but not authorization on the object level.

### Scenario 2: Mass Assignment on User Profile
The user update endpoint accepts a `role` field in the JSON body. By adding `"role":"admin"` to a profile update request, a regular user escalates to administrator privileges.

### Scenario 3: Deprecated API Version Bypass
The `/api/v2/users` endpoint has proper rate limiting, but `/api/v1/users` (still active) has no rate limiting. Attackers use the old version to brute-force credentials.

### Scenario 4: GraphQL Introspection Data Leak
GraphQL introspection is enabled in production, exposing the entire schema including internal queries, mutations, and sensitive field names that are not used in the frontend.

## Output Format

```
## API Security Assessment Report

**Target**: api.target.example.com
**API Type**: REST (OpenAPI 3.0)
**Assessment Date**: 2024-01-15
**OWASP API Security Top 10 (2023) Coverage**

| Risk | Status | Severity | Details |
|------|--------|----------|---------|
| API1: BOLA | VULNERABLE | Critical | /api/v1/orders/{id} - IDOR confirmed |
| API2: Broken Auth | VULNERABLE | High | No rate limit on /auth/login |
| API3: BOPLA | VULNERABLE | High | User role modifiable via mass assignment |
| API4: Resource Consumption | VULNERABLE | Medium | No pagination limit enforced |
| API5: Function Level Auth | PASS | - | Admin endpoints properly restricted |
| API6: Unrestricted Sensitive Flows | VULNERABLE | Medium | OTP endpoint lacks rate limiting |
| API7: SSRF | PASS | - | URL parameters properly validated |
| API8: Misconfiguration | VULNERABLE | Medium | Verbose stack traces in error responses |
| API9: Improper Inventory | VULNERABLE | Low | API v1 still accessible without docs |
| API10: Unsafe Consumption | NOT TESTED | - | No third-party API integrations found |

### Critical Finding: BOLA on Orders API
Authenticated users can access any order by iterating order IDs.
Tested range: 1-1000, 847 valid orders accessible.
PII exposure: names, addresses, payment details.
```