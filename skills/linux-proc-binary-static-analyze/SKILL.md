---
name: linux-proc-binary-static-analyze
description: - A Linux server or container has been compromised and suspicious ELF binaries are found - Analyzing Linux botnets (Mirai, Gafgyt, XorDDoS), cryptominers, or ransomware - Investigating malware targeting cloud infrastructure, Docker containers, or Kubernetes pods - Reverse engineering Linux rootkits and kernel modules - Analyzing cross-platform malw
domain: cybersecurity
---
---|------------|
| **ELF (Executable and Linkable Format)** | Standard binary format for Linux executables, shared libraries, and core dumps containing headers, sections, and segments |
| **Stripped Binary** | ELF binary with debug symbols removed, making reverse engineering more difficult as function names are lost |
| **LD_PRELOAD** | Linux environment variable specifying shared libraries to load before all others; abused by rootkits to intercept system library calls |
| **strace** | Linux system call tracer that logs all system calls and signals made by a process, revealing file, network, and process operations |
| **GOT/PLT** | Global Offset Table and Procedure Linkage Table; ELF structures for dynamic linking that can be hijacked for function hooking |
| **Statically Linked** | Binary compiled with all library code included; common in IoT malware to run on systems without matching shared libraries |
| **Mirai** | Prolific Linux botnet targeting IoT devices via telnet brute-force; source code leaked, leading to many variants |

## Tools & Systems

- **Ghidra**: NSA reverse engineering tool with full ELF support for x86, x86_64, ARM, MIPS, and other Linux architectures
- **Radare2**: Open-source reverse engineering framework with command-line interface for quick binary analysis and scripting
- **strace**: Linux system call tracing tool for observing binary behavior including file, network, and process operations
- **GDB**: GNU Debugger for setting breakpoints, examining memory, and stepping through Linux binary execution
- **pyelftools**: Python library for parsing ELF files programmatically for automated analysis pipelines

## Common Scenarios

### Scenario: Analyzing a Cryptominer Found on a Compromised Linux Server

**Context**: A cloud server shows 100% CPU usage. Investigation reveals an unknown binary running from /tmp with a suspicious name. The binary needs analysis to confirm it is a cryptominer and identify the attacker's wallet and pool.

**Approach**:
1. Copy the binary to an analysis VM and compute SHA-256 hash
2. Run `file` and `readelf` to identify architecture and linking type
3. Extract strings and search for mining pool addresses (stratum+tcp://) and wallet addresses
4. Run with strace in a sandbox to observe network connections (mining pool connection)
5. Import into Ghidra to identify the mining algorithm and configuration extraction
6. Check for persistence mechanisms (crontab, systemd service, SSH keys)
7. Document all IOCs including pool address, wallet, C2 for updates, and persistence artifacts

**Pitfalls**:
- Running `ldd` on malware outside a sandbox (ldd can execute code in the binary)
- Not checking for ARM/MIPS architecture before attempting x86_64 execution
- Missing companion scripts (.sh files) that may handle persistence and cleanup
- Ignoring the initial access vector (how the miner was deployed: SSH brute force, web exploit, container escape)

## Output Format

```
LINUX ELF MALWARE ANALYSIS REPORT
====================================
File:             /tmp/.X11-unix/.rsync
SHA-256:          e3b0c44298fc1c149afbf4c8996fb924...
Type:             ELF 64-bit LSB executable, x86-64
Linking:          Statically linked (all libraries embedded)
Stripped:         Yes
Size:             2,847,232 bytes
Packer:           UPX 3.96 (unpacked for analysis)

CLASSIFICATION
Family:           XMRig Cryptominer (modified)
Variant:          Custom build with C2 update mechanism

FUNCTIONALITY
[*] XMR (Monero) mining via RandomX algorithm
[*] Stratum pool connection for work submission
[*] C2 check-in for configuration updates
[*] Process name masquerading (argv[0] = "[kworker/0:0]")
[*] Competitor process killing (kills other miners)
[*] SSH key injection for re-access

NETWORK INDICATORS
Mining Pool:      stratum+tcp://pool.minexmr[.]com:4444
C2 Server:        hxxp://update.malicious[.]com/config
Wallet:           49jZ5Q3b...Monero_Wallet_Address...

PERSISTENCE
[1] Crontab entry: */5 * * * * /tmp/.X11-unix/.rsync
[2] SSH key added to /root/.ssh/authorized_keys
[3] Systemd service: /etc/systemd/system/rsync-daemon.service
[4] Modified /etc/ld.so.preload for process hiding

PROCESS HIDING
LD_PRELOAD:       /usr/lib/.libsystem.so
Hook:             readdir() to hide /tmp/.X11-unix/.rsync from ls
Hook:             fopen() to hide from /proc/*/maps reading
```