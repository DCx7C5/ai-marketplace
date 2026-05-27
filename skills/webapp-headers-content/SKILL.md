---
name: webapp-headers-content
description: "--|"
domain: cybersecurity
---
--|
| 1 | AngularJS via CDN | Load angular.min.js + template injection | Full XSS |
| 2 | Missing base-uri | <base href="https://evil.com/"> | Script hijack |

### Remediation
- Remove whitelisted CDN domains; use nonce-based or hash-based CSP
- Add base-uri 'self' to prevent base element injection
- Add object-src 'none' to block plugin-based execution
- Migrate from unsafe-inline to strict nonce-based policy
- Implement strict-dynamic for modern CSP3 browsers
```
