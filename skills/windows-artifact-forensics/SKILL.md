---
name: windows-artifact-forensics
description: Eric Zimmerman's EZ Tools suite is a collection of open-source forensic utilities that have become the global standard for Windows digital forensics investigations. Originally developed by a former FBI agent and current SANS instructor, these tools parse and analyze critical Windows artifacts including the Master File Table ($MFT), registry hives, 
domain: cybersecurity
---
----|-------------|
| EntryNumber | MFT record number |
| ParentEntryNumber | Parent directory MFT record |
| InUse | Whether the record is active or deleted |
| FileName | Name of the file or directory |
| Created0x10 | $STANDARD_INFORMATION creation timestamp |
| Created0x30 | $FILE_NAME creation timestamp |
| LastModified0x10 | $STANDARD_INFORMATION modification timestamp |
| IsDirectory | Boolean indicating directory or file |
| FileSize | Logical file size in bytes |
| Extension | File extension |

### PECmd - Prefetch File Parser

PECmd parses Windows Prefetch files (.pf) to provide evidence of program execution, including run counts and timestamps.

```powershell
# Parse all prefetch files from a directory
PECmd.exe -d "C:\Cases\Evidence\Windows\Prefetch" --csv C:\Cases\Output --csvf Prefetch_output.csv

# Parse a single prefetch file with verbose output
PECmd.exe -f "C:\Cases\Evidence\Windows\Prefetch\CMD.EXE-4A81B364.pf" --json C:\Cases\Output

# Parse prefetch with keyword filtering
PECmd.exe -d "C:\Cases\Evidence\Windows\Prefetch" -k "powershell,cmd,wscript,cscript,mshta" --csv C:\Cases\Output --csvf SuspiciousExec.csv
```

### RECmd - Registry Explorer Command Line

RECmd processes Windows registry hives using batch files that define which keys and values to extract.

```powershell
# Process all registry hives with the default batch file
RECmd.exe --bn C:\Tools\KAPE\Modules\bin\RECmd\BatchExamples\RECmd_Batch_MC.reb -d "C:\Cases\Evidence\Registry" --csv C:\Cases\Output --csvf Registry_output.csv

# Process a single NTUSER.DAT hive
RECmd.exe -f "C:\Cases\Evidence\Users\suspect\NTUSER.DAT" --bn C:\Tools\KAPE\Modules\bin\RECmd\BatchExamples\RECmd_Batch_MC.reb --csv C:\Cases\Output

# Process SYSTEM hive for USB device history
RECmd.exe -f "C:\Cases\Evidence\Registry\SYSTEM" --bn C:\Tools\KAPE\Modules\bin\RECmd\BatchExamples\RECmd_Batch_MC.reb --csv C:\Cases\Output
```

### EvtxECmd - Windows Event Log Parser

EvtxECmd parses Windows Event Log (.evtx) files into structured CSV format with customizable event ID maps.

```powershell
# Parse all event logs from a directory
EvtxECmd.exe -d "C:\Cases\Evidence\Windows\System32\winevt\Logs" --csv C:\Cases\Output --csvf EventLogs_output.csv

# Parse a single event log
EvtxECmd.exe -f "C:\Cases\Evidence\Security.evtx" --csv C:\Cases\Output --csvf Security_output.csv

# Parse with custom maps for enhanced field extraction
EvtxECmd.exe -d "C:\Cases\Evidence\Logs" --csv C:\Cases\Output --maps C:\Tools\KAPE\Modules\bin\EvtxECmd\Maps
```

### LECmd and JLECmd - Shortcut and Jump List Parsers

```powershell
# Parse LNK files from Recent directory
LECmd.exe -d "C:\Cases\Evidence\Users\suspect\AppData\Roaming\Microsoft\Windows\Recent" --csv C:\Cases\Output --csvf LNK_output.csv

# Parse Jump Lists (automatic destinations)
JLECmd.exe -d "C:\Cases\Evidence\Users\suspect\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations" --csv C:\Cases\Output --csvf JumpLists_auto.csv

# Parse Jump Lists (custom destinations)
JLECmd.exe -d "C:\Cases\Evidence\Users\suspect\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations" --csv C:\Cases\Output --csvf JumpLists_custom.csv
```

### SBECmd - Shellbag Explorer Command Line

```powershell
# Parse shellbags from a directory of registry hives
SBECmd.exe -d "C:\Cases\Evidence\Registry" --csv C:\Cases\Output --csvf Shellbags_output.csv

# Parse shellbags from a live system (requires admin)
SBECmd.exe --live --csv C:\Cases\Output --csvf LiveShellbags_output.csv
```

### Timeline Explorer - Visual Analysis

Timeline Explorer is the GUI tool for analyzing CSV output from all EZ Tools. It supports filtering, sorting, column grouping, and conditional formatting.

```powershell
# Launch Timeline Explorer and open CSV output
TimelineExplorer.exe "C:\Cases\Output\MFT_output.csv"
```

**Key Timeline Explorer Features:**
- Column-level filtering with regular expressions
- Conditional formatting for timestamp anomalies
- Multi-column sorting for chronological analysis
- Export filtered results to new CSV files
- Bookmarking rows of interest

## Investigation Workflow

### Step 1: Artifact Collection with KAPE

```powershell
# Full triage collection from forensic image mounted at E:
kape.exe --tsource E: --tdest C:\Cases\Case001\Collected --target KapeTriage --vhdx TriageImage --zv false
```

### Step 2: Artifact Processing with EZ Tools

```powershell
# Process all collected artifacts
kape.exe --msource C:\Cases\Case001\Collected --mdest C:\Cases\Case001\Processed --module !EZParser
```

### Step 3: Timeline Analysis

1. Open processed CSV files in Timeline Explorer
2. Sort by timestamp columns to establish chronological order
3. Filter for specific file extensions, paths, or event IDs
4. Cross-reference MFT timestamps with event log entries
5. Identify timestomping by comparing $SI and $FN timestamps
6. Document findings with bookmarks and exported filtered views

### Step 4: Timestomping Detection

```powershell
# In Timeline Explorer, compare these columns:
# Created0x10 ($STANDARD_INFORMATION) vs Created0x30 ($FILE_NAME)
# If Created0x10 < Created0x30, timestomping is indicated
# $FILE_NAME timestamps are harder to manipulate than $STANDARD_INFORMATION
```

## Forensic Artifacts Reference

| Tool | Artifact | Location |
|------|----------|----------|
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