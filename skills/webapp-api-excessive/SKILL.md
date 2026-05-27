---
name: webapp-api-excessive
description: - Testing APIs where the frontend displays a subset of data but the API response includes additional fields - Assessing mobile application APIs where responses are designed for multiple client types and may contain excess data - Identifying PII leakage in API responses that include email addresses, phone numbers, SSNs, or payment data not shown in 
domain: cybersecurity
---
---|------------|
| **Excessive Data Exposure** | API returns more data fields than the client needs, relying on frontend filtering to hide sensitive information from users |
| **Over-Fetching** | Requesting or receiving more data than needed for a specific operation, common in REST APIs that return fixed response schemas |
| **Response Filtering** | Client-side filtering of API response data to display only relevant fields, which provides zero security since the full response is interceptable |
| **Object Property Level Authorization** | OWASP API3:2023 - ensuring that users can only read/write object properties they are authorized to access |
| **PII Leakage** | Unintended exposure of Personally Identifiable Information in API responses including names, emails, addresses, SSNs, or financial data |
| **Schema Validation** | Enforcing that API responses conform to a defined schema, stripping unauthorized fields before transmission |

## Tools & Systems

- **Burp Suite Professional**: Intercept API responses and use the Comparer tool to diff expected vs actual response schemas
- **mitmproxy**: Scriptable proxy for automated response analysis with Python-based content inspection scripts
- **OWASP ZAP**: Passive scanner detects information disclosure in headers, error messages, and response bodies
- **Postman**: Compare documented response schemas against actual API responses using test scripts
- **jq**: Command-line JSON processor for extracting and analyzing specific fields from API responses

## Common Scenarios

### Scenario: Mobile Banking API Data Exposure Assessment

**Context**: A mobile banking application's API returns full account objects to the mobile client, which only displays account nickname and balance. The API is accessed by both iOS and Android apps and a web portal.

**Approach**:
1. Configure mitmproxy on a test device and authenticate as the test user
2. Capture all API responses during a complete user session (login, view accounts, transfer, logout)
3. Analyze `GET /api/v1/accounts` response: UI shows 4 fields but API returns 23 fields
4. Discover that the API returns `routing_number`, `account_holder_ssn_last4`, `internal_risk_score`, `kyc_verification_status`, and `linked_external_accounts` - none shown in UI
5. Analyze `GET /api/v1/transactions` response: API returns `merchant_id`, `terminal_id`, `authorization_code`, `processor_response` fields not needed by the client
6. Check `GET /api/v1/users/me`: API returns `last_login_ip`, `mfa_backup_codes_remaining`, `account_officer_name`, and `credit_score_band`
7. Test error responses: `POST /api/v1/transfers` with invalid payload returns SQL table name in error message

**Pitfalls**:
- Only checking top-level fields and missing sensitive data in deeply nested objects
- Not testing paginated responses where subsequent pages may include different fields
- Ignoring response headers that may leak server version, backend technology, or internal routing information
- Missing data exposure in error responses which often contain stack traces, SQL queries, or internal paths
- Assuming that HTTPS encryption prevents data exposure (it protects in transit, not from the authenticated client)

## Output Format

```
## Finding: Excessive Data Exposure in Account and Transaction APIs

**ID**: API-DATA-001
**Severity**: High (CVSS 7.1)
**OWASP API**: API3:2023 - Broken Object Property Level Authorization
**Affected Endpoints**:
  - GET /api/v1/accounts
  - GET /api/v1/transactions
  - GET /api/v1/users/me

**Description**:
The API returns full database objects to the client, including sensitive fields
that are not displayed in the mobile application UI. The mobile app filters
these fields client-side, but they are fully accessible by intercepting the
API response. This exposes SSN fragments, internal risk scores, and KYC
verification data for any authenticated user.

**Excess Fields Discovered**:
- /accounts: routing_number, account_holder_ssn_last4, internal_risk_score,
  kyc_verification_status, linked_external_accounts (18 excess fields total)
- /transactions: merchant_id, terminal_id, authorization_code,
  processor_response (12 excess fields total)
- /users/me: last_login_ip, mfa_backup_codes_remaining, credit_score_band

**Impact**:
An authenticated user can extract sensitive financial data, internal risk
assessments, and PII for their own account that the application is not
intended to reveal. Combined with BOLA vulnerabilities, this data could
be extracted for all users.

**Remediation**:
1. Implement server-side response filtering using DTOs/view models that only include fields needed by the client
2. Use GraphQL field-level authorization or REST response schemas per endpoint per role
3. Remove sensitive fields from API responses at the serialization layer
4. Implement response schema validation in the API gateway to strip undocumented fields
5. Add automated tests that verify response schemas match documentation
```