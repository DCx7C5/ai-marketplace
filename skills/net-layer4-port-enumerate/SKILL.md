---
name: net-layer4-port-enumerate
description: - Automatically blocking IP addresses that perform port scans against internet-facing servers - Defending SSH, HTTP, FTP, and other services against brute force attacks with automated IP banning - Creating custom detection filters for organization-specific attack patterns in log files - Reducing noise from automated scanning bots before traffic rea
domain: cybersecurity
---
---|------------|
| **Jail** | Fail2ban configuration unit that combines a filter (what to detect), an action (what to do), and parameters (thresholds, timing) for a specific service |
| **Filter** | Regular expression patterns that Fail2ban applies to log files to identify failed authentication attempts, scanning, or other malicious activity |
| **Recidive Jail** | Meta-jail that monitors Fail2ban's own log for repeat offenders, applying escalating ban durations to IPs banned multiple times |
| **Find Time** | Time window in seconds during which Fail2ban counts matching log entries; maxretry failures within findtime triggers a ban |
| **Ban Action** | Command or script executed when an IP is banned, typically adding firewall rules but extensible to webhooks, SIEM alerts, or blocklist updates |
| **Ignore IP** | Whitelist of IP addresses or CIDR ranges that are never banned, preventing lockout of trusted networks and monitoring systems |

## Tools & Systems

- **Fail2ban 0.11+**: Log-parsing intrusion prevention framework that bans IP addresses based on pattern matching across any log file
- **iptables/nftables**: Linux kernel firewall used by Fail2ban ban actions to block offending IP addresses at the network layer
- **fail2ban-regex**: Testing utility for validating filter regular expressions against actual log files before deploying to production
- **fail2ban-client**: Command-line management tool for querying jail status, manually banning/unbanning IPs, and reloading configuration
- **rsyslog/syslog-ng**: System logging daemons that generate the log files Fail2ban monitors for attack detection

## Common Scenarios

### Scenario: Defending a Public-Facing Web Server Against Automated Scanning

**Context**: A company runs a public web server that receives thousands of automated scan attempts daily from bots probing for vulnerable paths (/wp-admin, /phpmyadmin, /.env). The security team wants to automatically block scanners while allowing legitimate traffic. The server runs Nginx on Ubuntu 22.04.

**Approach**:
1. Install Fail2ban and configure it to monitor Nginx access logs for scanning patterns (404/403 responses to known vulnerability paths)
2. Create a custom `http-scan` filter matching common scanner signatures and vulnerability probing URIs
3. Set maxretry to 10 within a 5-minute findtime, with a 1-hour bantime for first offense
4. Enable the recidive jail to escalate ban duration to 7 days for repeat offenders
5. Configure webhook notifications to Slack for real-time visibility of banning activity
6. Add iptables logging rules for SYN packets to closed ports to detect port scanning
7. Create a daily report script showing banned IPs, attack patterns, and geographic distribution

**Pitfalls**:
- Setting maxretry too low (e.g., 1-2), causing legitimate users who mistype URLs to get banned
- Not whitelisting monitoring systems (Nagios, UptimeRobot) that may trigger filters with their health checks
- Forgetting to persist iptables rules, losing all bans after a reboot
- Not testing filters with fail2ban-regex before deploying, resulting in no matches or excessive false positives

## Output Format

```
## Fail2ban Port Scan Defense Report

**Server**: web-prod-01 (203.0.113.50)
**Reporting Period**: 2024-03-15 00:00 to 2024-03-16 00:00 UTC

### Active Jails

| Jail | Filter | Max Retry | Ban Time | Currently Banned |
|------|--------|-----------|----------|------------------|
| sshd | sshd | 3 | 2 hours | 12 IPs |
| portscan | portscan | 10 | 24 hours | 47 IPs |
| http-scan | http-scan | 10 | 1 hour | 89 IPs |
| recidive | recidive | 3 | 7 days | 8 IPs |

### 24-Hour Summary
- Total ban events: 347
- Unique IPs banned: 156
- Top attacking country: CN (67 IPs), RU (34 IPs), US (21 IPs)
- Most targeted service: HTTP scanning (214 bans)
- Recidive escalations: 8 IPs banned for 7 days

### Top 5 Banned IPs
| IP Address | Jail | Ban Count | First Seen | Last Seen |
|------------|------|-----------|------------|-----------|
| 45.33.32.156 | portscan | 12 | 00:15 | 23:47 |
| 198.51.100.23 | http-scan | 8 | 02:30 | 18:22 |
| 203.0.113.100 | sshd | 6 | 05:12 | 21:33 |
```