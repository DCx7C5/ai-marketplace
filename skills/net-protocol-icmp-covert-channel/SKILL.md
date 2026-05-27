---
name: net-protocol-icmp-covert-channel
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect ICMP covert channel C2 communication by analysing ICMP payload entropy, packet size distribution, timing patterns, and comparing against legitimate ping baselines.
subdomain: network-protocol-analysis
tags:
  - icmp-tunnel
  - covert-channel
  - c2
  - exfiltration
  - ptunnel
  - icmptunnel
nist_csf:
  - DE.CM-01
  - DE.AE-02
mitre:
  - T1095
  - T1071.004
cwe:
  - CWE-200
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
