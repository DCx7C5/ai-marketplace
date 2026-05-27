---
name: webapp-injection-ssrf-server
description: "-| | 169.254.169.254 (AWS metadata) | HTTP | IAM credentials retrieved | | 127."
domain: cybersecurity
---

-|
| 169.254.169.254 (AWS metadata) | HTTP | IAM credentials retrieved |
| 127.0.0.1:6379 (Redis) | Gopher | Commands executed |
| 127.0.0.1:9200 (Elasticsearch) | HTTP | Index listing retrieved |
| 10.0.0.5:8080 (Internal API) | HTTP | Admin panel accessible |

### Impact
- AWS IAM temporary credentials exfiltrated (S3 read/write access)
- Internal Redis server accessible (potential RCE)
- Internal Elasticsearch data exposed (user records)
- Full internal network scanning capability

### Recommendation
1. Implement strict URL allowlisting (only allow known trusted domains)
2. Block requests to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16)
3. Upgrade to AWS IMDSv2 (requires session token header)
4. Disable unused URL protocols (gopher, file, dict, ftp)
5. Use a dedicated outbound proxy for server-side requests with DNS resolution controls
```
