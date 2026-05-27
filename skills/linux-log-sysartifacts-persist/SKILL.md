---
name: linux-log-sysartifacts-persist
description: "Linux Log Sysartifacts Persist."
domain: cybersecurity
---

|
| chkrootkit | Rootkit detection scanner for Linux systems |
| rkhunter | Rootkit Hunter - checks for rootkits, backdoors, and local exploits |
| AIDE | Advanced Intrusion Detection Environment - file integrity monitor |
| auditd | Linux audit framework for system call and file access monitoring |
| last/lastb | Parse wtmp/btmp for login and failed login history |
| Plaso/log2timeline | Super-timeline creation including Linux artifacts |
| osquery | SQL-based system querying for live forensic investigation |
| Velociraptor | Endpoint agent with Linux artifact collection capabilities |

## Common Scenarios

**Scenario 1: SSH Brute Force Followed by Compromise**
Analyze auth.log for failed SSH attempts followed by success, identify the attacking IP, check .bash_history for post-compromise commands, examine authorized_keys for added backdoor keys, check crontab for persistence, review network connections.

**Scenario 2: Web Server Compromise via Application Vulnerability**
Examine web server access and error logs for exploitation attempts, check /tmp and /dev/shm for webshells, analyze the web server user's activity (www-data), check for privilege escalation via SUID binaries or kernel exploits, review outbound connections.

**Scenario 3: Insider Threat on Database Server**
Analyze the suspect user's bash_history for database dump commands, check for large tar/zip files in home directory or /tmp, examine scp/rsync commands for data transfer, review cron jobs for automated exfiltration, check USB device logs.

**Scenario 4: Crypto-Miner on Cloud Instance**
Check for high-CPU processes in /proc (live) or systemd service files, examine crontab entries for miner restart scripts, check /tmp for mining binaries, analyze network connections for mining pool communications, review authorized_keys for attacker access.

## Output Format

```
Linux Forensics Summary:
  System: webserver01 (Ubuntu 22.04 LTS)
  Hostname: webserver01.corp.local
  Kernel: 5.15.0-91-generic

  User Accounts:
    Total: 25 (3 with UID 0 - 1 ANOMALOUS)
    Interactive shells: 8 users
    Recently created: admin2 (created 2024-01-15)

  Authentication Events:
    Successful SSH logins: 456
    Failed SSH attempts: 12,345 (from 23 unique IPs)
    Sudo executions: 89

  Persistence Mechanisms Found:
    Cron jobs: 3 suspicious (reverse shell, miner restart)
    Systemd services: 1 unknown (update-checker.service)
    SSH keys: 2 unauthorized keys in root authorized_keys
    rc.local: Modified with download cradle

  Suspicious Activity:
    - bash_history contains wget to pastebin URL
    - SUID binary /tmp/.hidden/escalate found
    - /dev/shm/ contains compiled ELF binary
    - LD_PRELOAD in /etc/ld.so.preload pointing to /lib/.hidden.so

  Report: /cases/case-2024-001/linux/analysis/
```
