---
name: identity-kerberos-kerbattack
description: Kerberoasting is a post-exploitation technique that targets service accounts in Active Directory by requesting Kerberos TGS (Ticket Granting Service) tickets for accounts with Service Principal Names (SPNs) set. These tickets are encrypted with the service account's NTLM hash, allowing offline brute-force cracking without generating failed login ev
domain: cybersecurity
---
---|---------|----------|
| Rubeus | Kerberoasting and ticket manipulation | Windows (.NET) |
| Impacket GetUserSPNs.py | Remote Kerberoasting | Linux/Python |
| PowerView | SPN enumeration | Windows (PowerShell) |
| hashcat | Offline password cracking | Cross-platform |
| John the Ripper | Offline password cracking | Cross-platform |

## Detection Indicators

- Event ID 4769: Kerberos Service Ticket Request with RC4 encryption (0x17)
- Anomalous TGS requests from a single account in short timeframe
- TGS requests for services the user normally does not access
- Honeypot SPN accounts with alerting on ticket requests

## Validation Criteria

- [ ] SPN accounts enumerated and documented
- [ ] TGS tickets extracted in crackable format
- [ ] Offline cracking attempted with appropriate wordlists
- [ ] Cracked credentials validated
- [ ] Access level of compromised accounts assessed