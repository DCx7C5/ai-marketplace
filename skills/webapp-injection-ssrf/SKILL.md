---
name: webapp-injection-ssrf
description: "--| | 10.0.0.5 | 6379 | Redis | Yes | | 10.0.0.10 | 9200 | Elasticsearch | Yes | | 169."
domain: cybersecurity
---

--|
| 10.0.0.5 | 6379 | Redis | Yes |
| 10.0.0.10 | 9200 | Elasticsearch | Yes |
| 169.254.169.254 | 80 | AWS Metadata | Yes |

### Remediation
- Implement allowlist of permitted external domains for URL fetching
- Block requests to private IP ranges and cloud metadata endpoints
- Use IMDSv2 (token-required) for AWS instance metadata
- Disable unused URL schemes (gopher, file, dict)
- Implement network-level segmentation for application servers
```
