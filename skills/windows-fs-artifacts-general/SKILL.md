---
name: windows-fs-artifacts-general
description: "|"
domain: cybersecurity
---
|
| **Amcache.hve** | A Windows registry hive at `C:\Windows\appcompat\Programs\Amcache.hve` that stores metadata about applications, files, and drivers for application compatibility purposes |
| **Associated File Entry** | An Amcache record linked to a specific program installation, containing file path, size, hash, and timestamps |
| **Unassociated File Entry** | An orphaned Amcache record from an older format that is not linked to a program entry; common on Windows 7/8 systems |
| **Program Entry** | Amcache record containing installation metadata: program name, version, publisher, install date, and uninstall key |
| **SHA-1 Hash** | Cryptographic hash stored in Amcache for each registered file, enabling malware identification through threat intelligence lookups |
| **LinkDate** | The PE compilation timestamp embedded in the executable header; discrepancy with file system timestamps may indicate timestomping |
| **Transaction Logs** | `.LOG1` and `.LOG2` files containing uncommitted registry transactions that AmcacheParser replays for complete data recovery |
| **NSRL (National Software Reference Library)** | NIST-maintained database of SHA-1 hashes for known commercial software, used as a whitelist to filter benign entries |

## Verification

- [ ] Amcache.hve and transaction logs (LOG1, LOG2) were collected from the forensic image
- [ ] AmcacheParser produced all expected CSV output files without errors
- [ ] SHA-1 hashes were extracted and checked against VirusTotal or CIRCL hashlookup
- [ ] Unsigned executables in suspicious paths have been flagged for further analysis
- [ ] Program entries show all software installations within the incident window
- [ ] Driver binaries have been checked for unsigned or out-of-box entries
- [ ] LinkDate vs. FileKeyLastWriteTimestamp comparison has been performed to detect timestomping
- [ ] Amcache findings are correlated with Prefetch and ShimCache for execution confirmation
- [ ] Final timeline integrates Amcache data with other forensic artifacts
