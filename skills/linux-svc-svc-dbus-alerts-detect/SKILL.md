---
name: linux-svc-svc-dbus-alerts-detect
description: "5. Cross-correlate D-Bus alerts with authentication log timestamps 6."
domain: cybersecurity
---

## Rules for Agents

1. Flag any polkit `allow_any = yes` rule for unprivileged access as **HIGH**
2. Log all unknown well-known D-Bus names to `iocs.md`
3. Alert on pkexec calls outside normal admin workflows
4. Check DBUS_SESSION_BUS_ADDRESS in all process environments — unexpected paths are **MEDIUM**
5. Cross-correlate D-Bus alerts with authentication log timestamps
6. Sync all D-Bus IOCs to shared memory at session end
