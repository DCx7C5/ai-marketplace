---
name: linux-proc-proc-mem-inject-detect
description: "subdomain: process-security tags: - linux - proc - mem - injection - ptrace nist_csf: - DE."
domain: cybersecurity
---

subdomain: process-security
tags:
- linux
- proc
- mem
- injection
- ptrace
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1055
- T1083
capec: []
