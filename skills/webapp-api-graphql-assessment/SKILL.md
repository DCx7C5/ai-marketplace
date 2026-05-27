---
name: webapp-api-graphql-assessment
description: "Webapp Api Graphql Assessment."
domain: cybersecurity
---

--|
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
