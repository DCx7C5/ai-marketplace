---
name: linux-hw-firmware-bootkit-detect
description: - A system shows signs of compromise that persist through OS reinstallation - Antivirus and EDR are unable to detect malware despite clear evidence of compromise - UEFI Secure Boot has been disabled or shows integrity violations - Memory forensics reveals rootkit behavior (hidden processes, hooked system calls) - Investigating nation-state level th
domain: cybersecurity
---
---|------------|
| **Bootkit** | Malware that infects the boot process (MBR, VBR, UEFI) to execute before the operating system loads, gaining persistent low-level control |
| **MBR (Master Boot Record)** | First 512 bytes of a disk containing bootstrap code and partition table; MBR bootkits replace this code with malicious loaders |
| **UEFI (Unified Extensible Firmware Interface)** | Modern firmware interface replacing BIOS; UEFI bootkits implant malicious modules in firmware volumes or modify the ESP |
| **Secure Boot** | UEFI security feature verifying digital signatures of boot components; bootkits like BlackLotus exploit vulnerabilities to bypass it |
| **SPI Flash** | Flash memory chip storing UEFI firmware; advanced bootkits like LoJax and MoonBounce modify SPI flash for firmware-level persistence |
| **DKOM (Direct Kernel Object Manipulation)** | Rootkit technique modifying kernel structures to hide processes, files, and network connections without hooking functions |
| **Driver Signature Enforcement (DSE)** | Windows security feature requiring kernel drivers to be digitally signed; bootkits disable DSE during boot to load unsigned rootkit drivers |

## Tools & Systems

- **UEFITool**: Open-source UEFI firmware image editor and parser for inspecting firmware volumes, drivers, and modules
- **chipsec**: Intel hardware security assessment framework for verifying SPI flash protection, Secure Boot, and UEFI configuration
- **Volatility**: Memory forensics framework with SSDT, IDT, callback, and driver analysis plugins for kernel rootkit detection
- **GMER**: Windows rootkit detection tool scanning for SSDT hooks, IDT hooks, hidden processes, and modified kernel modules
- **Bootkits Analyzer**: Specialized tool for analyzing MBR/VBR code including disassembly and comparison against known-good baselines

## Common Scenarios

### Scenario: Investigating Persistent Compromise Surviving OS Reinstallation

**Context**: An organization reimaged a compromised workstation, but the same C2 beaconing resumed within hours. Standard disk forensics finds no malware. UEFI bootkit is suspected.

**Approach**:
1. Boot from a Linux live USB to avoid executing any compromised OS components
2. Dump the SPI flash firmware using chipsec or flashrom for offline analysis
3. Dump the MBR and VBR sectors with dd for boot sector analysis
4. Copy the EFI System Partition for bootloader integrity verification
5. Open the SPI dump in UEFITool and compare module GUIDs against vendor-provided firmware
6. Look for additional or modified DXE drivers that should not be present
7. Analyze any suspicious modules with Ghidra (x86_64 UEFI module format)
8. Verify Secure Boot configuration and check for exploit-based bypasses

**Pitfalls**:
- Analyzing the system while the compromised OS is running (rootkit may hide from live analysis)
- Not checking SPI flash (only analyzing disk-based boot components misses firmware-level implants)
- Assuming Secure Boot prevents all bootkits (known bypasses exist, e.g., CVE-2022-21894)
- Not preserving the original firmware dump before reflashing (critical evidence for attribution)

## Output Format

```
BOOTKIT / ROOTKIT ANALYSIS REPORT
====================================
System:           Dell OptiPlex 7090 (UEFI, TPM 2.0)
Firmware Version: 1.15.0 (Dell)
Secure Boot:      ENABLED (but bypassed)
Capture Method:   Linux Live USB + chipsec SPI dump

MBR/VBR ANALYSIS
MBR Signature:    Valid (0x55AA)
MBR Code:         MATCHES standard Windows 10 MBR (clean)
VBR Code:         MATCHES standard NTFS VBR (clean)

UEFI FIRMWARE ANALYSIS
Total Modules:    287
Vendor Expected:  285
Extra Modules:    2 UNAUTHORIZED
  [!] DXE Driver GUID: {ABCD1234-...} "SmmAccessDxe_mod" (MODIFIED)
      Original Size: 12,288 bytes
      Current Size:  45,056 bytes (32KB ADDED)
      Entropy: 7.82 (HIGH - encrypted payload)

  [!] DXE Driver GUID: {EFGH5678-...} "UefiPayloadDxe" (NEW - not in vendor firmware)
      Size: 28,672 bytes
      Function: Drops persistence agent during boot

BOOT CHAIN INTEGRITY
bootmgfw.efi:     MODIFIED (hash mismatch, Secure Boot bypass via CVE-2022-21894)
winload.efi:      MODIFIED (DSE disabled at load time)
ntoskrnl.exe:     CLEAN (but unsigned driver loaded after boot)

KERNEL ROOTKIT COMPONENTS
Driver:           C:\Windows\System32\drivers\null_mod.sys (unsigned, hidden)
SSDT Hooks:       3 (NtQuerySystemInformation, NtQueryDirectoryFile, NtDeviceIoControlFile)
Hidden Processes: 2 (PID 6784: beacon.exe, PID 6812: keylog.exe)
Hidden Files:     C:\Windows\System32\drivers\null_mod.sys

ATTRIBUTION
Family:           BlackLotus variant
Confidence:       HIGH (CVE-2022-21894 exploit, ESP modification pattern matches)

REMEDIATION
1. Reflash SPI firmware with clean vendor image via hardware programmer
2. Rebuild EFI System Partition from clean Windows installation media
3. Reinstall OS from verified media
4. Enable all firmware write protections
5. Update firmware to latest version (patches CVE-2022-21894)
```