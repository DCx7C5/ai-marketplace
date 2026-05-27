---
name: linux-hw-firmware-detect
description: "6. Always baseline PCR values and UEFI boot entries at session start 7."
domain: cybersecurity
---

## Rules for Agents

1. TPM PCR value changes vs baseline = **CRITICAL** — escalate to CYBERSEC-AGENT immediately
2. Rogue UEFI boot entry not in baseline = **CRITICAL**
3. Unexpected MOK enrolled key = **HIGH**
4. initramfs with network tools (curl/wget/nc) = **HIGH**
5. Unauthorized firmware downgrade in fwupd history = **HIGH**
6. Always baseline PCR values and UEFI boot entries at session start
7. Sync all firmware IOCs to shared memory at session end
