---
name: identity-ad-nopac
description: noPac is a critical exploit chain combining two Active Directory vulnerabilities: CVE-2021-42278 (sAMAccountName spoofing) and CVE-2021-42287 (KDC PAC confusion). Together, they allow any authenticated domain user to escalate to Domain Admin privileges, potentially achieving full domain compromise in under 60 seconds. CVE-2021-42278 allows an attac
domain: cybersecurity
---
---|---------|----------|
| noPac (cube0x0) | Automated scanner and exploiter | Python |
| noPac (Ridter) | Alternative exploit implementation | Python |
| Impacket | Kerberos ticket manipulation, DCSync | Python |
| CrackMapExec | Vulnerability scanning module | Python |
| Rubeus | Windows Kerberos ticket operations | Windows (.NET) |
| secretsdump.py | Post-exploitation credential dumping | Python |

## CVE Details

| CVE | Description | CVSS | Patch |
|-----|-------------|------|-------|
| CVE-2021-42278 | sAMAccountName spoofing (machine accounts) | 7.5 | KB5008102 |
| CVE-2021-42287 | KDC PAC confusion / privilege escalation | 7.5 | KB5008380 |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| Machine account sAMAccountName change | Event 4742 (computer account changed) with sAMAccountName modification |
| New machine account creation | Event 4741 (computer object created) |
| TGT request for account without trailing $ | Kerberos audit log analysis |
| S4U2self requests from non-DC machine accounts | Event 4769 with unusual service ticket requests |
| Rapid sequence: create account, rename, request TGT | SIEM correlation rule for noPac attack pattern |

## Validation Criteria

- [ ] Domain scanned for noPac vulnerability
- [ ] MachineAccountQuota verified (default 10)
- [ ] Exploit executed successfully (shell or DCSync)
- [ ] Domain Admin privileges obtained from standard user
- [ ] DCSync performed to dump domain credentials
- [ ] KRBTGT hash obtained for persistence validation
- [ ] Attack chain documented with timestamps
- [ ] Patch status verified (KB5008380, KB5008602)