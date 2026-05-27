---
name: linux-proc-zombie-orphan-detect
description: "See [SKILL taxonomy](../../TAXONOMY.md) for more details."
domain: cybersecurity
---

## Overview

Detect zombie and orphan processes indicating crashed services, fork bombs, or malware that intentionally creates orphans to evade parent-process correlation.
subdomain: process-forensics
tags:
  - zombie-process
  - orphan
  - fork-bomb
  - process-lifecycle
  - linux
nist_csf:
  - DE.CM-04
  - DE.AE-02
mitre:
  - T1014
capec: []

## Reference

See [SKILL taxonomy](../../TAXONOMY.md) for more details.
