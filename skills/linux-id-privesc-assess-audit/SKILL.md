---
name: linux-id-privesc-assess-audit
description: "Linux Id Privesc Assess Audit."
domain: cybersecurity
---

|
| **SUID Binary** | A Linux binary with the Set User ID bit enabled, which executes with the file owner's privileges (typically root) regardless of who runs it |
| **SeImpersonatePrivilege** | A Windows privilege that allows a process to impersonate another user's security token, commonly abused by service accounts to escalate to SYSTEM |
| **Kernel Exploit** | An exploit targeting a vulnerability in the operating system kernel to gain ring-0 or root/SYSTEM-level access |
| **GTFOBins** | A curated list of Unix binaries that can be exploited for privilege escalation, file read/write, or shell escape when misconfigured |
| **LOLBAS** | Living Off The Land Binaries and Scripts; legitimate Windows binaries that can be abused for code execution, file operations, or persistence |
| **DLL Hijacking** | Exploiting the DLL search order on Windows to load a malicious DLL by placing it in a directory searched before the legitimate DLL location |
| **Token Impersonation** | A Windows technique where a compromised process with appropriate privileges captures and uses another user's access token to execute commands as that user |

## Tools & Systems

- **linPEAS / winPEAS**: Automated privilege escalation enumeration scripts that check hundreds of potential escalation vectors on Linux and Windows
- **GTFOBins / LOLBAS**: Reference databases of Unix binaries and Windows binaries that can be exploited for privilege escalation when misconfigured
- **PrintSpoofer / GodPotato**: Windows privilege escalation tools that exploit `SeImpersonatePrivilege` to achieve SYSTEM-level access from service accounts
- **Linux Exploit Suggester**: Script that compares the target kernel version against a database of known kernel exploits to identify applicable exploits

## Common Scenarios

### Scenario: Privilege Escalation on a Linux Web Server

**Context**: During a penetration test, the tester gained a low-privilege shell as `www-data` on an Ubuntu 22.04 web server through a PHP file upload vulnerability. The goal is to escalate to root to demonstrate full server compromise.

**Approach**:
1. Run `linpeas.sh` which identifies that `www-data` can run `/usr/bin/find` as root via sudo without a password
2. Verify with `sudo -l`: `(root) NOPASSWD: /usr/bin/find`
3. Consult GTFOBins for the `find` sudo entry: `sudo find . -exec /bin/bash -p \; -quit`
4. Execute the command and obtain a root shell
5. As root, access `/etc/shadow` to extract password hashes, read database credentials from the application configuration, and access the MySQL database containing customer PII
6. Document: initial access as www-data -> sudo misconfiguration -> root shell -> database access -> 75,000 customer records accessible

**Pitfalls**:
- Running kernel exploits without testing on a similar system first, risking a kernel panic and system crash
- Not checking for container environments where apparent root access may be limited to the container namespace
- Ignoring cloud metadata endpoints accessible from the compromised host that may yield IAM credentials
- Failing to enumerate capabilities and SUID binaries after checking sudo, missing alternative escalation paths

## Output Format

```
## Finding: Sudo Misconfiguration Allowing Root Escalation via find

**ID**: PRIV-001
**Severity**: Critical (CVSS 8.8)
**Affected Host**: web-prod-01 (10.10.5.15)
**OS**: Ubuntu 22.04 LTS
**Initial Access**: www-data (via PHP file upload - WEB-004)
**Escalation Technique**: MITRE ATT&CK T1548.003 - Sudo and Sudo Caching

**Description**:
The www-data user is configured in /etc/sudoers to execute /usr/bin/find as root
without a password. The find command supports the -exec flag which can spawn a
root shell, effectively granting www-data unrestricted root access.

**Proof of Concept**:
www-data@web-prod-01:~$ sudo -l
(root) NOPASSWD: /usr/bin/find
www-data@web-prod-01:~$ sudo find . -exec /bin/bash -p \; -quit
root@web-prod-01:~# id
uid=0(root) gid=0(root) groups=0(root)

**Impact**:
Full root access on the production web server. From root, the tester accessed
database credentials in /var/www/app/.env, connected to MySQL, and confirmed
read access to 75,000 customer records including names, emails, and addresses.

**Remediation**:
1. Remove the /usr/bin/find sudo entry for www-data
2. If find access is required, restrict it to specific directories with --no-exec
3. Audit all sudo entries for binaries listed in GTFOBins
4. Implement sudo logging with auditd for all privileged command execution
```
