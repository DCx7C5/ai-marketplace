---
name: linux-hw-firmware-binwalk-detect
description: "- 0x00000000   U-Boot bootloader header      64 bytes 0x00020000   LZMA compressed data          1,048,576 bytes 0x00120000   SquashFS filesystem v4."
domain: cybersecurity
---

-
0x00000000   U-Boot bootloader header      64 bytes
0x00020000   LZMA compressed data          1,048,576 bytes
0x00120000   SquashFS filesystem v4.0      2,752,512 bytes
0x003B0000   Configuration partition       131,072 bytes

ENTROPY ANALYSIS
Region 0x000000-0x020000: 4.21 (bootloader - plaintext code)
Region 0x020000-0x120000: 7.89 (kernel - LZMA compressed)
Region 0x120000-0x3B0000: 7.45 (filesystem - SquashFS compressed)
Region 0x3B0000-0x3C0000: 1.12 (config - mostly empty)

EXTRACTED FILESYSTEM
Root filesystem: SquashFS v4.0, LZMA compression
Total files: 847
Total dirs: 112
BusyBox version: 1.19.4

SECURITY FINDINGS
[CRITICAL] Hardcoded root password in /etc/shadow (hash: $1$...)
[HIGH]     Telnet daemon enabled by default in /etc/init.d/rcS
[HIGH]     Private RSA key at /etc/ssl/private/server.key
[MEDIUM]   BusyBox 1.19.4 (CVE-2021-42373, CVE-2021-42374)
[MEDIUM]   Dropbear SSH 2014.63 (CVE-2016-3116)
[LOW]      UPnP service enabled by default
```
