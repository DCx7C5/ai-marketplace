---
name: linux-net-docker-socket-expose-detect
description: "subdomain: container-security tags: - linux - docker - socket - expose - root-escape - detect nist_csf: - DE."
domain: cybersecurity
---

subdomain: container-security
tags:
- linux
- docker
- socket
- expose
- root-escape
- detect
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1611
- T1190
capec: []
