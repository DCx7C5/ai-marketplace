---
name: identity-ad-certificates-verify
description: ESC1 (Escalation Scenario 1) is a critical misconfiguration in Active Directory Certificate Services where a certificate template allows a low-privileged user to request a certificate on behalf of any other user, including Domain Admins. The vulnerability exists when a template has the CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT flag enabled (also called "Su
domain: cybersecurity
---
---|---------|----------|
| Certify | AD CS enumeration and certificate requests | Windows (.NET) |
| Certipy | AD CS enumeration, request, and authentication | Linux (Python) |
| Rubeus | Kerberos authentication with certificates (PKINIT) | Windows (.NET) |
| Mimikatz | Credential dumping post-escalation | Windows |
| secretsdump.py | Remote credential dumping (Impacket) | Linux (Python) |
| PSPKIAudit | PowerShell AD CS auditing module | Windows |
| ForgeCert | Certificate forgery tool | Windows (.NET) |

## Vulnerable Template Indicators

| Condition | Vulnerable Value |
|-----------|-----------------|
| msPKI-Certificate-Name-Flag | ENROLLEE_SUPPLIES_SUBJECT (1) |
| pkiExtendedKeyUsage | Client Authentication (1.3.6.1.5.5.7.3.2) |
| Enrollment Rights | Domain Users or Authenticated Users |
| msPKI-Enrollment-Flag | No manager approval required |
| CA Setting | No approval workflow enforced |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| Certificate request with SAN different from requester | Windows Event 4886 / 4887 on CA server |
| Unusual PKINIT authentication | Event 4768 with certificate-based pre-auth |
| Certify.exe or Certipy execution | EDR process monitoring and command-line logging |
| Mass certificate template enumeration | LDAP query monitoring for pkiCertificateTemplate objects |
| Certificate issued to non-matching UPN | CA audit logs and certificate transparency |

## Validation Criteria

- [ ] AD CS Certificate Authority enumerated
- [ ] Vulnerable ESC1 templates identified with Certify or Certipy
- [ ] Certificate requested with Domain Admin SAN successfully
- [ ] PKINIT authentication performed with forged certificate
- [ ] Domain Admin TGT obtained
- [ ] Privileged access to domain controller validated
- [ ] Full attack chain documented with evidence
- [ ] Remediation recommendations provided (disable Supply in Request, require manager approval)