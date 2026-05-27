---
name: webapp-protocol-api
description: - Testing API endpoints for authorization flaws, injection vulnerabilities, and business logic bypasses - Assessing the security of microservices architecture where APIs are the primary communication method - Validating that API gateway protections (rate limiting, authentication, input validation) are properly enforced - Testing third-party API int
domain: cybersecurity
---
---|------------|
| **BOLA** | Broken Object Level Authorization (OWASP API #1); failure to verify that the requesting user is authorized to access a specific object, enabling IDOR attacks |
| **BFLA** | Broken Function Level Authorization (OWASP API #5); failure to restrict administrative or privileged API functions from being accessed by lower-privilege users |
| **Mass Assignment** | A vulnerability where the API binds client-provided data to internal object properties without filtering, allowing attackers to modify fields they should not have access to |
| **GraphQL Introspection** | A built-in GraphQL feature that exposes the complete API schema including all types, fields, and relationships; should be disabled in production |
| **JWT** | JSON Web Token; a self-contained token format used for API authentication containing claims signed with a secret or key pair |
| **Rate Limiting** | Controls that restrict the number of API requests a client can make within a time window, preventing brute force, enumeration, and abuse |

## Tools & Systems

- **Burp Suite Professional**: HTTP proxy for intercepting, modifying, and replaying API requests with extensions like Autorize for automated authorization testing
- **Postman**: API development platform used for organizing endpoint collections, scripting tests, and comparing responses across authentication contexts
- **GraphQL Voyager**: Visual tool for exploring GraphQL schemas obtained through introspection queries
- **jwt.io / jwt_tool**: Tools for decoding, analyzing, and tampering with JWT tokens to test authentication bypasses
- **Nuclei**: Template-based scanner with API-specific templates for detecting common misconfigurations and known vulnerabilities

## Common Scenarios

### Scenario: API Security Assessment for a Fintech Mobile Application

**Context**: A fintech startup has a mobile banking application with a REST API backend. The API handles account management, fund transfers, bill payments, and transaction history. The tester has Swagger documentation and accounts at user and admin levels.

**Approach**:
1. Import Swagger spec into Postman, generating 87 endpoint collections across 12 controllers
2. Discover BOLA on `/api/v1/accounts/{accountId}/transactions` allowing any authenticated user to view any account's transaction history
3. Find mass assignment on the user update endpoint where adding `"dailyTransferLimit": 999999` bypasses the configured transfer limit
4. Identify that the fund transfer endpoint lacks rate limiting, allowing unlimited transfer attempts without throttling
5. Discover that JWT tokens have a 30-day expiration with no refresh token rotation, enabling long-lived session hijacking
6. Find that the admin endpoint `/api/v1/admin/users` is accessible with a standard user token (BFLA)
7. Report all findings with CVSS scores and specific API code-level remediation guidance

**Pitfalls**:
- Testing only the endpoints documented in Swagger and missing undocumented or deprecated API versions
- Not testing the same endpoint with tokens from every privilege level to detect authorization bypasses
- Ignoring response body analysis for excessive data exposure when the UI only shows a subset of returned fields
- Failing to test for mass assignment by only sending fields shown in the documentation

## Output Format

```
## Finding: Broken Object Level Authorization in Transaction History API

**ID**: API-001
**Severity**: Critical (CVSS 9.1)
**Affected Endpoint**: GET /api/v1/accounts/{accountId}/transactions
**OWASP API Category**: API1:2023 - Broken Object Level Authorization

**Description**:
The transaction history endpoint returns all transactions for the specified
account without verifying that the authenticated user owns the account. Any
authenticated user can view the complete transaction history of any account
by substituting the accountId path parameter.

**Proof of Concept**:
1. Authenticate as User A (account ID: ACC-10045)
2. Request: GET /api/v1/accounts/ACC-10046/transactions
   Authorization: Bearer <User_A_token>
3. Response: 200 OK with User B's full transaction history

**Impact**:
Any authenticated user can view the complete financial transaction history of
all 45,000 customer accounts, including amounts, dates, recipients, and
transaction descriptions.

**Remediation**:
Implement server-side authorization check that verifies the authenticated user
owns the requested account before returning data:
  const account = await Account.findById(accountId);
  if (account.userId !== req.user.id) return res.status(403).json({error: "Forbidden"});
```