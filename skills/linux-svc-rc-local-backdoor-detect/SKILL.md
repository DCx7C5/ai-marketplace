---
name: linux-svc-rc-local-backdoor-detect
description: "subdomain: persistence-detection tags: - linux - rc-local - sysv - init - backdoor - persistence nist_csf: - DE."
domain: cybersecurity
---

subdomain: persistence-detection
tags:
- linux
- rc-local
- sysv
- init
- backdoor
- persistence
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1037.004
capec: []
