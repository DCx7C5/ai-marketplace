---
name: linux-id-ssh-authorized-keys-backdoor-detect
description: "subdomain: identity-forensics tags: - linux - ssh - authorized-keys - backdoor - persistence nist_csf: - DE."
domain: cybersecurity
---

subdomain: identity-forensics
tags:
- linux
- ssh
- authorized-keys
- backdoor
- persistence
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1098.004
- T1021.004
capec: []
