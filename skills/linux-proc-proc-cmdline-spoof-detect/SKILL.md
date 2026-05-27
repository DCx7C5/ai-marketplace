---
name: linux-proc-proc-cmdline-spoof-detect
description: "subdomain: process-forensics tags: - linux - proc - cmdline - spoof - masquerade nist_csf: - DE."
domain: cybersecurity
---

subdomain: process-forensics
tags:
- linux
- proc
- cmdline
- spoof
- masquerade
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1036.005
capec: []
