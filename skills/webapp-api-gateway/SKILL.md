---
name: webapp-api-gateway
description: "| | Authentication | JWT Plugin | Cognito IdP, 1-hour max TTL | | Rate Limiting | Rate Limiting Plugin | 60 req/min (user), Redis-backed | | Request Validation | OAS Validation | Strict mode, no additional properties | | TLS | Kong TLS | TLS 1."
domain: cybersecurity
---

|
| Authentication | JWT Plugin | Cognito IdP, 1-hour max TTL |
| Rate Limiting | Rate Limiting Plugin | 60 req/min (user), Redis-backed |
| Request Validation | OAS Validation | Strict mode, no additional properties |
| TLS | Kong TLS | TLS 1.3 only, HSTS enabled |
| mTLS | mTLS Auth Plugin | Client cert required for admin APIs |
| WAF | AWS WAF | SQLi, XSS, rate-based rules |
| Headers | Response Transformer | Server header removed, security headers added |
| Logging | HTTP Log Plugin | CloudWatch, security metric filters |

### Verification Results

- JWT validation: Expired/invalid tokens correctly rejected (tested 50 payloads)
- Rate limiting: Enforced at 60 req/min, 429 returned with Retry-After header
- Request validation: Malformed requests rejected with 400 (tested 30 invalid payloads)
- mTLS: Requests without client certificate rejected with 401
- WAF: SQL injection payloads blocked (tested top 100 SQLi patterns)
```
