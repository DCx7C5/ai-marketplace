---
name: linux-shell-profile-backdoor-detect
description: "subdomain: persistence-detection tags: - linux - shell - bashrc - profile - backdoor - persistence nist_csf: - DE."
domain: cybersecurity
---

subdomain: persistence-detection
tags:
- linux
- shell
- bashrc
- profile
- backdoor
- persistence
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1546.004
capec: []
