---
name: webapp-api-postman-verify
description: - Building repeatable API security test suites for OWASP API Security Top 10 coverage - Creating automated security regression tests that run in CI/CD pipelines via Newman - Testing API authentication and authorization across multiple user roles systematically - Integrating Postman with OWASP ZAP proxy for combined manual and automated security tes
domain: cybersecurity
---
---|------------|
| **Postman Collection** | Organized group of API requests with test scripts that can be shared, version-controlled, and executed automatically |
| **Newman** | Command-line companion for Postman that enables running collections in CI/CD pipelines and generating test reports |
| **Pre-request Script** | JavaScript code that executes before a Postman request, used for dynamic authentication and test data setup |
| **Test Script** | JavaScript code that executes after a Postman response, used to validate security assertions against the response |
| **Collection Runner** | Postman feature that executes all requests in a collection sequentially with configurable iterations and delays |
| **Environment Variables** | Key-value pairs scoped to a Postman environment that parameterize requests for different targets, roles, and configurations |

## Tools & Systems

- **Postman**: API platform for building, testing, and documenting APIs with built-in scripting and collection management
- **Newman**: CLI runner for Postman collections supporting multiple reporters (HTML, JUnit, JSON) for CI/CD integration
- **OWASP ZAP**: Open-source security proxy that can be configured as Postman's proxy to scan all requests passively
- **newman-reporter-htmlextra**: Enhanced HTML reporter for Newman that generates detailed test reports with request/response data
- **Postman Flows**: Visual workflow builder for chaining complex security test sequences with conditional logic

## Common Scenarios

### Scenario: API Security Regression Suite for CI/CD

**Context**: A development team releases API updates bi-weekly. They need an automated security test suite that runs on every pull request to catch authorization and authentication regressions before merge.

**Approach**:
1. Import the OpenAPI spec into Postman to generate a base collection with all endpoints
2. Create three environments: unauthenticated, regular user, admin with appropriate credentials
3. Add security test scripts to each request: BOLA checks, auth validation, data exposure scanning, header security
4. Create a dedicated "Security Tests" folder with injection payloads, mass assignment tests, and rate limit checks
5. Export the collection and environments to the repository
6. Configure Newman in GitHub Actions to run on every PR affecting API code
7. Set the pipeline to fail on any security test failure, blocking the merge

**Pitfalls**:
- Hardcoding authentication tokens in collections instead of using pre-request scripts for dynamic token generation
- Not testing with all user roles - only testing authenticated vs unauthenticated misses role-based authorization issues
- Running security tests against production instead of staging environments
- Not updating the collection when new endpoints are added, leaving gaps in coverage
- Ignoring Newman exit codes in CI/CD, allowing failing security tests to pass silently

## Output Format

```
## API Security Test Report - Postman/Newman

**Collection**: API Security Tests v2.3
**Environment**: Staging - Regular User
**Date**: 2024-12-15
**Total Requests**: 85
**Total Tests**: 234
**Passed**: 219
**Failed**: 15

### Failed Tests Summary

| # | Request | Test Name | Severity |
|---|---------|-----------|----------|
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