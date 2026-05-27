---
name: webapp-api-graphql-assessment
description: - During authorized penetration tests when the target application uses a GraphQL API - When assessing single-page applications (React, Vue, Angular) that communicate via GraphQL - For evaluating mobile app backends that expose GraphQL endpoints - When testing microservice architectures with a GraphQL gateway or federation - During bug bounty progra
domain: cybersecurity
---
------|-------------|
| **Introspection** | GraphQL feature that exposes the full schema, types, fields, and mutations |
| **Query Depth** | The nesting level of a GraphQL query; deep queries can cause DoS |
| **Query Complexity** | A score calculated from the cost of resolving each field in a query |
| **Batching** | Sending multiple queries in a single HTTP request for parallel execution |
| **Aliases** | GraphQL feature allowing the same field to be queried multiple times with different arguments |
| **Fragments** | Reusable field selections that can cause circular references if not validated |
| **N+1 Problem** | Unoptimized resolvers causing exponential database queries for nested fields |
| **Field-level Authorization** | Access control applied to individual fields rather than entire types |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **InQL (Burp Extension)** | GraphQL introspection scanner and query generator for Burp Suite |
| **GraphQL Voyager** | Interactive schema visualization tool |
| **Altair GraphQL Client** | Desktop GraphQL IDE for crafting and testing queries |
| **clairvoyance** | Schema enumeration when introspection is disabled |
| **graphql-cop** | GraphQL security auditing tool (`pip install graphql-cop`) |
| **BatchQL** | GraphQL batching attack tool for rate limit bypass |

## Common Scenarios

### Scenario 1: Introspection Exposes Internal Schema
Introspection is enabled in production, revealing internal types like `AdminSettings`, `InternalUser`, and mutations like `deleteAllUsers`. This provides a complete roadmap for further attacks.

### Scenario 2: Missing Field-Level Authorization
The `User` type exposes `passwordHash`, `ssn`, and `internalNotes` fields. While the frontend only queries `name` and `email`, any authenticated user can request sensitive fields directly.

### Scenario 3: Batch Login Bypass
The GraphQL endpoint accepts batch queries. By sending 1000 login mutation attempts in a single HTTP request, an attacker bypasses IP-based rate limiting that only counts HTTP requests.

### Scenario 4: Nested Query DoS
A social network API allows querying `friends { friends { friends { ... } } }` up to unlimited depth. A 10-level nested query causes the server to process millions of database queries, resulting in denial of service.

## Output Format

```
## GraphQL Security Assessment Report

**Target**: https://target.example.com/graphql
**Engine**: Apollo Server 4.x
**Assessment Date**: 2024-01-15

### Findings Summary
| Finding | Severity | Status |
|---------|----------|--------|
| Introspection enabled in production | Medium | VULNERABLE |
| Missing field-level authorization | High | VULNERABLE |
| No query depth limit | High | VULNERABLE |
| Batch query rate limit bypass | High | VULNERABLE |
| GraphiQL IDE exposed | Low | VULNERABLE |
| SQL injection in user query | Critical | VULNERABLE |
| CSRF on mutations | Medium | PASS (custom header required) |

### Critical: SQL Injection via user Query
**Location**: `user(name: String)` query argument
**Payload**: `{ user(name: "' OR 1=1--") { id email role } }`
**Impact**: Full database read access via GraphQL interface

### High: Batch Authentication Bypass
**Location**: POST /graphql (array body)
**Payload**: Array of 100 login mutations in single request
**Impact**: Rate limiting bypassed; 100 password attempts per HTTP request

### Recommendation
1. Disable introspection in production environments
2. Implement field-level authorization on all sensitive fields
3. Set query depth limit (max 7-10 levels)
4. Set query complexity limit and cost analysis
5. Disable or rate-limit batch queries
6. Remove GraphiQL/Playground from production
7. Parameterize all database queries in resolvers
```