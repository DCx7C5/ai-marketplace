---
name: webapp-language-type
description: "Webapp Language Type."
domain: cybersecurity
---

--|
| 0 == "password" | TRUE | String cast to 0 |
| true == "password" | TRUE | Non-empty string is truthy |
| "0e123" == "0e456" | TRUE | Both are scientific notation = 0 |
| NULL == 0 | TRUE | NULL cast to 0 |

### Remediation
- Replace all == with === (strict comparison) in security-critical code
- Use password_verify() for password comparison instead of direct comparison
- Use hash_equals() for timing-safe hash comparison
- Validate input types before comparison operations
- Enable PHP strict_types declaration in all files
```
