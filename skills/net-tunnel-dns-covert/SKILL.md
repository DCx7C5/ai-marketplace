---
name: net-tunnel-dns-covert
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect DNS tunnelling C2 channels by analysing query frequency, subdomain length entropy, TXT/NULL record abuse, and comparing against authoritative DNS baseline.
subdomain: network-security
tags:
  - dns-tunnel
  - c2
  - exfiltration
  - iodine
  - dnscat2
  - entropy
  - dns-anomaly
nist_csf:
  - DE.CM-01
  - DE.AE-02
mitre:
  - T1071.004
  - T1048.003
cwe:
  - CWE-200
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
