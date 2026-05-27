---
name: webapp-logic-business
description: - During authorized penetration tests when automated scanners have found few technical vulnerabilities - When assessing e-commerce platforms for pricing, cart, and payment flow manipulations - For testing multi-step workflows (registration, checkout, approval processes) for bypass opportunities - When evaluating rate-limited features like vouchers,
domain: cybersecurity
---
------|-------------|
| **Business Logic Flaw** | A vulnerability in the application's workflow or rules that allows unintended actions |
| **Price Manipulation** | Modifying price, quantity, or total values in client-side requests |
| **Workflow Bypass** | Skipping required steps in a multi-step business process |
| **Race Condition** | Exploiting concurrent request processing to violate business constraints |
| **Privilege Escalation** | Gaining higher permissions through business process manipulation |
| **Negative Testing** | Testing with unexpected values (negative, zero, null, extreme) |
| **State Manipulation** | Changing application state in an order not intended by the business logic |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Request interception, modification, and sequence testing |
| **Burp Turbo Intruder** | High-speed request sending for race condition testing |
| **Burp Sequencer** | Token randomness analysis for predictable reference testing |
| **OWASP ZAP** | Open-source alternative for proxy-based testing |
| **Postman** | Workflow testing with collection runners and environment variables |
| **Custom scripts** | Python/bash scripts for automated business logic testing |

## Common Scenarios

### Scenario 1: Coupon Code Stacking
An e-commerce site allows applying multiple coupon codes. By stacking "WELCOME10", "SAVE20", and "VIP30", the total discount exceeds the product price, resulting in a negative balance or free order.

### Scenario 2: Race Condition on Fund Transfer
A banking application checks balance before transfer but does not lock the account. Sending two simultaneous $1000 transfers from a $1000 balance results in both succeeding, creating money from nothing.

### Scenario 3: Checkout Price Override
The checkout flow sends the total amount in the POST body. Intercepting and changing the total from $499.99 to $0.01 results in a successful order at the manipulated price.

### Scenario 4: Password Reset Token Reuse
The password reset flow generates a one-time token but does not invalidate it after use. The same token can be used repeatedly to reset the password.

## Output Format

```
## Business Logic Vulnerability Finding

**Vulnerability**: Price Manipulation in Checkout Flow
**Severity**: Critical (CVSS 9.1)
**Location**: POST /api/checkout - `total` parameter
**OWASP Category**: A04:2021 - Insecure Design

### Reproduction Steps
1. Add item to cart (price: $499.99)
2. Proceed to checkout
3. Intercept POST /api/checkout request in Burp
4. Modify "total" from 499.99 to 0.01
5. Forward the request; order completes at $0.01

### Business Rules Violated
| Rule | Expected | Actual |
|------|----------|--------|
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