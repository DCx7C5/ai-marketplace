---
name: linux-proc-ipc-named-pipe-detect
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect named pipe impersonation abuse where a privileged service connects to an attacker-controlled pipe enabling token theft and privilege escalation.
subdomain: process-forensics
tags:
  - named-pipe
  - pipe-impersonation
  - token-theft
  - privilege-escalation
  - windows-ipc
nist_csf:
  - DE.CM-04
mitre:
  - T1134.001
  - T1134
cwe:
  - CWE-269
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
