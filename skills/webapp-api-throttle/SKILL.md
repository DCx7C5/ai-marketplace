---
name: webapp-api-throttle
description: "Webapp Api Throttle."
domain: cybersecurity
---

|
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
