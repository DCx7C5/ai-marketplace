---
name: soc-recovery-backup-recover
description: "Soc Recovery Backup Recover."
domain: cybersecurity
---

|
| Restic | Encrypted, deduplicated backup with built-in integrity verification |
| BorgBackup | Deduplicating backup with archive verification |
| Rclone | Cloud storage sync with checksum verification |
| AWS S3 Object Lock | Immutable backup storage with WORM compliance |
| Azure Immutable Blob | Tamper-proof backup storage for compliance |
| sha256sum | Standard hash computation for file integrity |
| pg_restore | PostgreSQL backup validation and restore testing |

## Common Pitfalls

- **Never testing restores**: The most common failure mode. Backups that are never restored are untested assumptions.
- **Checking only archive integrity, not data integrity**: A valid tar.gz can contain corrupted file contents. Always hash individual files.
- **Trusting last backup without scanning for ransomware**: Backups may contain encrypted files if the infection predates the backup.
- **Ignoring incremental chain integrity**: A single corrupted incremental backup can break the entire restore chain.
- **No alerting on validation failures**: Backup validation must be monitored with alerts, not just logged silently.
- **Using MD5 for integrity**: MD5 is cryptographically broken. Use SHA-256 or SHA-3 for integrity verification.

## References

- NIST SP 800-184: Guide for Cybersecurity Event Recovery
- NIST CSF 2.0 RC.RP-03: Backup Integrity Verification
- CIS Controls v8: Control 11 - Data Recovery
- CISA Ransomware Guide: https://www.cisa.gov/stopransomware
