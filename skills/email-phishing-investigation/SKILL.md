---
name: email-phishing-investigation
description: "Email Phishing Investigation."
domain: cybersecurity
---

--|
| **SPF (Sender Policy Framework)** | DNS TXT record specifying which mail servers are authorized to send on behalf of a domain |
| **DKIM** | DomainKeys Identified Mail — cryptographic signature proving email content was not altered in transit |
| **DMARC** | Domain-based Message Authentication, Reporting and Conformance — policy combining SPF and DKIM alignment |
| **Credential Harvesting** | Phishing technique using fake login pages to capture username/password combinations |
| **Business Email Compromise (BEC)** | Social engineering attack using compromised or spoofed executive email for financial fraud |
| **Message Trace** | O365/Exchange log showing email routing, delivery status, and filtering actions for forensic analysis |

## Tools & Systems

- **Microsoft Defender for Office 365**: Email security platform with Safe Links, Safe Attachments, and Threat Explorer for investigation
- **URLScan.io**: Free URL analysis service capturing screenshots, DOM, cookies, and network requests
- **Any.Run**: Interactive sandbox for detonating malicious files and URLs with real-time behavior analysis
- **Proofpoint TAP**: Targeted Attack Protection dashboard showing clicked URLs and delivered threats per user
- **PhishTool**: Dedicated phishing email analysis platform automating header parsing and IOC extraction

## Common Scenarios

- **Credential Phishing**: Fake O365 login page — check proxy for POST requests, force password resets for submitters
- **Macro-Enabled Document**: Word doc with VBA macro — sandbox shows PowerShell download cradle, check endpoints for execution
- **QR Code Phishing (Quishing)**: Email contains QR code linking to credential harvester — decode QR, submit URL to sandbox
- **Thread Hijacking**: Attacker uses compromised mailbox to reply in existing threads — check for impossible travel or new inbox rules
- **Voicemail Phishing**: Fake voicemail notification with HTML attachment — analyze attachment for redirect chains

## Output Format

```
PHISHING INCIDENT REPORT — PHI-2024-0315
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reported:     2024-03-15 09:12 UTC by jsmith (Finance)
Sender:       attacker@evil-domain[.]com (SPF: FAIL, DKIM: NONE, DMARC: FAIL)
Subject:      Urgent: Password Reset Required
Payload:      Credential harvesting URL

IOCs:
  URL:        hxxps://evil-login[.]example[.]com/office365
  Domain:     evil-login[.]example[.]com (registered 2024-03-14, Namecheap)
  IP:         185.234.xx.xx (VT: 12/90 malicious)

Scope:
  Recipients: 47 users across Finance and HR departments
  Clicked:    5 users visited phishing URL
  Submitted:  2 users entered credentials (confirmed via POST in proxy logs)

Containment:
  [DONE] 47 emails purged via Compliance Search
  [DONE] Domain blocked on proxy and DNS sinkhole
  [DONE] 2 user passwords reset, sessions revoked
  [DONE] MFA enforced for both compromised accounts
  [DONE] Inbox rules audited — no forwarding rules found

Status:       RESOLVED — No evidence of lateral movement post-compromise
```
