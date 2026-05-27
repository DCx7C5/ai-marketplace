---
name: webapp-enumeration-directory
description: "--| | /etc/passwd | User enumeration (42 accounts) | | /var/www/html/."
domain: cybersecurity
---

--|
| /etc/passwd | User enumeration (42 accounts) |
| /var/www/html/.env | Database credentials exposed |
| /home/deploy/.ssh/id_rsa | SSH private key recovered |
| /proc/self/environ | Environment variables with API keys |

### Filter Bypass Required
Original `../` stripped by filter. Successful bypass: `....//....//....//etc/passwd`

### Recommendation
1. Use an allowlist of permitted file names rather than accepting arbitrary paths
2. Resolve the canonical path and verify it stays within the intended directory
3. Run the web server with minimal file system permissions
4. Remove sensitive files from web-accessible directories
5. Disable PHP wrappers (allow_url_include, allow_url_fopen) if not required
```
