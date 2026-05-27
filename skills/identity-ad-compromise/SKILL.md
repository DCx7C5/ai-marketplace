---
name: identity-ad-compromise
description: Active Directory (AD) compromise investigation is a critical incident response capability that focuses on identifying how attackers gained access to domain services, what persistence mechanisms they established, and the scope of credential compromise. Since 88% of breaches involve compromised credentials (Verizon 2025 DBIR), AD is the primary targe
domain: cybersecurity
---
-------|--------|-------------|
| 4624 | Security | Successful logon |
| 4625 | Security | Failed logon |
| 4648 | Security | Explicit credential logon |
| 4662 | Security | Operation on AD object |
| 4768 | Security | Kerberos TGT requested |
| 4769 | Security | Kerberos service ticket requested |
| 4771 | Security | Kerberos pre-authentication failed |
| 4776 | Security | NTLM credential validation |
| 5136 | Security | Directory object modified |
| 5137 | Security | Directory object created |
| 4706 | Security | Trust created |
| 4707 | Security | Trust removed |
| 4742 | Security | Computer account changed |
| 8222 | System | Shadow copy created |

## Tools for AD Investigation

| Tool | Purpose |
|------|---------|
| **BloodHound** | Attack path mapping and privilege escalation analysis |
| **Pingcastle** | AD security assessment and risk scoring |
| **Purple Knight** | AD vulnerability scanning by Semperis |
| **ADRecon** | Active Directory data gathering |
| **Mimikatz** | Credential extraction and Kerberos analysis |
| **Impacket** | DCSync detection and NTLM relay analysis |
| **Velociraptor** | Remote forensic artifact collection |
| **Timeline Explorer** | Event log timeline analysis |

## MITRE ATT&CK Mapping

| Technique | ID | Relevance |
|-----------|----|-----------|
| DCSync | T1003.006 | NTDS.dit credential extraction |
| Golden Ticket | T1558.001 | Kerberos TGT forgery |
| Silver Ticket | T1558.002 | Service ticket forgery |
| Kerberoasting | T1558.003 | Service account hash extraction |
| Pass-the-Hash | T1550.002 | NTLM hash reuse |
| Group Policy Modification | T1484.001 | Persistence via GPO |
| Account Manipulation | T1098 | Privileged group changes |
| SID-History Injection | T1134.005 | Privilege escalation |

## References

- [CISA: Detecting and Mitigating Active Directory Compromises](https://www.cisa.gov/resources-tools/resources/detecting-and-mitigating-active-directory-compromises)
- [Microsoft: Total Identity Compromise IR Lessons](https://techcommunity.microsoft.com/blog/microsoftsecurityexperts/total-identity-compromise-microsoft-incident-response-lessons-on-securing-active/3753391)
- [Semperis: Top 10 Active Directory Risks](https://www.semperis.com/blog/10-ad-risks-caught-by-identity-forensics-and-incident-response/)
- [Fidelis: Active Directory Compromise Response](https://fidelissecurity.com/threatgeek/active-directory-security/respond-after-an-active-directory-compromise/)