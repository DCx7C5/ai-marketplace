---
name: vuln-ms17
description: MS17-010 (EternalBlue) is a critical vulnerability in Microsoft's SMBv1 implementation that allows remote code execution. Originally discovered by the NSA and leaked by the Shadow Brokers in 2017, it was used in the WannaCry and NotPetya ransomware campaigns. Despite patches being available since March 2017, many organizations still have unpatched 
domain: cybersecurity
---
---|---------|
| Nmap ms-17-010 NSE scripts | Vulnerability detection |
| Metasploit ms17_010_eternalblue | Exploitation module |
| Metasploit ms17_010_psexec | Alternative exploitation |
| AutoBlue-MS17-010 | Standalone Python exploit |
| CrackMapExec | Mass SMB vulnerability scanning |

## Detection Indicators

- IDS/IPS signatures for EternalBlue exploit traffic
- SMBv1 negotiation from unusual source hosts
- Event ID 7045: New service installation after exploitation
- Anomalous named pipe activity on SMB
- Large SMB write requests characteristic of buffer overflow

## Validation Criteria

- [ ] Vulnerable systems identified via scanning
- [ ] Exploitation achieved on authorized target
- [ ] Code execution confirmed with session established
- [ ] Post-exploitation activities documented
- [ ] Remediation recommendations provided

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "ms17" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist