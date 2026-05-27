---
name: windows-artifact-forensics
description: "-|"
domain: cybersecurity
---
-|
| MFTECmd | $MFT | Root of NTFS volume |
| MFTECmd | $J (USN Journal) | $Extend\$UsnJrnl:$J |
| PECmd | Prefetch files | C:\Windows\Prefetch\*.pf |
| RECmd | NTUSER.DAT | C:\Users\{user}\NTUSER.DAT |
| RECmd | SYSTEM hive | C:\Windows\System32\config\SYSTEM |
| RECmd | SAM hive | C:\Windows\System32\config\SAM |
| RECmd | SOFTWARE hive | C:\Windows\System32\config\SOFTWARE |
| EvtxECmd | Event logs | C:\Windows\System32\winevt\Logs\*.evtx |
| LECmd | LNK files | C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Recent\ |
| JLECmd | Jump lists | C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\ |
| SBECmd | Shellbags | NTUSER.DAT and UsrClass.dat registry hives |

## Common Investigation Scenarios

### Malware Execution Evidence
1. Parse Prefetch with PECmd to identify executed binaries
2. Cross-reference with MFT for file creation timestamps
3. Check Amcache.hve with RECmd for SHA1 hashes of executables
4. Correlate with Event Log entries for process creation (Event ID 4688)

### Data Exfiltration Investigation
1. Parse USN Journal with MFTECmd for file rename/delete operations
2. Analyze LNK files with LECmd for recently accessed documents
3. Review Shellbags with SBECmd for directory browsing activity
4. Check for USB device connections in SYSTEM registry with RECmd

### Lateral Movement Detection
1. Parse Security.evtx with EvtxECmd for logon events (4624, 4625)
2. Analyze RDP-related event logs (Microsoft-Windows-TerminalServices)
3. Cross-reference with network share access from SMB logs
4. Review scheduled tasks and services for persistence mechanisms

## Output Format and Integration

All EZ Tools produce CSV output that can be:
- Analyzed in Timeline Explorer for visual investigation
- Imported into Splunk, Elastic, or other SIEM platforms
- Processed by Python/PowerShell scripts for automated analysis
- Combined into super timelines using log2timeline/Plaso

## References

- Eric Zimmerman's Tools: https://ericzimmerman.github.io/
- KAPE Documentation: https://ericzimmerman.github.io/KapeDocs/
- SANS EZ Tools Training: https://www.sans.org/tools/ez-tools
- SANS FOR508: Advanced Incident Response and Threat Hunting
- SANS FOR498: Battlefield Forensics & Data Acquisition
