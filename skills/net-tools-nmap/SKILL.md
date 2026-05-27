---
name: net-tools-nmap
description: - Performing comprehensive asset discovery across large enterprise networks during authorized assessments - Enumerating service versions and configurations to identify outdated or vulnerable software - Bypassing firewall rules and IDS during authorized penetration tests using scan evasion techniques - Scripting automated vulnerability checks using 
domain: cybersecurity
---
---|------------|
| **SYN Scan (-sS)** | Half-open TCP scan that sends SYN packets and analyzes responses without completing the three-way handshake, making it faster and stealthier than connect scans |
| **NSE (Nmap Scripting Engine)** | Lua-based scripting framework built into Nmap that enables vulnerability detection, brute forcing, service discovery, and custom automation |
| **Timing Templates (-T0 to -T5)** | Predefined scan speed profiles ranging from Paranoid (T0) to Insane (T5), controlling probe parallelism, timeout values, and inter-probe delays |
| **Idle Scan (-sI)** | Advanced scan technique that uses a zombie host's IP ID sequence to port scan a target without sending packets from the scanner's own IP address |
| **Version Intensity** | Controls how many probes Nmap sends to determine service versions, ranging from 0 (light) to 9 (all probes), trading speed for accuracy |
| **Grepable Output (-oG)** | Legacy Nmap output format designed for easy parsing with grep, awk, and sed for scripted analysis of scan results |

## Tools & Systems

- **Nmap 7.90+**: Core scanning engine with NSE scripting, OS detection, version probing, and multiple output formats
- **nmap-parse-output**: Community tool for parsing Nmap XML output into structured formats (CSV, JSON, host lists)
- **Ndiff**: Nmap utility for comparing two scan results to identify changes in network state over time
- **Zenmap**: Official Nmap GUI providing visual network topology mapping and scan profile management
- **Metasploit Framework**: Imports Nmap XML output for direct correlation of scan results with exploit modules

## Common Scenarios

### Scenario: Enterprise Network Asset Discovery and Vulnerability Baseline

**Context**: A security team needs to establish a vulnerability baseline for a corporate network spanning 10.0.0.0/8 with approximately 5,000 active hosts. Scanning must complete within a weekend maintenance window with minimal network disruption.

**Approach**:
1. Run layered host discovery using ARP (local subnets), TCP SYN (ports 22,80,443,445,3389), and ICMP echo probes across all /24 subnets
2. Perform a full TCP SYN scan on discovered hosts using `--min-rate 5000` and `-T4` to complete within the window
3. Run service version detection and default NSE scripts on all open ports
4. Execute targeted NSE vulnerability scripts for critical services (SMB, SSL/TLS, HTTP)
5. Parse XML output to generate per-subnet CSV reports and import into the vulnerability management platform
6. Schedule Ndiff comparisons against future scans to track remediation progress

**Pitfalls**:
- Setting `--min-rate` too high on congested network segments causing packet loss and false negatives
- Running `-T5` (Insane) timing on production networks, potentially overwhelming older network devices
- Forgetting to scan UDP ports, missing critical services like SNMP (161), DNS (53), and TFTP (69)
- Not saving output in XML format (`-oX` or `-oA`), losing structured data for downstream tool integration

## Output Format

```
## Nmap Scan Summary

**Scan Profile**: Full TCP + Top 200 UDP + Service Enumeration
**Target Range**: 10.10.0.0/16
**Hosts Discovered**: 347 live hosts
**Scan Duration**: 2h 14m

### Critical Findings

| Host | Port | Service | Version | Vulnerability |
|------|------|---------|---------|---------------|
| 10.10.5.23 | 445/tcp | SMB | Windows Server 2012 R2 | MS17-010 (EternalBlue) |
| 10.10.8.100 | 443/tcp | Apache httpd | 2.4.29 | CVE-2021-41773 (Path Traversal) |
| 10.10.12.5 | 3306/tcp | MySQL | 5.6.24 | CVE-2016-6662 (RCE) |
| 10.10.3.77 | 161/udp | SNMP | v2c | Public community string |

### Recommendations
1. Patch MS17-010 on 10.10.5.23 immediately -- Critical RCE vulnerability
2. Upgrade Apache httpd to 2.4.58+ on 10.10.8.100
3. Upgrade MySQL to 8.0.x on 10.10.12.5 and restrict bind address
4. Change SNMP community strings from "public" on 10.10.3.77
```