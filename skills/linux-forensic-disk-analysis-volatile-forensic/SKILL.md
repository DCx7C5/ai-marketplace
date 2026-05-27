---
name: linux-forensic-disk-analysis-volatile-forensic
description: - Security incident confirmed and compromised host identified - Before system isolation, shutdown, or remediation begins - Memory-resident malware suspected (fileless attacks) - Need to capture network connections, running processes, and system state - Legal proceedings may require forensic evidence preservation - Incident requires root cause analy
domain: cybersecurity
---
------|-------------|
| Order of Volatility | RFC 3227 - Collect most volatile data first: registers > cache > memory > disk |
| Live Forensics | Collecting evidence from a running system before shutdown |
| Chain of Custody | Documentation tracking evidence handling from collection to court |
| Forensic Soundness | Ensuring evidence collection doesn't alter the original evidence |
| Trusted Tools | Using verified tools from external media, not from the compromised system |
| Evidence Integrity | SHA256 hashing of all evidence immediately after collection |
| Locard's Exchange Principle | Every contact leaves a trace - minimize investigator artifacts |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| WinPmem | Windows memory acquisition |
| LiME (Linux Memory Extractor) | Linux kernel memory acquisition |
| Sysinternals Suite | Process, handle, and DLL analysis (Windows) |
| Velociraptor | Remote forensic collection at scale |
| KAPE (Kroll Artifact Parser) | Automated artifact collection on Windows |
| CyLR | Cross-platform live response collection |
| GRR Rapid Response | Remote live forensics framework |

## Common Scenarios

1. **Fileless Malware Attack**: PowerShell-based attack with no files on disk. Memory dump is critical evidence containing the malicious scripts.
2. **Active C2 Session**: Attacker has live connection. Network connections and process data reveal C2 infrastructure.
3. **Insider Data Theft**: Employee copying files. Process list, mapped drives, and network connections show exfiltration activity.
4. **Compromised Web Server**: Web shell detected. Memory may contain additional backdoors not yet written to disk.
5. **Lateral Movement in Progress**: Attacker moving between systems. Authentication tokens and network sessions in memory reveal scope.

## Output Format
- Memory dump file (.raw or .lime format) with SHA256 hash
- Network state captures (connections, ARP, DNS, routes)
- Process listings with command lines and parent processes
- User session and authentication data
- System configuration snapshots
- Evidence manifest with SHA256 checksums
- Chain of custody documentation