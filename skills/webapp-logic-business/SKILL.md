---
name: webapp-logic-business
description: "Webapp Logic Business."
domain: cybersecurity
---

--|
| Server-side price calculation | Total computed server-side | Client-submitted total accepted |
| Coupon single use | One coupon per order | Same coupon applied 5 times |
| Negative quantity check | Quantity >= 1 | Quantity -1 accepted (credit issued) |
| Race condition on transfer | Balance checked atomically | Dual transfer exceeded balance |

### Impact
- Financial loss: orders processed at attacker-controlled prices
- Inventory loss: products shipped for $0.01
- Reward abuse: unlimited referral credits via self-referral
- Double-spending via race condition on transfers

### Recommendation
1. Perform all price calculations server-side; never trust client-submitted totals
2. Implement server-side validation for quantity (positive integers only)
3. Use database-level locks or atomic transactions for financial operations
4. Implement idempotency keys to prevent duplicate transaction processing
5. Rate-limit and log coupon applications, referral submissions, and transfers
```
