---
name: linux-svc-motd-script-backdoor-detect
description: "subdomain: persistence-detection tags: - linux - motd - update-motd - backdoor - persistence nist_csf: - DE."
domain: cybersecurity
---

subdomain: persistence-detection
tags:
- linux
- motd
- update-motd
- backdoor
- persistence
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1037
- T1543
capec: []
