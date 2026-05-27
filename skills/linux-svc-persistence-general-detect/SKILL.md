---
name: linux-svc-persistence-general-detect
description: "7. Always cross-validate with @kernel-analyst for LKM/eBPF findings 8."
domain: cybersecurity
---

## Rules for Agents

1. Always load PersistenceBaseline at start — ALL deltas = at least **MEDIUM**
2. /etc/ld.so.preload exists = **CRITICAL** — escalate immediately
3. New kernel module not in baseline = **HIGH**
4. eBPF pinned to /sys/fs/bpf = **HIGH** — dump and analyse
5. Unauthorized SSH authorized_keys = **HIGH**
6. Log every persistence mechanism with path, owner, creation date, and content hash to `iocs.md`
7. Always cross-validate with @kernel-analyst for LKM/eBPF findings
8. Sync all persistence IOCs to shared memory at session end
