---
name: identity-credentials-lazagne
description: LaZagne is an open-source post-exploitation tool designed to retrieve credentials stored on local systems. It supports Windows, Linux, and macOS, with the most extensive module library for Windows. LaZagne recovers passwords from browsers (Chrome, Firefox, Edge, Opera), email clients (Outlook, Thunderbird), databases (PostgreSQL, MySQL, SQLite), sy
domain: cybersecurity
---
---|---------|----------|
| LaZagne | Multi-source credential extraction | Windows/Linux/macOS |
| Mimikatz | LSASS/DPAPI credential dumping | Windows |
| SharpChrome | Chrome credential extraction (.NET) | Windows |
| SharpDPAPI | DPAPI credential decryption | Windows |
| CrackMapExec | Credential validation and spraying | Linux |
| Impacket | Remote credential testing | Linux (Python) |

## LaZagne Module Coverage (Windows)

| Category | Modules |
|----------|---------|
| Browsers | Chrome, Firefox, Edge, Opera, IE, Brave, Vivaldi |
| Email | Outlook, Thunderbird, Foxmail |
| Databases | PostgreSQL, MySQL, SQLiteDB, Robomongo |
| Sysadmin | PuTTY, WinSCP, FileZilla, OpenSSH, RDPManager |
| Windows | Credential Manager, Vault, DPAPI, Autologon |
| WiFi | Stored Wi-Fi passwords |
| Git | Git Credential Store, Git Credential Manager |
| SVN | TortoiseSVN |
| Chat | Pidgin, Skype |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| LaZagne.exe process execution | EDR process monitoring with hash-based detection |
| Access to Chrome Login Data SQLite DB | File access monitoring on browser credential stores |
| DPAPI CryptUnprotectData API calls | API hooking and ETW tracing |
| Access to Windows Credential Manager | Event 5379 (Credential Manager read) |
| Mass credential store enumeration | Behavioral analysis for sequential access patterns |
| Python interpreter accessing credential files | Script block logging and file access auditing |

## Validation Criteria

- [ ] LaZagne deployed on compromised endpoint
- [ ] Full credential extraction completed (all modules)
- [ ] Credentials exported in JSON format for analysis
- [ ] Recovered credentials parsed and deduplicated
- [ ] High-value credentials identified and prioritized
- [ ] Domain credentials validated against AD
- [ ] Lateral movement opportunities identified from recovered creds
- [ ] Evidence documented with appropriate handling procedures