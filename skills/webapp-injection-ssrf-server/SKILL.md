---
name: webapp-injection-ssrf-server
description: - During authorized penetration tests when the application fetches URLs provided by users (webhooks, URL previews, file imports) - When testing cloud-hosted applications for access to instance metadata services - For assessing PDF generators, screenshot services, or any feature that renders external content - When evaluating microservice architectu
domain: cybersecurity
---
------|-------------|
| **SSRF** | Server-Side Request Forgery - making the server send requests to unintended destinations |
| **Blind SSRF** | SSRF where the response is not returned to the attacker, requiring OOB detection |
| **Cloud Metadata** | Instance metadata services (169.254.169.254) exposing credentials and configuration |
| **Gopher Protocol** | Protocol allowing raw TCP data transmission, enabling attacks on internal services |
| **DNS Rebinding** | DNS attack that switches IP resolution to bypass SSRF hostname allowlists |
| **TOCTOU** | Time-of-check to time-of-use race condition in URL validation |
| **IMDSv2** | AWS metadata service v2 requiring session tokens, mitigating basic SSRF |
| **Open Redirect Chain** | Using an open redirect to bypass URL allowlists in SSRF filters |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Request modification and Collaborator for blind SSRF detection |
| **SSRFmap** | Automated SSRF exploitation framework with protocol support |
| **interactsh** | Out-of-band interaction detection for blind SSRF |
| **Gopherus** | Generates gopher payloads for exploiting internal services |
| **rbndr.us** | DNS rebinding service for SSRF filter bypass |
| **singularity** | DNS rebinding attack framework for automated exploitation |

## Common Scenarios

### Scenario 1: Webhook URL SSRF to AWS Credentials
A webhook configuration endpoint allows specifying a callback URL. Pointing it to `http://169.254.169.254/latest/meta-data/iam/security-credentials/` returns temporary AWS IAM credentials that can be used to access S3 buckets and other AWS services.

### Scenario 2: PDF Generator SSRF
A feature that generates PDFs from URLs makes server-side requests. Providing `http://127.0.0.1:8080/admin` as the URL generates a PDF containing the internal admin panel content.

### Scenario 3: Image URL SSRF with Protocol Bypass
An avatar URL field is filtered for HTTP/HTTPS but accepts `file://` protocol. Using `file:///etc/passwd` as the avatar URL causes the server to read local files and include content in the response.

### Scenario 4: Blind SSRF to Internal Redis
A URL fetch feature does not return response content but confirms success/failure. Using gopher protocol payloads, an attacker writes data to an internal Redis instance, achieving remote code execution.

## Output Format

```
## SSRF Vulnerability Finding

**Vulnerability**: Server-Side Request Forgery (Full SSRF)
**Severity**: Critical (CVSS 9.1)
**Location**: POST /api/webhooks - `callback_url` parameter
**OWASP Category**: A10:2021 - Server-Side Request Forgery

### Reproduction Steps
1. Send POST /api/webhooks with callback_url set to http://169.254.169.254/latest/meta-data/
2. Server makes request to AWS metadata endpoint
3. Response contains AWS instance metadata including IAM role name
4. Follow up with IAM credentials endpoint to retrieve temporary access keys

### Confirmed Access
| Target | Protocol | Response |
|--------|----------|----------|
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