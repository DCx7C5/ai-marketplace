---
name: linux-proc-signal-handler-hijack-detect
description: "subdomain: process-forensics tags: - linux - signal - handler - hijack - persistence nist_csf: - DE."
domain: cybersecurity
---

subdomain: process-forensics
tags:
- linux
- signal
- handler
- hijack
- persistence
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1055
- T1543
capec: []
