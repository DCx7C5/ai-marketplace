---
name: linux-hw-firmware-analyze
description: "Linux Hw Firmware Analyze."
domain: cybersecurity
---

|
| **Firmware** | Software permanently stored in device hardware (flash memory, EEPROM) controlling low-level device operations and boot process |
| **UEFI (Unified Extensible Firmware Interface)** | Modern system firmware replacing legacy BIOS; provides boot services, runtime services, and a modular driver architecture |
| **SPI Flash** | Serial Peripheral Interface flash memory chip storing UEFI/BIOS firmware; can be read and modified for persistence |
| **Secure Boot** | UEFI feature verifying digital signatures of boot components to prevent unauthorized code execution during startup |
| **SquashFS** | Read-only compressed filesystem commonly used in embedded Linux firmware for space-efficient storage |
| **Bootkit** | Malware infecting the boot process (MBR, VBR, UEFI) to load before the operating system and evade OS-level security |
| **Firmware Emulation** | Running extracted firmware in a virtual environment (QEMU, firmadyne) to analyze behavior without physical hardware |

## Tools & Systems

- **binwalk**: Firmware analysis tool for scanning, extracting, and analyzing embedded file systems and compressed data in firmware images
- **UEFITool**: Open-source UEFI firmware image parser and extractor for analyzing UEFI volumes, modules, and drivers
- **chipsec**: Intel's open-source framework for platform security assessment including SPI flash, Secure Boot, and UEFI analysis
- **firmadyne**: Automated firmware analysis and emulation platform for Linux-based embedded devices
- **Ghidra**: NSA's reverse engineering tool with ARM, MIPS, and other embedded architecture support for firmware binary analysis

## Common Scenarios

### Scenario: Investigating a Compromised Router with Persistent Backdoor

**Context**: A network router continues to exhibit suspicious behavior (unexpected DNS resolutions, traffic to unknown IPs) even after factory resets. Firmware-level compromise is suspected.

**Approach**:
1. Dump the firmware from the router using JTAG/UART debug interface or vendor management tools
2. Extract the filesystem with binwalk and identify the Linux distribution and kernel version
3. Compare file hashes against known-good firmware image from the vendor
4. Search startup scripts (rcS, inittab, crontab) for backdoor entries
5. Analyze any modified or new binaries with Ghidra (ARM/MIPS architecture)
6. Check for hardcoded credentials, unauthorized SSH keys, and reverse shell scripts
7. Emulate the firmware to observe network behavior and identify C2 communication

**Pitfalls**:
- Not dumping firmware from the actual device (downloading from vendor site gives clean version, not the compromised one)
- Ignoring modified shared libraries (.so files) that may hook system functions
- Missing firmware modifications stored outside the main filesystem (bootloader, configuration partitions)
- Not checking both the primary and backup firmware partitions (some devices have dual-bank flash)

## Output Format

```
FIRMWARE MALWARE ANALYSIS REPORT
===================================
Device:           NetGear R7000 Router
Firmware Version: V1.0.11.116 (modified)
Architecture:     ARM (Little Endian)
Filesystem:       SquashFS (Linux 3.4.103)
Dump Method:      UART debug console

INTEGRITY CHECK
Vendor Firmware Hash:  aaa111bbb222... (clean V1.0.11.116)
Analyzed Firmware Hash: ccc333ddd444... (MISMATCH)
Modified Files:        14 files differ from vendor baseline

BACKDOOR FINDINGS
[!] /usr/bin/httpd_backdoor (new binary, not in vendor firmware)
    Architecture: ARM 32-bit
    Function: Reverse shell to 185.220.101[.]42:4444
    Persistence: Added to /etc/init.d/rcS

[!] /etc/shadow modified
    Root password changed to known hash
    New user 'admin2' added with UID 0

[!] /etc/crontab modified
    Added: */5 * * * * /usr/bin/httpd_backdoor

[!] /root/.ssh/authorized_keys (new file)
    Contains attacker's SSH public key

EXTRACTED IOCs
C2 IP:            185.220.101[.]42
C2 Port:          4444
SSH Key:          ssh-rsa AAAA... attacker@control
Backdoor Hash:    eee555fff666...

REMEDIATION
1. Flash clean vendor firmware via TFTP recovery mode
2. Change all device credentials
3. Update to latest firmware version
4. Enable firmware integrity checking if available
5. Monitor for re-compromise indicators
```
