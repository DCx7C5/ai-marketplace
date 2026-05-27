---
name: webapp-design-prototype-review
description: "--| | 1 | POST /api/merge __proto__ | EJS escapeFunction | Template render | RCE | | 2 | POST /api/profile __proto__ | isAdmin property | Auth middleware | Privilege Escalation | | 3 | URL ?"
domain: cybersecurity
---

--|
| 1 | POST /api/merge __proto__ | EJS escapeFunction | Template render | RCE |
| 2 | POST /api/profile __proto__ | isAdmin property | Auth middleware | Privilege Escalation |
| 3 | URL ?__proto__[innerHTML] | innerHTML property | DOM write | Client-Side XSS |

### Remediation
- Use Object.create(null) for configuration objects instead of {}
- Freeze Object.prototype with Object.freeze(Object.prototype)
- Sanitize __proto__ and constructor keys in user input
- Use Map instead of plain objects for user-controlled data
- Update vulnerable npm packages (lodash, merge-deep, etc.)
```
