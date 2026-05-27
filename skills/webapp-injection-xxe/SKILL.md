---
name: webapp-injection-xxe
description: "--| | /etc/passwd | 42 user accounts, service accounts identified | | /var/www/html/config."
domain: cybersecurity
---

--|
| /etc/passwd | 42 user accounts, service accounts identified |
| /var/www/html/config.php | Database credentials in plaintext |
| /etc/hostname | Internal hostname: prod-web-01 |

### Recommendation
1. Disable external entity processing in the XML parser
2. Disable DTD processing entirely if not required
3. Use JSON instead of XML where possible
4. Implement input validation to reject DTD declarations in XML input
5. Apply least-privilege file system permissions for the web server user
```
