---
name: net-protocol-tcp-session-hijack
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect TCP session hijacking by identifying sequence number anomalies, RST injection events, and unexpected window size changes through packet capture analysis.
subdomain: network-protocol-analysis
tags:
  - tcp-hijack
  - session-hijack
  - sequence-number
  - pcap
  - scapy
  - wireshark
nist_csf:
  - DE.CM-01
  - DE.AE-02
mitre:
  - T1557
cwe:
  - CWE-940
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
