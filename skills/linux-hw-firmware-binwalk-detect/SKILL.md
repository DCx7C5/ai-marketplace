---
name: linux-hw-firmware-binwalk-detect
description: - Analyzing IoT device firmware downloaded from vendor sites or extracted from flash chips - Reverse engineering router, camera, or embedded device firmware for vulnerability research - Identifying embedded filesystems (SquashFS, CramFS, JFFS2, UBIFS) within firmware blobs - Detecting encrypted or compressed regions using entropy analysis - Extract
domain: cybersecurity
---
---|------------|
| **Firmware** | Software embedded in hardware devices providing low-level control; typically contains a bootloader, kernel, root filesystem, and configuration data |
| **Entropy Analysis** | Statistical measurement of randomness in binary data; high entropy indicates encryption or compression, low entropy indicates plaintext or structured data |
| **SquashFS** | Read-only compressed filesystem commonly used in embedded Linux devices; supports LZMA, gzip, LZO, and zstd compression |
| **Magic Bytes** | Known byte sequences at fixed offsets that identify file types; binwalk uses a database of magic signatures to detect embedded files |
| **Matryoshka Extraction** | Recursive extraction mode where binwalk re-scans extracted files for additional embedded content, handling deeply nested archives |
| **CramFS** | Compressed ROM filesystem designed for embedded systems with limited flash storage; supports only zlib compression |
| **JFFS2** | Journalling Flash File System version 2, designed for NOR and NAND flash memory in embedded devices |

## Tools & Systems

- **binwalk**: Primary firmware analysis tool for signature scanning, entropy analysis, and automated extraction of embedded files
- **unsquashfs**: SquashFS extraction utility for mounting read-only compressed filesystems found in router and IoT firmware
- **jefferson**: Python tool for extracting JFFS2 flash filesystem images commonly found in embedded devices
- **sasquatch**: Patched SquashFS utility supporting non-standard vendor-modified SquashFS variants
- **firmware-mod-kit**: Toolkit for extracting, modifying, and repacking firmware images for security testing

## Common Scenarios

### Scenario: Extracting and Auditing Router Firmware for Hardcoded Credentials

**Context**: A security researcher is performing an authorized assessment of a consumer router. The firmware update file was downloaded from the vendor's support page. The goal is to identify hardcoded credentials, insecure default configurations, and known vulnerable components.

**Approach**:
1. Run `binwalk -e firmware.bin` to perform initial extraction
2. Use `binwalk -E firmware.bin` to check entropy and identify encrypted regions
3. Locate the SquashFS root filesystem in the extracted output
4. Mount with `unsquashfs` and inspect `/etc/passwd`, `/etc/shadow`, and web server configs
5. Search for hardcoded credentials with `grep -rni "password" /tmp/root/etc/`
6. Identify service versions and cross-reference with CVE databases
7. Check for debug interfaces (telnet, UART, JTAG references) in startup scripts
8. Examine web application code for authentication bypass or command injection

**Pitfalls**:
- Some vendors use non-standard SquashFS with custom compression; use sasquatch instead of unsquashfs
- Encrypted firmware requires decryption keys often found in bootloader or previous unencrypted versions
- Firmware headers may need to be stripped before binwalk can identify the embedded filesystem
- Obfuscated strings may evade simple grep searches; use entropy analysis to locate data blobs

## Output Format

```
FIRMWARE EXTRACTION REPORT
====================================
Firmware:         TP-Link TL-WR841N v14
File:             wr841nv14_en_3_16_9_up.bin
Size:             3,932,160 bytes (3.75 MB)
SHA-256:          a1b2c3d4e5f6...

SIGNATURE SCAN RESULTS
Offset       Type                          Size
------       ----                          ----
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