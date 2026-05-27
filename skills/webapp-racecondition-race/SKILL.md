---
name: webapp-racecondition-race
description: - When testing applications with transaction-based functionality (payments, transfers, coupons) - During assessment of rate-limiting or attempt-limiting mechanisms - When testing multi-step workflows (registration, password reset, MFA) - During bug bounty hunting for logic flaws in state-changing operations - When evaluating applications with inven
domain: cybersecurity
---
------|-------------|
| TOCTOU | Time-of-Check-to-Time-of-Use flaw where state changes between validation and action |
| Single-Packet Attack | Sending multiple HTTP/2 requests in one TCP packet for precise synchronization |
| Last-Byte Sync | HTTP/1.1 technique holding final byte of multiple requests then releasing simultaneously |
| Limit Overrun | Exceeding one-time-use limits by exploiting race windows in validation logic |
| Hidden State Machine | Exploiting transitional states in multi-step application workflows |
| Gate Mechanism | Turbo Intruder feature that holds requests until all are queued, then releases simultaneously |
| Connection Warming | Pre-establishing connections to reduce network jitter in race condition attacks |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Turbo Intruder | Burp Suite extension for high-speed race condition exploitation |
| Burp Suite Repeater | Group send feature for basic race condition testing |
| Nuclei | Template-based scanner with race condition detection templates |
| Python threading | Custom multi-threaded race condition scripts |
| racepwn | Dedicated race condition testing framework |
| asyncio/aiohttp | Python async HTTP for concurrent request sending |

## Common Scenarios

1. **Coupon Double-Spend** — Redeem a single-use coupon multiple times by sending concurrent redemption requests before the server marks it as used
2. **Balance Overdraft** — Transfer more money than available by sending simultaneous transfer requests that each pass the balance check
3. **MFA Bypass** — Submit multiple MFA codes simultaneously to bypass rate limiting on verification attempts
4. **Inventory Manipulation** — Purchase more items than available stock by exploiting race conditions in inventory decrement logic
5. **Account Registration Bypass** — Create multiple accounts with the same email by submitting concurrent registration requests

## Output Format

```
## Race Condition Assessment Report
- **Target**: http://target.com/api/redeem-coupon
- **Technique**: HTTP/2 Single-Packet Attack via Turbo Intruder
- **Concurrent Requests**: 20
- **Successful Exploitations**: 4 out of 20

### Findings
| # | Endpoint | Operation | Expected | Actual | Severity |
|---|----------|-----------|----------|--------|----------|
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