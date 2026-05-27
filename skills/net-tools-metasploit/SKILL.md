---
name: net-tools-metasploit
description: "Net Tools Metasploit."
domain: cybersecurity
---

|
| **EternalBlue (MS17-010)** | Critical SMB vulnerability in SMBv1 allowing remote code execution as SYSTEM without authentication, originally developed by the NSA and leaked by Shadow Brokers |
| **SMB Signing** | Cryptographic signing of SMB packets to prevent tampering and relay attacks; when disabled, attackers can relay NTLM authentication to other SMB hosts |
| **Pass-the-Hash** | Authentication technique using captured NTLM password hashes directly instead of plaintext passwords, bypassing the need to crack the hash |
| **NTLM Relay** | Attack where captured NTLM authentication is forwarded to a different server in real-time, granting the attacker access as the relayed user |
| **PsExec** | Remote execution technique that uploads a service binary to the ADMIN$ share and creates a Windows service to execute commands as SYSTEM |
| **Null Session** | Anonymous SMB connection (empty username and password) that may expose share listings, user enumeration, and policy information on misconfigured systems |

## Tools & Systems

- **Metasploit Framework**: Exploitation framework with dedicated SMB scanner, exploit, and post-exploitation modules for comprehensive SMB testing
- **CrackMapExec**: Swiss-army knife for SMB enumeration, credential testing, share enumeration, and command execution across Windows networks
- **Impacket**: Python library providing psexec, smbclient, ntlmrelayx, and other tools for low-level SMB protocol interaction
- **Responder**: LLMNR/NBT-NS/mDNS poisoner that captures NTLM hashes from Windows name resolution fallback behavior
- **enum4linux-ng**: Updated SMB enumeration tool for extracting users, groups, shares, and policies from Windows/Samba hosts

## Common Scenarios

### Scenario: Internal Penetration Test Targeting Windows Domain via SMB

**Context**: During an internal penetration test for a financial services firm, the tester has network access to the corporate VLAN (10.10.0.0/16). The scope includes testing all Windows servers and workstations for SMB-related vulnerabilities. Active Directory domain is CORP.EXAMPLE.COM with approximately 200 hosts.

**Approach**:
1. Scan the entire /16 for open SMB ports and enumerate OS versions with CrackMapExec
2. Identify 12 hosts running Windows Server 2012 R2 without MS17-010 patch applied
3. Exploit EternalBlue on a non-critical file server (10.10.5.23) to gain SYSTEM access
4. Extract local administrator password hash using hashdump and discover password reuse across 47 hosts
5. Use pass-the-hash to access a domain controller, extracting the NTDS.dit database
6. Demonstrate that SMB signing is disabled on 83% of hosts, enabling relay attacks
7. Document the complete attack chain showing how one unpatched system led to full domain compromise

**Pitfalls**:
- EternalBlue exploit can cause a blue screen of death (BSOD) on the target, especially on older or unstable systems
- Running psexec on heavily monitored endpoints may trigger EDR alerts and burn the engagement
- Performing hashdump on domain controllers with large databases can cause performance degradation
- Not checking for SMBv1 explicitly -- some scanners may miss it if SMBv2/v3 is also available

## Output Format

```
## SMB Vulnerability Assessment Report

**Engagement**: Internal Penetration Test
**Target Range**: 10.10.0.0/16 (CORP.EXAMPLE.COM)
**SMB Hosts Discovered**: 187

### Critical Findings

**Finding 1: MS17-010 (EternalBlue) - 12 Unpatched Hosts**
- Severity: Critical (CVSS 9.8)
- Affected: 10.10.5.23, 10.10.5.24, 10.10.8.10 (+ 9 others)
- Impact: Remote code execution as SYSTEM without authentication
- Exploited: Yes - gained SYSTEM on 10.10.5.23
- Remediation: Apply MS17-010 patch, disable SMBv1

**Finding 2: SMB Signing Disabled - 155/187 Hosts**
- Severity: High (CVSS 7.5)
- Impact: NTLM relay attacks allow credential forwarding
- Exploited: Yes - relayed domain admin credentials
- Remediation: Enable SMB signing via Group Policy

**Finding 3: Local Admin Password Reuse - 47 Hosts**
- Severity: High (CVSS 7.2)
- Impact: Compromise of one host enables lateral movement to 47 systems
- Remediation: Deploy LAPS (Local Administrator Password Solution)
```
