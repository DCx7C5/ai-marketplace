---
name: vuln-metasploit
description: The Metasploit Framework is the world's most widely used penetration testing platform, maintained by Rapid7. It contains over 2,300 exploits, 1,200 auxiliary modules, and 400 post-exploitation modules. Within vulnerability management, Metasploit serves as a validation tool to confirm that identified vulnerabilities are actually exploitable, enablin
domain: cybersecurity
---
## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "metasploit" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist