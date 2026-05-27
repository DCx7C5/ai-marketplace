---
name: linux-mem-heap-use-after-free-detect
description: "subdomain: memory-security tags: - linux - heap - use-after-free - uaf - memory-corruption nist_csf: - DE."
domain: cybersecurity
---

subdomain: memory-security
tags:
- linux
- heap
- use-after-free
- uaf
- memory-corruption
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1068
capec: []
