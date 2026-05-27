---
name: net-security-monitoring
description: "6. Log all remote IPs, listening ports, and anomalous routes to `iocs."
domain: cybersecurity
---

## Rules for Agents

1. Always correlate all remote IPs against `ioc-db.md` before proceeding
2. Any connection to IOC-listed IP = **HIGH** minimum, escalate to CYBERSEC-AGENT
3. Unexpected listeners on ports < 1024 = **HIGH**
4. ARP cache with duplicate IPs = **MEDIUM+** MITM indicator
5. Tunnel interfaces not in NetworkBaseline = **HIGH**
6. Log all remote IPs, listening ports, and anomalous routes to `iocs.md`
7. Sync all network IOCs to shared memory at session end
