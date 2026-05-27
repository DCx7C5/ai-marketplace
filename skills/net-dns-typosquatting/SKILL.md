---
name: net-dns-typosquatting
description: "Net Dns Typosquatting."
domain: cybersecurity
---

-|
| reqeusts       | requests      | 1           | 2026-02-28 | 43     | 92    |
| requsets       | requests      | 1           | 2026-03-01 | 12     | 88    |
| numpyy         | numpy         | 1           | 2026-01-15 | 67     | 78    |

### Recommendation
- BLOCK: reqeusts, requsets, numpyy (add to artifact proxy deny-list)
- REPORT: Submit malware reports to security@pypi.org with package names and evidence
- MONITOR: Continue weekly scans for the full dependency watchlist
```
