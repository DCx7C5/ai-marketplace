## Overview

Investigate browser compromise indicators on Linux. Analyzes running browser processes, profile data (cookies, history, preferences), installed extensions for known-malicious IDs, and network connections made by the browser. Findings logged to both `findings.md` (session dir) and ORM database via `db.browser_forensics.log_finding_async`.

## Usage

```
Invoke when: suspected session hijacking, malicious extension, cookie theft, or browser-based C2.
Options: --deep (full artifact collection), --browser brave|all, --cookies, --extensions
```

## Checks

| Area | What is checked |
|---|---|
| Processes | Running browser processes, open file handles, memory maps |
| Cookies | Cookie files copied + analyzed for suspicious session tokens |
| History | Recent URLs cross-referenced against known malicious domains |
| Extensions | Extension IDs compared against blocklist; permissions reviewed |
| Network | Browser-initiated connections for C2 beaconing |

## Artifacts

- `session_dir/artifacts/browser/` — copied profile data
- ORM model: `db.browser_forensics` — `log_finding_async()` for each hit
- Uses `BrowserCookiesDB`, `BrowserHistoryDB`, `BrowserPreferencesDB` abstractions

## MITRE Coverage

| Technique | Description |
|---|---|
| T1539 | Steal Web Session Cookie |
| T1185 | Browser Session Hijacking |
| T1217 | Browser Information Discovery |
| T1176 | Browser Extensions (malicious) |
