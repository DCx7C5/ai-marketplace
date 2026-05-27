---
name: webapp-waf-firewall
description: "--|"
domain: cybersecurity
---
--|
| 1 | 1' OR 1=1-- | {"id":"1' OR 1=1--"} | JSON content-type |
| 2 | UNION SELECT | /*!50000UNION*/ /*!50000SELECT*/ | MySQL version comments |
| 3 | <script>alert(1)</script> | <svg/onload=alert(1)> | Alternative tag+event |

### Remediation
- Enable JSON body inspection in WAF rules
- Implement behavioral analysis alongside signature detection
- Add rules for uncommon HTML tags and event handlers
- Enable deep content inspection for all HTTP methods
- Implement request normalization before rule evaluation
```
