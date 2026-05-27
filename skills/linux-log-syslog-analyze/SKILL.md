---
name: linux-log-syslog-analyze
description: "6. Output timeline format: `ISO_TIMESTAMP | SOURCE | EVENT_TYPE | DETAILS | SEVERITY` 7."
domain: cybersecurity
---

## Rules for Agents

1. Always report log tampering (mtime mismatch) as **HIGH** — preserve original
2. SSH brute-force from single IP (>10 failures) = **MEDIUM** minimum
3. Successful login following brute-force = **CRITICAL**
4. New cron jobs or systemd timers not in PersistenceBaseline = **HIGH**
5. Web server path traversal attempts = **MEDIUM** — correlate with process tree
6. Output timeline format: `ISO_TIMESTAMP | SOURCE | EVENT_TYPE | DETAILS | SEVERITY`
7. Sync reconstructed attacker timeline to shared memory at session end
