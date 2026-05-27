---
name: vuln-scanning-authenticated
description: Authenticated (credentialed) vulnerability scanning uses valid system credentials to log into target hosts and perform deep inspection of installed software, patches, configurations, and security settings. Compared to unauthenticated scanning, credentialed scans detect 45-60% more vulnerabilities with significantly fewer false positives because the
domain: cybersecurity
---
## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "authenticated" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist