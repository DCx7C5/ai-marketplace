---
name: webapp-auth-evilginx-verify
description: EvilGinx3 is a man-in-the-middle attack framework used for phishing login credentials along with session cookies, enabling bypass of multi-factor authentication (MFA). Unlike traditional credential phishing that only captures usernames and passwords, EvilGinx3 operates as a transparent reverse proxy between the victim and the legitimate authenticat
domain: cybersecurity
---
---|---------|----------|
| EvilGinx3 | AiTM phishing framework | Linux |
| GoPhish | Phishing campaign management | Cross-platform |
| EvilGoPhish | Combined EvilGinx3 + GoPhish integration | Linux |
| Cookie-Editor | Browser cookie import/export | Browser Extension |
| Modlishka | Alternative AiTM proxy framework | Linux |
| Muraena | Alternative AiTM phishing proxy | Linux |

## Phishlet Targets

| Target Service | Phishlet | Captured Data |
|---------------|----------|---------------|
| Microsoft 365 | o365 | Session cookies, credentials |
| Google Workspace | google | Session cookies, credentials |
| Okta | okta | Session tokens, credentials |
| GitHub | github | Session cookies, credentials |
| AWS Console | aws | Session tokens, credentials |

## Detection Indicators

| Indicator | Detection Method |
|-----------|-----------------|
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