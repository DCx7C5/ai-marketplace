---
name: linux-kernel-syscall-audit-monitor
description: "| | `identity_change` | T1003.008 — /etc/passwd and /etc/shadow | | `module_load` | T1547."
domain: cybersecurity
---

|
| `identity_change` | T1003.008 — /etc/passwd and /etc/shadow |
| `module_load` | T1547.006 — Kernel Modules and Extensions |
| `process_injection` | T1055 — Process Injection |
| `cron_persistence` | T1053.003 — Cron |
| `privesc` | T1068 — Exploitation for Privilege Escalation |

## IOC Indicators

- Audit daemon stopped unexpectedly → T1562.012 (Disable Security Tools)
- Rules cleared (`auditctl -D`) without admin action → Active evasion
- `NETFILTER_CFG` events without change management → Firewall tampering
