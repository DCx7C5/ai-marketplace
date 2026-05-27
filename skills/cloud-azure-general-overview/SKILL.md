---
name: cloud-azure-general-overview
description: Azure service principals are identity objects used by applications, services, and automation tools to access Azure resources. Attackers exploit service principals for privilege escalation, lateral movement, and persistent access. Key abuse patterns include: adding credentials to existing principals, assigning privileged roles, bypassing admin conse
domain: cybersecurity
---
--------|-----|-------------|
| Account Manipulation: Additional Cloud Credentials | T1098.001 | Adding credentials to service principal |
| Valid Accounts: Cloud Accounts | T1078.004 | Using compromised service principal |
| Account Discovery: Cloud Account | T1087.004 | Enumerating service principals |
| Steal Application Access Token | T1528 | OAuth token theft via service principal |

## References

- Splunk Detection: Azure AD Service Principal Abuse
- Semperis: Service Principal Ownership Abuse in Entra ID
- MITRE ATT&CK Cloud Matrix
- Microsoft: Securing service principals in Entra ID