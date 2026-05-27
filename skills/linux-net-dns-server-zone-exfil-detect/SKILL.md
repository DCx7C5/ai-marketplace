---
name: linux-net-dns-server-zone-exfil-detect
description: "subdomain: network-security tags: - linux - dns - bind - zone-transfer - exfil - detect nist_csf: - DE."
domain: cybersecurity
---

subdomain: network-security
tags:
- linux
- dns
- bind
- zone-transfer
- exfil
- detect
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1048
- T1590.002
capec: []
