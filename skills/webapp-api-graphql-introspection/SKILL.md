---
name: webapp-api-graphql-introspection
description: "Webapp Api Graphql Introspection."
domain: cybersecurity
---

|
| **GraphQL Introspection** | Built-in capability to query the schema definition, exposing all types, fields, queries, mutations, and subscriptions available in the API |
| **Query Depth Attack** | Sending deeply nested queries that cause exponential resolver execution, consuming server resources and potentially causing DoS |
| **Alias-Based Batching** | Using GraphQL aliases to execute multiple operations in a single request, bypassing per-request rate limiting |
| **Schema Reconstruction** | Reconstructing the GraphQL schema when introspection is disabled by analyzing error messages and field suggestions |
| **Field-Level Authorization** | Controlling access to individual fields within a GraphQL type based on the authenticated user's role or permissions |
| **Query Complexity Analysis** | Calculating the computational cost of a GraphQL query before execution to enforce resource limits |

## Tools & Systems

- **InQL (Burp Suite Extension)**: Automated GraphQL introspection, schema analysis, and attack generation with support for schema brute-forcing
- **Clairvoyance**: Schema reconstruction tool that works even when introspection is disabled, using error-based field discovery
- **GraphQL Voyager**: Visual schema explorer that generates interactive diagrams from introspection results
- **Altair GraphQL Client**: Feature-rich GraphQL IDE for crafting and testing queries with authentication support
- **graphql-cop**: GraphQL security auditor that tests for common misconfigurations including introspection, field suggestions, and query limits

## Common Scenarios

### Scenario: E-Commerce GraphQL API Security Assessment

**Context**: An e-commerce platform migrated from REST to GraphQL. The GraphQL endpoint serves the web and mobile frontends. Introspection was left enabled during development and was not disabled for production.

**Approach**:
1. Run full introspection query against `/graphql` endpoint - complete schema extracted with 45 types, 120 queries, and 38 mutations
2. Identify sensitive types: `AdminUser`, `PaymentInfo`, `InternalConfig`, `AuditLog`
3. Discover that `User` type exposes `passwordHash`, `mfaSecret`, and `lastLoginIp` fields
4. Find admin mutations accessible to regular users: `deleteUser`, `updateRole`, `exportAllOrders`
5. Test query depth: no limit enforced, nested query 50 levels deep executes successfully and takes 45 seconds
6. Test alias batching: 1000 login attempts in a single request bypass rate limiting
7. Test batch queries: array of 500 queries accepted without limit
8. Schema reveals internal `InternalConfig` type with `databaseConnectionString` and `stripeSecretKey` fields

**Pitfalls**:
- Assuming introspection is the only way to discover the schema (error messages and field suggestions reveal information even when introspection is disabled)
- Not testing mutations which often have weaker authorization than queries
- Missing subscription endpoints that may expose real-time data streams without authentication
- Not testing query complexity limits with realistic payloads that trigger expensive database operations
- Ignoring that GraphQL over WebSocket (subscriptions) may have different authentication requirements

## Output Format

```
## Finding: GraphQL Introspection Enabled with Sensitive Schema Exposure

**ID**: API-GQL-001
**Severity**: High (CVSS 7.5)
**Affected Endpoint**: POST /graphql
**Tools Used**: InQL, Clairvoyance, custom Python scripts

**Description**:
The GraphQL endpoint has introspection enabled in production, exposing
the complete API schema including 45 types, 120 queries, and 38 mutations.
The schema reveals sensitive internal types (AdminUser, PaymentInfo,
InternalConfig) and exposes fields containing password hashes, MFA secrets,
and database connection strings. No query depth or complexity limits are
enforced, enabling denial-of-service through nested queries.

**Schema Highlights**:
- User.passwordHash: bcrypt hash exposed
- User.mfaSecret: TOTP secret exposed (allows MFA bypass)
- InternalConfig.databaseConnectionString: Production DB credentials
- InternalConfig.stripeSecretKey: Payment processing API key
- 12 admin mutations accessible to regular users

**Impact**:
An attacker can extract the complete API schema, identify sensitive
fields, access password hashes and MFA secrets for any user, retrieve
production database credentials, and execute admin-only mutations.

**Remediation**:
1. Disable introspection in production: set introspection to false in the GraphQL server config
2. Implement field-level authorization using GraphQL directives (@auth, @hasRole)
3. Remove sensitive fields from the schema or restrict them with authorization middleware
4. Implement query depth limiting (max 10 levels) and complexity scoring
5. Disable field suggestions in error messages to prevent schema reconstruction
6. Rate limit GraphQL requests per query, not just per HTTP request
```
