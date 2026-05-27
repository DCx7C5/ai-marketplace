---
name: linux-kernel-cgroups-v2-forensic
description: Control Groups (cgroups) manage resource allocation for process groups. Attackers exploit cgroup release agents for container escapes (CVE-2022-0492) and abuse cgroup namespaces to persist or evade detection. This skill covers forensic inspection of the unified cgroup v2 hierarchy.
domain: cybersecurity
---
|---|
| `release_agent` with script payload | T1611 — Escape to Host |
| Process bypassing cgroup limits | T1055 — Process Injection |
| Service registered in cgroup without systemd unit | T1543.002 — Systemd Service |