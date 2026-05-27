---
name: windows-processes-hollow-technique
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect process hollowing (RunPE) by identifying processes with mismatched image paths between PEB and VAD tree, or unmapped PE headers in memory.
subdomain: process-forensics
tags:
  - process-hollow
  - runpe
  - peb
  - vad
  - pe-header
  - memory-forensics
nist_csf:
  - DE.CM-04
  - DE.AE-02
mitre:
  - T1055.012
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
