---
name: webapp-racecondition-race
description: "Webapp Racecondition Race."
domain: cybersecurity
---

-|
| 1 | POST /redeem-coupon | Single use coupon | 1 redemption | 4 redemptions | High |
| 2 | POST /transfer | Balance transfer | Limited by balance | Overdraft achieved | Critical |

### Race Window Analysis
- HTTP/2 single-packet: Reliable exploitation in <30 seconds
- Success rate: ~20% per batch of 20 requests
- Race window estimated: 50-100ms

### Remediation
- Implement database-level locking (SELECT FOR UPDATE) on critical operations
- Use optimistic concurrency control with version numbers
- Apply idempotency keys for state-changing requests
- Implement distributed locks for multi-server environments
```
