---
name: cloud-incident-forensics
description: Cloud storage forensic acquisition involves collecting digital evidence from services like Google Drive, OneDrive, Dropbox, and Box through both API-based remote acquisition and local endpoint artifact analysis. Modern investigations must address the challenge that cloud-synced files may exist in multiple states: locally synchronized, cloud-only (o
domain: cybersecurity
---
------|---------------|----------------|-----------|
| OneDrive | SyncEngineDatabase.db | %LOCALAPPDATA%\Microsoft\OneDrive\cache\ | %LOCALAPPDATA%\Microsoft\OneDrive\logs\ |
| Google Drive | metadata_sqlite_db | %LOCALAPPDATA%\Google\DriveFS\{account}\content_cache\ | %LOCALAPPDATA%\Google\DriveFS\Logs\ |
| Dropbox | filecache.dbx (encrypted) | %APPDATA%\Dropbox\.dropbox.cache\ | %APPDATA%\Dropbox\logs\ |
| Box | sync_db | %LOCALAPPDATA%\Box\Box\cache\ | %LOCALAPPDATA%\Box\Box\logs\ |

## References

- SANS Cloud Storage Acquisition: https://www.sans.org/blog/cloud-storage-acquisition-from-endpoint-devices
- Magnet AXIOM Cloud: https://www.magnetforensics.com/blog/how-to-acquire-and-analyze-cloud-data-with-magnet-axiom/
- AWS Cloud Forensics Framework: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/cyber-forensics.html
- API-Based Forensic Acquisition of Cloud Drives: https://arxiv.org/abs/1603.06542

## Example Output

```text
$ python3 cloud_forensic_acquire.py --provider google-drive --auth /tokens/gdrive_token.json \
    --user jsmith@corporate.com --output /acquisition/gdrive

Cloud Storage Forensic Acquisition Tool v3.2
==============================================
Provider:    Google Drive
Account:     jsmith@corporate.com
Start Time:  2024-01-19 08:00:15 UTC
Auth Method: Admin SDK (domain-wide delegation)

[+] Enumerating files...
    Total files:        2,345
    Total folders:      178
    Shared with me:     456
    Trashed items:      89 (included in acquisition)
    Total size:         14.7 GB

[+] Acquiring file contents...
    Downloaded:    2,345 / 2,345  [████████████████████████████████] 100%
    Errors:        0
    Elapsed:       18m 32s

[+] Acquiring metadata...
    File metadata:      2,345 entries
    Revision history:   8,912 revisions across 1,234 files
    Sharing permissions: 3,456 permission entries
    Activity log:       12,345 events

[+] Acquiring trashed items...
    Recovered:     89 / 89 items (234 MB)

--- Acquisition Log ---
Timestamp (UTC)          | Action           | File                                    | Size    | SHA-256
2024-01-19 08:00:45      | Downloaded       | /My Drive/Finance/Q4_Report.xlsm        | 245 KB  | 7a3b8c9d...
2024-01-19 08:00:46      | Downloaded       | /My Drive/Finance/Budget_2024.xlsx       | 1.2 MB  | 8b4c9d0e...
...
2024-01-19 08:02:12      | Trash-Recovered  | /Trash/employee_list_full.csv            | 4.5 MB  | 9c5d0e1f...
2024-01-19 08:02:13      | Trash-Recovered  | /Trash/network_diagram_v3.vsdx          | 2.1 MB  | 0d6e1f2a...
2024-01-19 08:02:14      | Trash-Recovered  | /Trash/credentials_backup.kdbx          | 128 KB  | 1e7f2a3b...

--- Sharing Analysis ---
Files Shared Externally:
  /My Drive/Finance/Q4_Report.xlsm     → j.smith.personal8842@protonmail.com (2024-01-16 03:10 UTC)
  /My Drive/HR/employee_list_full.csv   → j.smith.personal8842@protonmail.com (2024-01-16 03:12 UTC)
  /My Drive/IT/network_diagram_v3.vsdx  → anonymous (link sharing, 2024-01-16 03:15 UTC)

--- Revision History (Suspicious) ---
File: /My Drive/Finance/Q4_Report.xlsm
  Rev 1:  2024-01-10 09:00:00 UTC  (245 KB)  - Original
  Rev 2:  2024-01-15 14:35:00 UTC  (248 KB)  - Modified (macro added)
  Rev 3:  2024-01-16 03:05:00 UTC  (245 KB)  - Reverted (macro removed - anti-forensics)

Acquisition Summary:
  Files acquired:       2,345 (14.7 GB)
  Trashed items:        89 (234 MB)
  Revisions:            8,912
  Chain of custody hash (full archive):
    SHA-256: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
  Output directory:     /acquisition/gdrive/
  Acquisition log:      /acquisition/gdrive/acquisition_log.csv
  Completion Time:      2024-01-19 08:18:47 UTC
```