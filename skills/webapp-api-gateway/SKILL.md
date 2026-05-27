---
name: webapp-api-gateway
description: - Deploying a centralized authentication and authorization layer for microservice APIs - Implementing rate limiting, throttling, and quota management across all API endpoints - Configuring request/response validation against OpenAPI specifications at the gateway level - Setting up TLS termination, mutual TLS, and certificate management for API traf
domain: cybersecurity
---
---|------------|
| **API Gateway** | Centralized entry point for all API traffic that enforces authentication, authorization, rate limiting, and request validation before routing to backend services |
| **Rate Limiting** | Controlling the number of API requests per client within a time window to prevent abuse and ensure fair resource allocation |
| **Request Validation** | Verifying that incoming API requests conform to the expected schema (data types, required fields, value ranges) before forwarding to backend services |
| **Mutual TLS (mTLS)** | Two-way TLS authentication where both the client and server present certificates, providing strong identity verification for API-to-API communication |
| **WAF Integration** | Web Application Firewall rules applied at the API gateway to block common attack patterns (SQLi, XSS, path traversal) |
| **OAuth2/OIDC** | Token-based authentication protocols where the gateway validates JWT tokens against an identity provider before allowing access |

## Tools & Systems

- **Kong Gateway**: Open-source API gateway with extensive plugin ecosystem for security, rate limiting, and authentication
- **AWS API Gateway**: Managed API gateway service with built-in throttling, WAF integration, and Lambda authorizers
- **Azure API Management**: Enterprise API gateway with policy-based security, developer portal, and Azure AD integration
- **Apigee (Google Cloud)**: API management platform with threat protection, quota management, and API analytics
- **Envoy Proxy**: High-performance proxy used as API gateway in service mesh architectures with extensive filter chain

## Common Scenarios

### Scenario: Securing a Microservice API with Kong Gateway

**Context**: A company is migrating from a monolithic API to microservices. Each microservice has its own REST API. The security team needs to implement centralized authentication, rate limiting, and request validation without modifying each service.

**Approach**:
1. Deploy Kong Gateway as the single entry point, routing traffic to 8 backend microservices
2. Configure JWT validation plugin to verify tokens against the company's Keycloak IdP
3. Apply rate limiting: 60 requests/minute for regular users, 300/minute for premium users, identified by JWT claims
4. Enable OAS validation plugin to reject requests that do not match the OpenAPI spec (blocks mass assignment and injection)
5. Configure mTLS for service-to-service communication behind the gateway
6. Set up response transformer to remove Server and X-Powered-By headers and add security headers
7. Integrate with AWS WAF for SQL injection and XSS protection rules
8. Configure access logging to CloudWatch with security metric filters and alerting

**Pitfalls**:
- Relying solely on the gateway for authorization when backend services also need to verify permissions
- Not configuring rate limiting per authenticated user (per-IP only allows attackers to bypass with IP rotation)
- Using verbose error responses from the gateway that reveal internal service architecture
- Not testing the gateway configuration with security tools after deployment
- Missing mutual TLS between the gateway and backend services, allowing direct backend access

## Output Format

```
## API Gateway Security Configuration Report

**Gateway**: Kong 3.5 (Kubernetes deployment)
**Backend Services**: 8 microservices
**Date**: 2024-12-15

### Security Controls Implemented

| Control | Plugin/Feature | Configuration |
|---------|---------------|---------------|
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