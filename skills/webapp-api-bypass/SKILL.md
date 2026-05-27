---
name: webapp-api-bypass
description: - Testing whether API rate limiting can be circumvented to enable brute force attacks on authentication endpoints - Assessing the effectiveness of API throttling controls against credential stuffing or account enumeration - Evaluating if rate limits are enforced consistently across all API versions, methods, and encoding formats - Testing if API ga
domain: cybersecurity
---
---|------------|
| **Rate Limiting** | Controlling the number of requests a client can make to an API within a time window, typically enforced per IP, per user, or per API key |
| **Unrestricted Resource Consumption** | OWASP API4:2023 - APIs that do not properly limit the size or number of resources requested, enabling DoS or brute force attacks |
| **X-Forwarded-For Spoofing** | Manipulating the X-Forwarded-For header to make the server believe requests originate from different IP addresses, bypassing IP-based rate limits |
| **Credential Stuffing** | Automated injection of stolen username/password pairs against login endpoints, requiring rate limit bypass for large-scale attacks |
| **Token Bucket** | Rate limiting algorithm that allows bursts of requests up to a bucket size, refilling at a constant rate |
| **Sliding Window** | Rate limiting algorithm that tracks requests in a rolling time window, more resistant to burst attacks than fixed windows |

## Tools & Systems

- **Burp Suite Turbo Intruder**: High-performance request sender for rate limit testing using Python-based scripting engine
- **ffuf**: Fast web fuzzer capable of testing rate limits with configurable request rates and header manipulation
- **wfuzz**: Web fuzzer with support for header injection, parameter fuzzing, and rate limit evasion techniques
- **Postman Collection Runner**: Automated collection execution with variable rotation for rate limit bypass testing
- **Gatling/k6**: Load testing tools that simulate realistic traffic patterns to test rate limiting under production-like conditions

## Common Scenarios

### Scenario: Login API Rate Limit Bypass Assessment

**Context**: A financial services API implements rate limiting on the login endpoint to prevent brute force attacks. The security team wants to verify the effectiveness of these controls before a compliance audit.

**Approach**:
1. Baseline: Send 100 requests to `POST /api/v1/auth/login` - rate limited at request 10 per minute per IP
2. Test X-Forwarded-For rotation: Send 100 requests with unique X-Forwarded-For values - rate limit bypassed (all requests return 401, not 429)
3. Test path variation: `/api/v1/auth/login/` (trailing slash) resets the rate limit counter
4. Test API versioning: `/api/v2/auth/login` has no rate limiting configured (shadow API)
5. Test parameter pollution: Adding `?_=<random>` to each request bypasses the rate limit
6. Test concurrent requests: 50 simultaneous requests from same IP - 45 succeed before rate limit kicks in (race condition in counter)
7. Determine that rate limiting is implemented at the nginx reverse proxy level using IP-only tracking, trusting X-Forwarded-For header without validation

**Pitfalls**:
- Sending too many requests too fast and causing actual denial of service to the test environment
- Not testing rate limits on password reset, MFA verification, and account enumeration endpoints
- Assuming the rate limit applies globally when it may be per-endpoint or per-method only
- Missing race conditions in rate limit counters that allow burst bypasses
- Not testing both authenticated and unauthenticated rate limiting separately

## Output Format

```
## Finding: Rate Limiting Bypass via X-Forwarded-For Header Spoofing

**ID**: API-RATE-001
**Severity**: High (CVSS 7.3)
**OWASP API**: API4:2023 - Unrestricted Resource Consumption
**Affected Endpoints**:
  - POST /api/v1/auth/login
  - POST /api/v1/auth/forgot-password
  - POST /api/v1/auth/verify-mfa

**Description**:
The API rate limiting implementation relies on the X-Forwarded-For header
to identify client IP addresses. Since the application sits behind a load
balancer that does not strip or validate this header, an attacker can set
arbitrary X-Forwarded-For values to bypass the 10 requests/minute rate limit
on authentication endpoints.

**Bypass Methods Confirmed**:
1. X-Forwarded-For rotation: 1000 login attempts in 60 seconds (vs 10 limit)
2. Trailing slash path variation: /auth/login/ treated as separate endpoint
3. API v2 endpoint: No rate limiting configured
4. Race condition: 50 concurrent requests, 45 succeed before counter updates

**Impact**:
An attacker can perform unlimited brute force attacks against any user
account, bypassing the rate limit designed to prevent credential stuffing.
At 1000 attempts per minute, a 6-digit PIN can be brute-forced in under
17 minutes.

**Remediation**:
1. Configure the load balancer to set X-Forwarded-For and strip client-provided values
2. Implement rate limiting at the application layer using authenticated user ID, not just IP
3. Normalize URL paths before applying rate limit rules (strip trailing slashes, enforce lowercase)
4. Apply rate limits consistently across all API versions and content types
5. Use atomic rate limit counters (Redis INCR) to prevent race conditions
6. Implement progressive delays (exponential backoff) in addition to hard limits
```