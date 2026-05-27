---
name: webapp-auth-evilginx-verify
description: "--| | Newly registered lookalike domains | Domain monitoring and certificate transparency logs | | SSL certificates for suspicious domains | CT log monitoring (crt."
domain: cybersecurity
---

--|
| Newly registered lookalike domains | Domain monitoring and certificate transparency logs |
| SSL certificates for suspicious domains | CT log monitoring (crt.sh, Censys) |
| Unusual login locations after phishing | SIEM correlation of authentication events |
| Session cookie replay from different IP | Conditional access policy alerts |
| AiTM proxy headers in traffic | Network inspection for proxy artifacts |

## Validation Criteria

- [ ] EvilGinx3 deployed with valid SSL certificates
- [ ] Phishlet configured and enabled for target service
- [ ] Lure URL generated and accessible
- [ ] Test credentials captured successfully through phishing flow
- [ ] Session cookies captured and validated for MFA bypass
- [ ] Session hijack demonstrated in browser with stolen cookies
- [ ] Post-authentication access to target service confirmed
- [ ] Evidence documented with screenshots and session logs
