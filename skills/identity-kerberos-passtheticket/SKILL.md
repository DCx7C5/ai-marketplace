---
name: identity-kerberos-passtheticket
description: Pass-the-Ticket (PtT) is a lateral movement technique that uses stolen Kerberos tickets (TGT or TGS) to authenticate to services without knowing the user's password. By extracting Kerberos tickets from memory (LSASS) on a compromised host, an attacker can inject those tickets into their own session to impersonate the ticket owner and access resourc
domain: cybersecurity
---
---|---------|---------|
| Mimikatz | Ticket export/import | sekurlsa::tickets /export, kerberos::ptt |
| Rubeus | Ticket dumping and injection | dump, ptt, tgtdeleg |
| Impacket ticketConverter | Convert between formats | ticketConverter.py ticket.kirbi ticket.ccache |
| Impacket psexec/smbexec | Remote execution with ticket | KRB5CCNAME=ticket.ccache psexec.py |

## Detection Indicators

- Event ID 4768 with unusual client addresses
- Event ID 4769 service ticket requests from unexpected hosts
- TGT usage from different IP than the TGT was issued to
- Multiple authentications from same ticket across different workstations

## Validation Criteria

- [ ] Kerberos tickets extracted from compromised host
- [ ] Tickets injected into attacker session
- [ ] Lateral movement demonstrated using stolen tickets
- [ ] Evidence captured for reporting