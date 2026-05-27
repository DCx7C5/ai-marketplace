---
name: linux-sw-browser-artifact-forensics-forensic
description: - When investigating user web activity as part of a forensic examination - During insider threat investigations to establish patterns of data exfiltration - When tracing user visits to malicious or policy-violating websites - For correlating browser activity with other forensic artifacts and timelines - When investigating phishing attacks to identi
domain: cybersecurity
---
------|-------------|
| Chrome timestamp | Microseconds since January 1, 1601 (WebKit/Chrome epoch) |
| Firefox timestamp | Microseconds since January 1, 1970 (Unix epoch in microseconds) |
| Transition types | How a URL was accessed: typed (1), link (0), bookmark (1), redirect (5/6) |
| DPAPI encryption | Windows Data Protection API encrypting stored passwords and cookies |
| places.sqlite | Firefox combined history and bookmark database |
| SQLite WAL | Write-Ahead Log that may contain recently deleted browser records |
| Session restore | Browser data preserving open tabs across restarts |
| IndexedDB | Browser-based database that may contain web application data |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Hindsight | Comprehensive Chrome/Chromium forensic analysis tool |
| sqlite3 | Command-line SQLite database query tool |
| DB Browser for SQLite | GUI tool for browsing SQLite databases |
| BrowsingHistoryView | NirSoft tool for viewing browser history across all browsers |
| ChromeCacheView | NirSoft tool for examining Chrome cache contents |
| MZCacheView | NirSoft tool for Firefox cache analysis |
| KAPE | Automated artifact collection including browser data |
| Autopsy | Full forensic platform with browser artifact ingest modules |

## Common Scenarios

**Scenario 1: Phishing Investigation**
Extract browser history around the reported phishing timeframe, identify the phishing URL that was visited, check downloads for malicious attachments, examine cookies for session tokens that may have been stolen, correlate with email header analysis.

**Scenario 2: Data Exfiltration via Cloud Services**
Search history for cloud storage URLs (Dropbox, Google Drive, OneDrive, Mega), examine downloads and uploads, check form history for file names entered, review cookies for active cloud service sessions during the investigation period.

**Scenario 3: Policy Violation Investigation**
Extract complete browsing history for the investigation period, categorize sites visited, identify access to prohibited content categories, document timestamps and visit duration, correlate with network proxy logs for verification.

**Scenario 4: Malware Delivery Vector Analysis**
Trace the chain of redirects leading to a drive-by download, examine the downloads database for the malware payload, check cache for exploit kit landing pages, identify the initial referrer URL that started the infection chain.

## Output Format

```
Browser Forensics Summary:
  User Profile: suspect (Windows 10)
  Browsers Found: Chrome 120, Firefox 121, Edge 120

  Chrome Analysis:
    History Entries:    12,456
    Downloads:          234
    Saved Passwords:    67 sites (encrypted)
    Cookies:            3,456
    Bookmarks:          89

  Firefox Analysis:
    History Entries:    5,678
    Form Entries:       234
    Bookmarks:          45
    Cookies:            1,234

  Suspicious Findings:
    - Visited known phishing URL at 2024-01-15 14:32 UTC
    - Downloaded "invoice_update.exe" from suspicious domain
    - Cloud storage (mega.nz) accessed 15 times in 2-hour window
    - Search queries: "how to encrypt files", "secure file transfer"

  Reports:
    Chrome History:   /analysis/chrome_history.csv
    Firefox History:  /analysis/firefox_history.csv
    Full Report:      /analysis/hindsight_report.xlsx
```