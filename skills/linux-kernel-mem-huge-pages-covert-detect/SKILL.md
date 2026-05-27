---
name: linux-kernel-mem-huge-pages-covert-detect
description: "subdomain: kernel-security tags: - linux - huge-pages - side-channel - aslr - covert nist_csf: - DE."
domain: cybersecurity
---

subdomain: kernel-security
tags:
- linux
- huge-pages
- side-channel
- aslr
- covert
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1068
capec: []
