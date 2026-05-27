---
name: webapp-injection-xxe-xml
description: "--|"
domain: cybersecurity
---
--|
| 1 | XXE File Read | POST /api/import | SYSTEM "file:///etc/passwd" | Local File Disclosure |
| 2 | Blind XXE | POST /api/upload | External DTD with OOB | Data Exfiltration |
| 3 | SSRF via XXE | POST /api/parse | SYSTEM "http://169.254.169.254/" | Cloud Credential Theft |

### Remediation
- Disable external entity processing in XML parser configuration
- Use JSON instead of XML where possible
- Implement XML schema validation with strict DTD restrictions
- Block outbound connections from XML processing services
```
