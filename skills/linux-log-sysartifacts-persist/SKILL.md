---
name: linux-log-sysartifacts-persist
description: - When investigating a compromised Linux server or workstation - For identifying persistence mechanisms (cron, systemd, SSH keys) - When tracing user activity through shell history and authentication logs - During incident response to determine the scope of a Linux-based breach - For detecting rootkits, backdoors, and unauthorized modifications
domain: cybersecurity
---
$cronfile ---" >> /cases/case-2024-001/linux/persistence/cron_analysis.txt
    cat "$cronfile" 2>/dev/null >> /cases/case-2024-001/linux/persistence/cron_analysis.txt
    echo "" >> /cases/case-2024-001/linux/persistence/cron_analysis.txt
done

# User cron tabs
for cronfile in /mnt/evidence/var/spool/cron/crontabs/*; do
    echo "--- User crontab: $(basename $cronfile) ---" >> /cases/case-2024-001/linux/persistence/cron_analysis.txt
    cat "$cronfile" 2>/dev/null >> /cases/case-2024-001/linux/persistence/cron_analysis.txt
    echo "" >> /cases/case-2024-001/linux/persistence/cron_analysis.txt
done

# Check systemd services for persistence
echo "=== SYSTEMD SERVICES ===" > /cases/case-2024-001/linux/persistence/systemd_analysis.txt
find /mnt/evidence/etc/systemd/system/ -name "*.service" -newer /mnt/evidence/etc/os-release \
   >> /cases/case-2024-001/linux/persistence/systemd_analysis.txt

for svc in /mnt/evidence/etc/systemd/system/*.service; do
    echo "--- $(basename $svc) ---" >> /cases/case-2024-001/linux/persistence/systemd_analysis.txt
    cat "$svc" >> /cases/case-2024-001/linux/persistence/systemd_analysis.txt
    echo "" >> /cases/case-2024-001/linux/persistence/systemd_analysis.txt
done

# Check authorized SSH keys (backdoor detection)
echo "=== SSH AUTHORIZED KEYS ===" > /cases/case-2024-001/linux/persistence/ssh_keys.txt
find /mnt/evidence/home/ /mnt/evidence/root/ -name "authorized_keys" -exec sh -c \
   'echo "--- {} ---"; cat {}; echo ""' \; >> /cases/case-2024-001/linux/persistence/ssh_keys.txt

# Check rc.local and init scripts
cat /mnt/evidence/etc/rc.local 2>/dev/null > /cases/case-2024-001/linux/persistence/rc_local.txt

# Check /etc/profile.d/ for login-triggered scripts
ls -la /mnt/evidence/etc/profile.d/ > /cases/case-2024-001/linux/persistence/profile_scripts.txt

# Check for LD_PRELOAD hijacking
grep -r "LD_PRELOAD" /mnt/evidence/etc/ 2>/dev/null > /cases/case-2024-001/linux/persistence/ld_preload.txt
cat /mnt/evidence/etc/ld.so.preload 2>/dev/null >> /cases/case-2024-001/linux/persistence/ld_preload.txt
```

### Step 4: Analyze Shell History and Command Execution

```bash
# Analyze bash history for each user
python3 << 'PYEOF'
import os, glob

print("=== SHELL HISTORY ANALYSIS ===\n")

suspicious_commands = [
    'wget', 'curl', 'nc ', 'ncat', 'netcat', 'python -c', 'python3 -c',
    'perl -e', 'base64', 'chmod 777', 'chmod +s', '/dev/tcp', '/dev/udp',
    'nmap', 'masscan', 'hydra', 'john', 'hashcat', 'passwd', 'useradd',
    'iptables -F', 'ufw disable', 'history -c', 'rm -rf /', 'dd if=',
    'crontab', 'at ', 'systemctl enable', 'ssh-keygen', 'scp ', 'rsync',
    'tar czf', 'zip -r', 'openssl enc', 'gpg --encrypt', 'shred',
    'chattr', 'setfacl', 'awk', '/tmp/', '/dev/shm/'
]

for hist_file in glob.glob('/cases/case-2024-001/linux/users/*/.bash_history'):
    username = hist_file.split('/')[-2]
    print(f"User: {username}")

    with open(hist_file, 'r', errors='ignore') as f:
        lines = f.readlines()

    print(f"  Total commands: {len(lines)}")
    flagged = []
    for i, line in enumerate(lines):
        line = line.strip()
        for cmd in suspicious_commands:
            if cmd in line.lower():
                flagged.append((i+1, line))
                break

    if flagged:
        print(f"  Suspicious commands: {len(flagged)}")
        for lineno, cmd in flagged:
            print(f"    Line {lineno}: {cmd[:120]}")
    print()
PYEOF
```

### Step 5: Check for Rootkits and Modified Binaries

```bash
# Check for known rootkit indicators
# Compare system binary hashes against known-good
find /mnt/evidence/usr/bin/ /mnt/evidence/usr/sbin/ /mnt/evidence/bin/ /mnt/evidence/sbin/ \
   -type f -executable -exec sha256sum {} \; > /cases/case-2024-001/linux/analysis/binary_hashes.txt

# Check for SUID/SGID binaries (potential privilege escalation)
find /mnt/evidence/ -perm -4000 -type f 2>/dev/null > /cases/case-2024-001/linux/analysis/suid_files.txt
find /mnt/evidence/ -perm -2000 -type f 2>/dev/null > /cases/case-2024-001/linux/analysis/sgid_files.txt

# Check for suspicious files in /tmp and /dev/shm
find /mnt/evidence/tmp/ /mnt/evidence/dev/shm/ -type f 2>/dev/null \
   -exec file {} \; > /cases/case-2024-001/linux/analysis/tmp_files.txt

# Check for hidden files and directories
find /mnt/evidence/ -name ".*" -not -path "*/\." -type f 2>/dev/null | \
   head -100 > /cases/case-2024-001/linux/analysis/hidden_files.txt

# Check kernel modules
ls -la /mnt/evidence/libs/modules/$(ls /mnt/evidence/libs/modules/ | head -1)/extra/ 2>/dev/null \
   > /cases/case-2024-001/linux/analysis/extra_modules.txt

# Check for modified PAM configuration (authentication backdoors)
diff /mnt/evidence/etc/pam.d/ /cases/baseline/pam.d/ 2>/dev/null \
   > /cases/case-2024-001/linux/analysis/pam_changes.txt
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| /var/log/auth.log | Primary authentication log on Debian/Ubuntu systems |
| /var/log/secure | Primary authentication log on RHEL/CentOS systems |
| wtmp/btmp | Binary logs recording successful and failed login sessions |
| .bash_history | User command history file (can be cleared by attackers) |
| crontab | Scheduled task system commonly used for persistence |
| authorized_keys | SSH public keys granting passwordless access to an account |
| SUID bit | File permission allowing execution as the file owner (privilege escalation vector) |
| LD_PRELOAD | Environment variable that loads a shared library before all others (hooking technique) |

## Tools & Systems

| Tool | Purpose |
|------|---------|
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