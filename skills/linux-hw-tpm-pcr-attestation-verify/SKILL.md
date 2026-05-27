---
name: linux-hw-tpm-pcr-attestation-verify
description: Verify TPM PCR values and perform remote attestation to confirm system boot integrity — detect PCR tampering indicating bootkit or firmware compromise.
domain: cybersecurity
subdomain: hardware-security
tags:
- linux
- tpm
- pcr
- attestation
- secure-boot
nist_csf:
- PR.DS-06
- ID.RA-05
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1542.001
capec: []
