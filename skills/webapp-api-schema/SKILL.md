---
name: webapp-api-schema
description: API schema validation enforces that all data exchanged through APIs conforms to a predefined structure defined in OpenAPI Specification (OAS) or JSON Schema documents. This prevents injection attacks (SQLi, XSS, XXE), blocks mass assignment by rejecting unknown properties, prevents data leakage by validating response schemas, and ensures type safet
domain: cybersecurity
---
|---|---|
| `additionalProperties: true` or missing | Mass assignment | Set `additionalProperties: false` |
| No `maxLength` on strings | Buffer overflow, DoS | Add appropriate `maxLength` constraints |
| No `pattern` on string fields | Injection attacks | Add regex patterns to restrict input |
| No `enum` for fixed-value fields | Unexpected input processing | Use `enum` for fields with known values |
| `format: password` without TLS | Credential exposure | Enforce HTTPS-only server URLs |
| Missing error response schemas | Information leakage | Define all 4xx/5xx response schemas |
| `readOnly` fields in request body | Data manipulation | Enforce `readOnly` server-side |

## References

- OpenAPI Specification v3.1: https://spec.openapis.org/oas/v3.1.0
- Cloudflare API Shield Schema Validation: https://developers.cloudflare.com/api-shield/security/schema-validation/
- Redocly API Security by Design: https://redocly.com/learn/security
- Impart Security API Validation: https://www.impart.ai/blog/detect-and-fix-api-vulnerabilities-using-validation-secure-principles-and-real-time-response
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x00-header/