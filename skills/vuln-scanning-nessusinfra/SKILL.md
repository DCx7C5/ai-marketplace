---
name: vuln-scanning-nessusinfra
description: Tenable Nessus is the industry-leading vulnerability scanner used to identify security weaknesses across network infrastructure including servers, workstations, network devices, and operating systems. This skill covers configuring scan policies, running authenticated and unauthenticated scans, interpreting results, and integrating Nessus into conti
domain: cybersecurity
---
## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "nessusinfra" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist