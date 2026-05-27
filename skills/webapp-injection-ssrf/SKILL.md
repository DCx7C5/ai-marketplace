---
name: webapp-injection-ssrf
description: - When testing URL/webhook input parameters where server-side responses are not reflected - During assessment of applications that fetch external resources (avatars, previews, imports) - When testing PDF generators, image processors, or document converters for SSRF - During cloud security assessments to detect metadata endpoint access - When evalua
domain: cybersecurity
---
------|-------------|
| Blind SSRF | Server makes request but response is not visible to attacker |
| Out-of-Band Detection | Using external callbacks (DNS, HTTP) to confirm SSRF execution |
| DNS Rebinding | Technique to bypass IP-based SSRF filters by changing DNS resolution |
| Cloud Metadata | Instance metadata endpoints accessible via SSRF for credential theft |
| Gopher Protocol | Protocol allowing crafted payloads to interact with internal TCP services |
| Time-Based Detection | Detecting SSRF success by measuring response time differences |
| SSRF Chain | Combining SSRF with other vulnerabilities for greater impact |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Collaborator | Out-of-band interaction server for DNS and HTTP callback detection |
| interact.sh | Open-source OOB interaction tool by ProjectDiscovery |
| SSRFmap | Automated SSRF detection and exploitation framework |
| Gopherus | Generate gopher payloads for exploiting internal services via SSRF |
| webhook.site | Free webhook receiver for testing SSRF callbacks |
| rebinder.net | DNS rebinding service for bypassing SSRF IP filters |

## Common Scenarios

1. **Cloud Credential Theft** — Exploit blind SSRF to access AWS/GCP/Azure metadata endpoints and steal IAM credentials for cloud account compromise
2. **Internal Service Discovery** — Use timing-based blind SSRF to enumerate internal network hosts and open ports
3. **Redis Exploitation** — Chain blind SSRF with gopher:// protocol to execute commands on internal Redis instances
4. **Webhook Abuse** — Exploit webhook URL fields to scan internal networks and exfiltrate data through OOB channels
5. **PDF Generator SSRF** — Inject internal URLs into PDF generation features to exfiltrate internal content in rendered documents

## Output Format

```
## Blind SSRF Assessment Report
- **Target**: http://target.com/api/fetch-url
- **Detection Method**: Burp Collaborator DNS + HTTP callback
- **Internal Access Confirmed**: Yes

### Findings
| # | Input Point | Payload | Detection | Impact |
|---|------------|---------|-----------|--------|
| 1 | POST /api/fetch url parameter | http://collaborator | HTTP callback | Confirmed SSRF |
| 2 | POST /api/avatar avatar_url | http://169.254.169.254 | Timing (2.3s vs 0.1s) | Cloud metadata |
| 3 | POST /api/webhook callback | gopher://127.0.0.1:6379 | Redis write confirmed | RCE potential |

### Internal Network Map
| Host | Port | Service | Accessible |
|------|------|---------|-----------|
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