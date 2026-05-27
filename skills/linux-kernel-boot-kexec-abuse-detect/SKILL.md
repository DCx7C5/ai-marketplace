---
name: linux-kernel-boot-kexec-abuse-detect
description: "subdomain: kernel-forensics tags: - linux - kexec - kernel - bypass - secure-boot nist_csf: - DE."
domain: cybersecurity
---

subdomain: kernel-forensics
tags:
- linux
- kexec
- kernel
- bypass
- secure-boot
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1542
- T1068
capec: []
