---
name: linux-kernel-id-cap-enum-detect
description: Linux capabilities divide root privileges into discrete units (e.g., `CAP_NET_ADMIN`, `CAP_SYS_PTRACE`). Attackers abuse misconfigured capabilities to escalate privileges without needing SUID binaries or full root access. This skill covers enumeration, audit, and detection of capability abuse.
domain: cybersecurity
---
|---|
| `CAP_SYS_PTRACE` | Inject shellcode into any process (T1055) |
| `CAP_SYS_ADMIN` | Mount namespaces, bypass seccomp, write cgroups |
| `CAP_NET_RAW` | Raw socket sniffing, ARP poisoning |
| `CAP_DAC_OVERRIDE` | Read/write any file regardless of permissions |
| `CAP_SETUID` | Change UID to 0 (full root escalation) |
| `CAP_CHOWN` | Change ownership of any file |
| `cap_sys_module` | Load kernel modules (rootkit installation) |

### Check for Capability Abuse Vectors
```bash
# Find SUID + capability combinations
find / -perm -4000 -o -perm -2000 2>/dev/null | xargs getcap 2>/dev/null

# Python with cap_setuid
python3 -c "import os; os.setuid(0); os.system('/bin/bash')"

# Check ambient capabilities in containers
grep CapAmb /proc/1/status
```

### Remove Dangerous Capabilities
```bash
# Remove all capabilities from a binary
setcap -r /usr/bin/python3

# Remove specific cap
setcap cap_net_raw-eip /usr/bin/ping
```

## Forensic Detection Workflow

1. Run `getcap -r /` and baseline legitimate capabilities
2. Compare against known-good: `diff baseline_caps.txt current_caps.txt`
3. Run `pscap -a` — look for user processes with `cap_sys_admin` or `cap_setuid`
4. Check container spawned processes: `cat /proc/1/status | grep Cap`
5. Correlate with `auditd` events for `setcap` system calls

## MITRE ATT&CK Mapping

| Finding | Technique |
|---|---|
| Binary with `cap_setuid+ep` | T1548.001 — Setuid and Setgid |
| Process with `cap_sys_ptrace` injecting shellcode | T1055 — Process Injection |
| Container with `cap_sys_admin` escaping namespace | T1611 — Escape to Host |