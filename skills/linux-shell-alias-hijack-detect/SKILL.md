---
name: linux-shell-alias-hijack-detect
description: "subdomain: persistence-detection tags: - linux - shell - alias - hijack - rootkit nist_csf: - DE."
domain: cybersecurity
---

subdomain: persistence-detection
tags:
- linux
- shell
- alias
- hijack
- rootkit
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1574
- T1036
capec: []
