---
name: linux-forensic-mem-analysis-volcombined-detect
description: - An endpoint has been contained during an active incident and volatile evidence must be preserved - EDR alerts suggest process injection or fileless malware that only exists in memory - Encryption keys need to be recovered from a ransomware-infected system before shutdown - Credential theft (Mimikatz, LSASS dumping) is suspected and evidence must 
domain: cybersecurity
---
---|------------|
| **Volatile Evidence** | Data that exists only in RAM and is lost when a system is powered off; includes running processes, network connections, encryption keys |
| **Process Injection** | Technique where malware inserts code into a legitimate process's memory space to evade detection (malfind detects this) |
| **EPROCESS** | Windows kernel data structure representing a process; psscan searches for these structures even when unlinked from the active process list |
| **VAD (Virtual Address Descriptor)** | Windows kernel structure tracking memory regions allocated to a process; malfind examines VADs for executable but non-file-backed regions |
| **Symbol Tables** | OS-specific data structures that Volatility 3 uses to parse memory; downloaded automatically based on detected OS version |
| **PAGE_EXECUTE_READWRITE** | Memory protection flag indicating a region is readable, writable, and executable; common indicator of injected malicious code |
| **Memory-Resident Malware** | Malware that operates entirely in RAM without writing persistent files to disk, making it invisible to traditional disk-based antivirus |

## Tools & Systems

- **Volatility 3**: Primary open-source memory forensics framework; Python 3 rewrite with automatic symbol resolution
- **WinPmem / DumpIt / Magnet RAM Capture**: Memory acquisition tools for Windows systems
- **AVML (Acquire Volatile Memory for Linux)**: Microsoft's open-source Linux memory acquisition tool
- **YARA**: Pattern matching engine for scanning memory dumps against malware signatures and behavioral rules
- **MemProcFS**: Memory analysis tool that presents memory as a virtual file system for intuitive browsing

## Common Scenarios

### Scenario: Detecting Cobalt Strike Beacon in Memory

**Context**: EDR detects suspicious named pipe activity but cannot identify the source. A memory dump is acquired from the suspect endpoint for analysis.

**Approach**:
1. Run `windows.pstree` to identify the process hierarchy and spot abnormal parent-child relationships
2. Run `windows.malfind` to detect injected code regions, particularly in `svchost.exe` or `rundll32.exe`
3. Dump the injected memory region and scan with YARA rules for Cobalt Strike beacon signatures
4. Run `windows.netscan` to identify C2 connections and correlate with the injected process PID
5. Extract the beacon configuration (C2 URLs, sleep time, jitter, watermark) using CobaltStrikeParser
6. Run `windows.cmdline` to identify any post-exploitation commands executed

**Pitfalls**:
- Analyzing only the process list without running malfind (missing injected code in legitimate processes)
- Not capturing memory before isolating the endpoint (EDR containment may trigger malware self-deletion)
- Using Volatility 2 profiles instead of Volatility 3 automatic symbol resolution on newer Windows versions

## Output Format

```
MEMORY FORENSICS ANALYSIS REPORT
==================================
Incident:         INC-2025-1547
Evidence File:    WKSTN-042_20251115_1445.raw
SHA-256:          a4b3c2d1e5f6...
OS Identified:    Windows 10 22H2 (Build 19045)
Analysis Tool:    Volatility 3.2.0

PROCESS ANOMALIES
PID    Process         Parent       Anomaly
3847   update.exe      powershell   Suspicious executable in Temp directory
5102   svchost.exe     explorer     Wrong parent (expected services.exe)
---    [hidden]        ---          Found in psscan but not pslist

INJECTED CODE
PID    Process        Address Range        Protection              Finding
5102   svchost.exe    0x00A10000-0x00A14   PAGE_EXECUTE_READWRITE  MZ header (PE injection)

NETWORK CONNECTIONS
PID    Process      Local              Foreign             State
3847   update.exe   10.1.5.42:49721    185.220.101.42:443  ESTABLISHED
5102   svchost.exe  10.1.5.42:51003    91.215.85.17:8443   ESTABLISHED

YARA MATCHES
Rule: CobaltStrike_Beacon_x64
Match PID: 5102 (svchost.exe)
Offset: 0x00A10240

EXTRACTED IOCS
Hashes:     [SHA-256 of dumped injected code]
C2 IPs:     185.220.101.42, 91.215.85.17
C2 Domains: [extracted from beacon config]
Mutexes:    Global\MSCTF.Shared.MUTEX.ZRQ
```