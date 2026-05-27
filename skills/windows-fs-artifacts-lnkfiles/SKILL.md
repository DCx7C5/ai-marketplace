---
name: windows-fs-artifacts-lnkfiles
description: - When reconstructing user file access history from Windows shortcut files - For tracking accessed files, network shares, and removable media - During investigations to prove a user opened specific documents - When correlating file access with other timeline artifacts - For identifying accessed paths on remote systems or USB devices
domain: cybersecurity
---
------|-------------|
| Shell Link (.lnk) | Windows shortcut file format containing target path, timestamps, and metadata |
| Target timestamps | Creation, modification, and access times of the file the shortcut points to |
| Volume serial number | Unique identifier of the drive volume where the target file resides |
| Machine ID | NetBIOS name embedded by the Distributed Link Tracking service |
| MAC address | Network adapter MAC from the machine that created the LNK file |
| Jump Lists | Recent and pinned file lists per application (contain embedded LNK data) |
| Automatic Destinations | System-managed Jump List entries for recently opened files |
| Custom Destinations | User-pinned Jump List items that persist until manually removed |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| LECmd | Eric Zimmerman command-line LNK file parser with CSV/JSON output |
| JLECmd | Eric Zimmerman Jump List parser |
| LnkParse3 | Python library for programmatic LNK file analysis |
| lnk_parser | Alternative Python LNK parsing tool |
| Autopsy | Forensic platform with LNK file analysis module |
| KAPE | Automated LNK and Jump List artifact collection |
| Plaso | Timeline tool with LNK file parser for super-timeline creation |
| LNK Explorer | GUI tool for interactive LNK file examination |

## Common Scenarios

**Scenario 1: Data Exfiltration via USB Drive**
Analyze Recent folder LNK files for targets on removable drives, correlate volume serial numbers with USBSTOR registry entries, build a list of files accessed from USB devices, establish which documents were opened from the removable drive, correlate with file copy timestamps.

**Scenario 2: Malware Persistence via Startup Shortcuts**
Examine Startup folder LNK files for malicious targets, check target path and arguments for encoded commands or suspicious executables, verify target file exists and examine it, correlate creation timestamp with initial compromise time.

**Scenario 3: Network Share Access Investigation**
Filter LNK files with network paths (UNC targets), identify which network shares were accessed and when, correlate machine IDs with known corporate systems, check if sensitive file servers were accessed outside of normal duties, build access timeline for compliance investigation.

**Scenario 4: Document Access Timeline for Legal Proceedings**
Extract all Recent folder LNK files, build chronological list of documents accessed by the user, identify specific files relevant to the case, present target timestamps showing when files were opened, correlate with email and communication timelines.

## Output Format

```
LNK File Analysis Summary:
  User Profile: suspect_user
  Total LNK Files: 234 (Recent: 198, Desktop: 23, Startup: 5, Other: 8)

  File Access Statistics:
    Local drive (C:):    156 files
    Removable media:     23 files (3 unique volume serials)
    Network shares:      15 files (\\server01, \\fileserver)
    Other drives:        4 files

  Machine IDs Found: DESKTOP-ABC123, LAPTOP-XYZ789
  MAC Addresses: AA:BB:CC:DD:EE:FF, 11:22:33:44:55:66

  Removable Media Access:
    Volume Serial 1234-ABCD:
      2024-01-15 14:32 - E:\Confidential\financial_report.xlsx
      2024-01-15 14:45 - E:\Confidential\customer_database.csv
      2024-01-15 15:00 - E:\Projects\source_code.zip

  Startup Persistence:
    updater.lnk -> C:\ProgramData\svc\updater.exe (SUSPICIOUS)
    OneDrive.lnk -> C:\Users\...\OneDrive.exe (Legitimate)

  Timeline: /cases/case-2024-001/analysis/lnk_analysis.csv
```