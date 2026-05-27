---
name: soc-forensics-investigation
description: "5. Never delete suspicious files — preserve with `cp --preserve=all` 6."
domain: cybersecurity
---

## Rules for Agents

1. Always compare against stored FilesystemBaseline — changes without known updates = **MEDIUM+**
2. SUID binaries not in baseline = **HIGH** immediately
3. Executables in `/tmp`, `/dev/shm`, `/run` = **HIGH** unless explicitly whitelisted
4. Log all anomalous files with SHA-256 hash, path, permissions, and owner to `iocs.md`
5. Never delete suspicious files — preserve with `cp --preserve=all`
6. Sync all filesystem IOCs to shared memory at session end
