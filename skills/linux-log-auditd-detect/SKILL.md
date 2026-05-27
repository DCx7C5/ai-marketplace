---
name: linux-log-auditd-detect
description: "| | **auditd** | The Linux Audit daemon that receives audit events from the kernel and writes them to `/var/log/audit/audit."
domain: cybersecurity
---

|
| **auditd** | The Linux Audit daemon that receives audit events from the kernel and writes them to `/var/log/audit/audit.log` |
| **auditctl** | Command-line utility to control the audit system: add/remove rules, check status, set backlog size |
| **ausearch** | Query tool that searches audit logs by message type, user, file, key, time range, or event ID |
| **aureport** | Reporting tool that generates aggregate summaries of audit events for triage and compliance |
| **audit rule key (-k)** | A user-defined label attached to an audit rule, enabling fast filtering of related events with ausearch and aureport |
| **syscall auditing** | Kernel-level monitoring of system calls (execve, open, connect, ptrace) that captures process and file activity |
| **augenrules** | Utility that merges all files in `/etc/audit/rules.d/` into `/etc/audit/audit.rules` and loads them into the kernel |

## Verification

- [ ] auditd is running and rules are loaded (`auditctl -l` returns expected rule count)
- [ ] No audit backlog overflow (`auditctl -s` shows `backlog: 0` or low value, lost: 0)
- [ ] ausearch returns events for each custom key (`ausearch -k <key> -ts today` returns results)
- [ ] aureport generates non-empty summaries for authentication, executable, and file events
- [ ] Timeline reconstruction produces a coherent chronological sequence of attacker actions
- [ ] Critical file watches trigger alerts on test modifications (`touch /etc/shadow` generates an event)
- [ ] Logs are forwarding to central SIEM (verify with a test event and confirm receipt)
- [ ] Audit rules persist across reboot (rules in `/etc/audit/rules.d/`, not only via `auditctl`)
