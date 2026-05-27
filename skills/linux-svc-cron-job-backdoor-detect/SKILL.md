---
name: linux-svc-cron-job-backdoor-detect
description: "subdomain: persistence-detection tags: - linux - cron - crontab - backdoor - persistence nist_csf: - DE."
domain: cybersecurity
---

subdomain: persistence-detection
tags:
- linux
- cron
- crontab
- backdoor
- persistence
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1053.003
capec: []
