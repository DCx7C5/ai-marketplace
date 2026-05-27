---
name: windows-hardening-defender
description: "Windows Hardening Defender."
domain: cybersecurity
---

--|
| **ASR Rules** | Attack Surface Reduction rules that block specific high-risk behaviors at the endpoint level |
| **Controlled Folder Access** | Ransomware protection feature that prevents unauthorized applications from modifying files in protected folders |
| **Network Protection** | Blocks outbound connections to low-reputation or known-malicious domains using SmartScreen intelligence |
| **Exploit Protection** | System and per-application memory mitigations (DEP, ASLR, CFG) to prevent exploitation |
| **BAFS (Block at First Sight)** | Cloud-based zero-day protection that holds suspicious files for cloud analysis before allowing execution |
| **Tamper Protection** | Prevents unauthorized changes to Defender security settings, even by local administrators |

## Tools & Systems

- **Microsoft 365 Defender Portal**: security.microsoft.com for centralized management and reporting
- **Microsoft Intune**: Cloud-based endpoint management for Defender policy deployment
- **PowerShell (Set-MpPreference)**: Local configuration of Defender settings
- **WDAC (Windows Defender Application Control)**: Complementary application control technology
- **Microsoft Defender for Endpoint API**: REST API for automation and custom integrations

## Common Pitfalls

- **Enabling all ASR rules in Block mode immediately**: Some ASR rules cause false positives with legitimate software (Office macros, admin scripts). Always deploy in Audit mode first and monitor for 2-4 weeks.
- **Not configuring Controlled Folder Access exclusions**: Backup software, database applications, and development tools may be blocked from writing to protected folders. Add exclusions proactively.
- **Ignoring tamper protection**: Without tamper protection, malware or insiders can disable Defender via PowerShell or registry edits. Enable tamper protection through the M365 Defender portal.
- **Running Defender alongside third-party AV**: Defender enters passive mode when third-party AV is present. Ensure you are using the intended AV solution and configure Defender appropriately (EDR-only mode if keeping third-party AV).
- **Forgetting cloud connectivity requirements**: Cloud-delivered protection and BAFS require endpoints to reach Microsoft cloud services. Verify proxy/firewall rules allow Defender cloud traffic.
