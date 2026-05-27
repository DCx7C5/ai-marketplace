---
name: linux-forensic-mem-analysis-credentials-extract
description: "| | Volatility 3 | Memory forensics framework with hashdump, lsadump, cachedump plugins | | pypykatz | Python implementation of Mimikatz for cross-platform LSASS analysis | | Mimikatz | Windows credential extraction tool (used offline against dumps) | | secretsdump."
domain: cybersecurity
---

|
| Volatility 3 | Memory forensics framework with hashdump, lsadump, cachedump plugins |
| pypykatz | Python implementation of Mimikatz for cross-platform LSASS analysis |
| Mimikatz | Windows credential extraction tool (used offline against dumps) |
| secretsdump.py | Impacket tool for extracting secrets from SAM/SYSTEM/SECURITY |
| hashcat | Password hash cracking for recovered NTLM and DCC2 hashes |
| John the Ripper | Alternative password cracking tool |
| Rubeus | Kerberos ticket manipulation and extraction tool |
| Impacket | Python toolkit for working with Windows network protocols and credentials |

## Common Scenarios

**Scenario 1: Post-Breach Credential Assessment**
Extract all cached credentials from LSASS memory to determine which accounts were exposed, prioritize password resets based on privilege level, check for golden ticket material (krbtgt hash), assess if cloud credentials were accessible.

**Scenario 2: Lateral Movement Investigation**
Extract NTLM hashes and Kerberos tickets to understand how the attacker moved between systems, identify pass-the-hash/pass-the-ticket artifacts, correlate extracted credentials with network logon events in event logs.

**Scenario 3: Ransomware Operator Credential Theft**
Analyze pre-encryption memory dump for Mimikatz execution evidence, extract all available credential types, determine if domain admin credentials were obtained, assess if krbtgt was compromised (golden ticket), plan credential rotation strategy.

**Scenario 4: Cloud Credential Theft from Endpoint**
Search endpoint memory for AWS access keys, Azure tokens, and GCP service account keys stored by CLI tools and browsers, identify exposed cloud permissions, immediately rotate discovered credentials, audit cloud audit logs for unauthorized access.

## Output Format

```
Credential Extraction Summary:
  Source: memory.raw (16 GB, Windows 10 Build 19041)
  LSASS PID: 684

  Credentials Recovered:
    Local NTLM Hashes:        4 accounts
    Domain NTLM Hashes:       3 accounts
    Kerberos TGTs:             2 tickets
    Kerberos TGS:              5 service tickets
    Plaintext Passwords:       1 (WDigest - svc.backup)
    Cached Domain Creds:       2 DCC2 hashes
    LSA Secrets:               3 service account passwords
    DPAPI Master Keys:         4 keys recovered
    Cloud Credentials:         1 AWS access key, 1 Azure token

  Highest Privilege Compromised: Domain Admin (CORP\domain.admin)

  Recommended Actions:
    - Immediate: Reset all extracted account passwords
    - Immediate: Rotate AWS access key AKIA...
    - Urgent: Double krbtgt password reset (golden ticket mitigation)
    - High: Revoke all Kerberos tickets via krbtgt rotation
    - Medium: Audit DPAPI-protected data exposure
```
