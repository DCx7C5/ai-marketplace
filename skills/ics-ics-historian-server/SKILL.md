---
name: ics-ics-historian-server
description: - When deploying a new historian server in an OT environment and configuring it securely from the start - When hardening an existing historian after a security assessment identified it as a high-risk target - When designing historian data replication architecture through a DMZ for IT access to process data - When implementing access controls to pre
domain: cybersecurity
---
{sev.upper()} ({len(findings)}) ---")
                for f in findings:
                    report.append(f"  [{f.finding_id}] {f.title}")
                    report.append(f"    {f.detail}")
                    report.append(f"    Fix: {f.remediation}")

        return "\n".join(report)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "10.30.1.50"
    audit = HistorianSecurityAudit(target, "PI")
    audit.check_network_exposure()
    audit.check_authentication()
    audit.check_data_integrity()
    print(audit.generate_report())
```

### Step 2: Harden Historian Server

Apply security hardening based on vendor security guides and IEC 62443 requirements.

```powershell
# OSIsoft PI Server Hardening Script (Windows)
# Based on OSIsoft Security Best Practices Guide

# 1. Disable PI Trust authentication - migrate to Windows Integrated Security
# In PI SMT (System Management Tools):
# Security > Mappings & Trusts > Delete all Trust entries
# Create PI Mappings for Windows groups instead

# 2. Disable the default piadmin account
# In PI SMT: Security > Identities, Users & Groups
# Set piadmin account to disabled

# 3. Configure Windows Firewall for PI Server
New-NetFirewallRule -DisplayName "PI Data Archive" -Direction Inbound `
    -Protocol TCP -LocalPort 5450 -Action Allow `
    -RemoteAddress "10.30.0.0/16","10.20.0.0/16" `
    -Description "Allow PI SDK connections from OT zones only"

New-NetFirewallRule -DisplayName "PI AF Server" -Direction Inbound `
    -Protocol TCP -LocalPort 5457 -Action Allow `
    -RemoteAddress "10.30.0.0/16" `
    -Description "Allow PI AF connections from Operations zone"

New-NetFirewallRule -DisplayName "PI Vision HTTPS" -Direction Inbound `
    -Protocol TCP -LocalPort 443 -Action Allow `
    -RemoteAddress "172.16.0.0/16" `
    -Description "Allow PI Vision HTTPS from DMZ only"

# Block HTTP (force HTTPS)
New-NetFirewallRule -DisplayName "Block HTTP" -Direction Inbound `
    -Protocol TCP -LocalPort 80 -Action Block

# Block RDP from non-authorized sources
New-NetFirewallRule -DisplayName "RDP Restrict" -Direction Inbound `
    -Protocol TCP -LocalPort 3389 -Action Allow `
    -RemoteAddress "10.30.1.100" `
    -Description "Allow RDP from admin jump server only"

# 4. Enable Windows audit policies for CIP-007 compliance
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Account Lockout" /success:enable /failure:enable
auditpol /set /subcategory:"File System" /success:enable /failure:enable
auditpol /set /subcategory:"Registry" /success:enable /failure:enable

# 5. Configure PI audit trail for data integrity
# In PI SMT: Audit > Enable auditing for security changes
# Enable auditing for: point creation/deletion, data edits, security changes
```

### Step 3: Implement Secure Data Replication to DMZ

Configure historian data replication through the DMZ using PI-to-PI interfaces or data diodes to provide IT access to process data without exposing the OT historian.

```yaml
# Historian DMZ Replication Architecture
#
# OT Historian (Level 3) --> Data Diode --> DMZ Historian (Level 3.5) <-- Enterprise (Level 4)
#
# Key principle: Enterprise users NEVER connect directly to the OT historian.
# Data flows unidirectionally from OT to DMZ.

architecture:
  ot_historian:
    location: "Level 3 - Site Operations"
    server: "PI-OT-01 (10.30.1.50)"
    role: "Primary data collection from OPC servers and PLCs"
    access: "OT operators and engineers only"

  data_diode:
    location: "Between Level 3 and Level 3.5"
    device: "Waterfall Security Unidirectional Gateway"
    direction: "OT -> DMZ (physically enforced one-way)"
    protocol: "PI-to-PI replication protocol"

  dmz_historian:
    location: "Level 3.5 - DMZ"
    server: "PI-DMZ-01 (172.16.1.50)"
    role: "Read-only mirror of OT historian for enterprise access"
    access: "Enterprise users via PI Vision (HTTPS)"
    data_delay: "Near real-time (typically 5-30 second delay)"

  enterprise_access:
    method: "PI Vision web application on DMZ historian"
    authentication: "Windows Integrated Security with MFA"
    protocol: "HTTPS (TLS 1.2+)"
    restrictions:
      - "Read-only access to process data"
      - "No write-back capability to OT historian"
      - "No direct database queries - PI Vision API only"
      - "Session timeout after 30 minutes of inactivity"
```

## Key Concepts

| Term | Definition |
|------|------------|
| Process Historian | Server that collects, stores, and serves time-series process data from industrial control systems at high frequency (sub-second to seconds) |
| PI Trust | Legacy OSIsoft PI authentication method based on IP address/hostname; insecure and should be migrated to Windows Integrated Security |
| Data Diode | Hardware-enforced unidirectional gateway ensuring historian data flows only from OT to DMZ, preventing reverse access |
| PI-to-PI Interface | OSIsoft replication mechanism that synchronizes PI data between servers, used for DMZ data mirroring |
| Audit Trail | Historian feature logging all modifications to historical data with before/after values, user identity, and timestamp |
| Tag Security | Per-tag access control in PI determining which users/applications can read or write specific process data points |

## Tools & Systems

- **OSIsoft PI Server**: Industry-leading process historian by AVEVA (formerly OSIsoft) used in 90%+ of large industrial facilities
- **AVEVA Historian**: Time-series database for process data with SQL-like query interface
- **Waterfall Security**: Hardware data diode for unidirectional historian replication
- **PI Vision**: Web-based visualization tool for PI data, deployed in DMZ for enterprise access

## Output Format

```
Historian Security Assessment Report
=====================================
Historian: [Type and Version]
Server: [Hostname/IP]
Network Zone: [Purdue Level]

AUTHENTICATION:
  PI Trust entries: [N] (should be 0)
  Default accounts: [enabled/disabled]
  Windows auth: [enabled/disabled]

NETWORK EXPOSURE:
  Open ports: [list]
  Unnecessary services: [list]

DATA INTEGRITY:
  Audit trail: [enabled/disabled]
  Backup tested: [date]

DMZ REPLICATION:
  Method: [PI-to-PI / Data Diode / VPN]
  Direction: [Unidirectional / Bidirectional]
```