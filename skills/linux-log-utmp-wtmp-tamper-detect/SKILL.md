---
name: linux-log-utmp-wtmp-tamper-detect
description: "subdomain: logging-forensics tags: - linux - utmp - wtmp - login - tamper - anti-forensics nist_csf: - DE."
domain: cybersecurity
---

subdomain: logging-forensics
tags:
- linux
- utmp
- wtmp
- login
- tamper
- anti-forensics
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1070.006
capec: []
