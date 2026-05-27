---
name: linux-svc-systemd-timer-persist-detect
description: "subdomain: persistence-detection tags: - linux - systemd - timer - cron - persistence nist_csf: - DE."
domain: cybersecurity
---

subdomain: persistence-detection
tags:
- linux
- systemd
- timer
- cron
- persistence
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1053.006
capec: []
