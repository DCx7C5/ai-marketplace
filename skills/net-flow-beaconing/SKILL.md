---
name: net-flow-beaconing
description: - When proactively searching for compromised endpoints calling back to C2 infrastructure - After threat intelligence reports indicate active C2 frameworks targeting your sector - When network logs show periodic outbound connections to unfamiliar destinations - During purple team exercises validating C2 detection capabilities - When investigating a 
domain: cybersecurity
---
------|-------------|
| T1071.001 | Application Layer Protocol: Web Protocols -- HTTP/HTTPS beaconing |
| T1071.004 | Application Layer Protocol: DNS -- DNS-based C2 tunneling |
| T1573 | Encrypted Channel -- TLS/SSL encrypted C2 communication |
| T1568.002 | Dynamic Resolution: Domain Generation Algorithms |
| Coefficient of Variation | Standard deviation divided by mean; values below 0.20 indicate periodicity |
| Jitter | Random variation added to beacon interval to evade detection |
| RITA Beacon Score | Composite score from connection regularity, data size consistency, and connection count |
| JA3/JA4 Fingerprinting | TLS client fingerprinting to identify C2 framework signatures |
| Fast-Flux DNS | Rapidly changing DNS resolution used to protect C2 infrastructure |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| RITA (Real Intelligence Threat Analytics) | Automated beacon scoring from Zeek logs |
| AC-Hunter | Commercial threat hunting platform with beacon detection |
| Splunk | SPL-based statistical beacon analysis with streamstats |
| Elastic Security | ML anomaly detection for periodic network behavior |
| Zeek | Network metadata collection (conn.log, dns.log, ssl.log) |
| Suricata | Network IDS with JA3/JA4 TLS fingerprint extraction |
| FLARE | C2 profile and beacon pattern detection |
| VirusTotal | Domain and IP reputation enrichment |

## Detection Queries

### Splunk -- HTTP/S Beacon Frequency Analysis
```spl
index=proxy OR index=firewall
| where NOT match(dest, "(?i)(microsoft|google|amazonaws|cloudflare|akamai)")
| bin _time span=1s
| stats count by src_ip dest _time
| streamstats current=f last(_time) as prev_time by src_ip dest
| eval interval=_time-prev_time
| stats count avg(interval) as avg_interval stdev(interval) as stdev_interval
  min(interval) as min_interval max(interval) as max_interval by src_ip dest
| where count > 50
| eval cv=stdev_interval/avg_interval
| where cv < 0.20 AND avg_interval > 30 AND avg_interval < 86400
| sort cv
| table src_ip dest count avg_interval stdev_interval cv
```

### KQL -- Microsoft Sentinel Beacon Detection
```kql
DeviceNetworkEvents
| where Timestamp > ago(24h)
| where RemoteIPType == "Public"
| summarize ConnectionTimes=make_list(Timestamp), Count=count() by DeviceName, RemoteIP, RemoteUrl
| where Count > 50
| extend Intervals = array_sort_asc(ConnectionTimes)
| mv-apply Intervals on (
    extend NextTime = next(Intervals)
    | where isnotempty(NextTime)
    | extend IntervalSec = datetime_diff('second', NextTime, Intervals)
    | summarize AvgInterval=avg(IntervalSec), StdDev=stdev(IntervalSec)
)
| extend CV = StdDev / AvgInterval
| where CV < 0.2 and AvgInterval > 30
| sort by CV asc
```

### Sigma Rule -- Beaconing Pattern Detection
```yaml
title: Potential C2 Beaconing Pattern Detected
status: experimental
logsource:
    category: proxy
detection:
    selection:
        dst_ip|cidr: '!10.0.0.0/8'
    timeframe: 24h
    condition: selection | count(dst) by src_ip > 50
level: medium
tags:
    - attack.command_and_control
    - attack.t1071.001
```

## Common Scenarios

1. **Cobalt Strike Beacon**: Default 60-second interval with configurable 0-50% jitter over HTTPS. Malleable C2 profiles can mimic legitimate traffic patterns.
2. **Sunburst/SUNSPOT**: 12-14 day dormancy period, then beaconing every 12-14 minutes with randomized jitter, designed to evade frequency analysis.
3. **DNS Tunneling C2**: Encoded data exfiltration via DNS TXT/CNAME queries to attacker-controlled domains, detectable via high subdomain entropy and query volume.
4. **Sliver C2**: Modern C2 framework with HTTPS, mTLS, and WireGuard protocols, configurable beacon intervals with built-in jitter support.
5. **Legitimate Service Abuse**: C2 communication over Slack, Discord, Telegram, or cloud storage APIs, making destination-based filtering ineffective.

## Output Format

```
Hunt ID: TH-BEACON-[DATE]-[SEQ]
Source IP: [Internal IP]
Source Host: [Hostname from DHCP/DNS]
Destination: [Domain/IP]
Protocol: [HTTP/HTTPS/DNS]
Beacon Interval: [Average seconds]
Jitter Estimate: [Percentage]
Coefficient of Variation: [CV value]
Connection Count: [Total connections in window]
Data Size CV: [Payload consistency metric]
Domain Age: [Days since registration]
TI Match: [Yes/No -- source]
Risk Score: [0-100]
Risk Level: [Critical/High/Medium/Low]
Indicators: [List of triggered risk factors]
```