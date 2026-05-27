---
name: webapp-api-throttle
description: - Protecting authentication endpoints against brute force and credential stuffing attacks - Preventing API abuse and resource exhaustion from automated scripts and bots - Implementing fair usage quotas for different API consumer tiers (free, premium, enterprise) - Defending against denial-of-service attacks at the application layer - Meeting compli
domain: cybersecurity
---
---|------------|
| **Sliding Window** | Rate limiting algorithm that tracks requests in a rolling time window, providing smoother rate enforcement than fixed windows |
| **Token Bucket** | Algorithm where tokens are added at a fixed rate and consumed per request, allowing controlled bursts up to the bucket capacity |
| **Fixed Window** | Simplest rate limiting where requests are counted per fixed time window (e.g., per minute), susceptible to burst at window boundaries |
| **429 Too Many Requests** | HTTP status code indicating the client has exceeded the rate limit, accompanied by Retry-After header |
| **Retry-After Header** | HTTP response header telling the client how many seconds to wait before retrying, essential for well-behaved API clients |
| **Distributed Rate Limiting** | Rate limiting across multiple server instances using shared state (Redis, Memcached) to maintain accurate global counters |

## Tools & Systems

- **Redis**: In-memory data store used for distributed rate limit counters with atomic operations via Lua scripts
- **Kong Rate Limiting Plugin**: API gateway plugin supporting fixed-window and sliding-window rate limiting with Redis backend
- **express-rate-limit**: Express.js middleware for simple rate limiting with Redis, Memcached, or in-memory stores
- **Flask-Limiter**: Flask extension for rate limiting with support for multiple backends and configurable limits per endpoint
- **Envoy Rate Limit Service**: Centralized rate limiting service for Envoy-based service mesh architectures

## Common Scenarios

### Scenario: Implementing Rate Limiting for a Public API

**Context**: A company launches a public API with free, premium, and enterprise tiers. The API must protect against abuse while providing fair access to paying customers. The API runs on 6 instances behind an AWS ALB.

**Approach**:
1. Deploy Redis Cluster (3 nodes) for distributed rate limit state
2. Implement sliding window rate limiter using Redis sorted sets with Lua scripts for atomicity
3. Configure per-tier limits: Free (60 req/min), Premium (300 req/min), Enterprise (1000 req/min)
4. Add stricter limits on authentication endpoints (5 req/min per IP) regardless of tier
5. Implement resource-intensive endpoint limits (search: 10 req/min free, export: 5 req/hour)
6. Set rate limit response headers on every response (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
7. Return 429 with Retry-After header and JSON error body when limits are exceeded
8. Set up Prometheus metrics for rate limit hits and CloudWatch alarms for unusual patterns

**Pitfalls**:
- Using in-memory rate limiting without shared state across instances, allowing limit bypass by hitting different servers
- Not implementing rate limiting on authentication endpoints separately from general API limits
- Using fixed windows that allow burst at window boundaries (2x the limit in a short period)
- Not including rate limit headers on successful responses, giving clients no visibility into their quota
- Trusting X-Forwarded-For for IP identification without validating it against the load balancer

## Output Format

```
## Rate Limiting Implementation Report

**API**: Public API v2
**Algorithm**: Sliding Window (Redis Sorted Sets)
**Backend**: Redis Cluster (3 nodes)
**Deployment**: 6 API instances behind AWS ALB

### Rate Limit Configuration

| Tier | Default | Search | Export | Auth (per IP) |
|------|---------|--------|--------|---------------|
| Free | 60/min | 10/min | 5/hour | 5/min |
| Premium | 300/min | 50/min | 20/hour | 5/min |
| Enterprise | 1000/min | 200/min | 100/hour | 10/min |

### Validation Results (k6 load test)

- Free tier: Rate limited at 61st request (correct)
- Premium tier: Rate limited at 301st request (correct)
- Cross-instance: Rate limiting consistent across all 6 instances
- Redis failover: Rate limiting degrades gracefully (allows traffic) when Redis is unreachable
- Retry-After header: Accurate within 1 second of actual reset time
- Response overhead: < 2ms added latency per request for rate limit check
```