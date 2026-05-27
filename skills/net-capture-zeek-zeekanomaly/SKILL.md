---
name: net-capture-zeek-zeekanomaly
description: - Deploying passive network security monitoring at key network choke points for continuous visibility - Generating structured connection, DNS, HTTP, SSL, and file transfer logs for SIEM ingestion and threat hunting - Writing custom Zeek scripts to detect organization-specific threats, policy violations, or beaconing behavior - Performing retrospect
domain: cybersecurity
---
---|------------|
| **Network Security Monitor** | Passive analysis tool that observes network traffic and generates structured metadata logs without altering or blocking traffic flow |
| **Zeek Script** | Event-driven scripts written in Zeek's domain-specific language that process network events and generate notices, logs, and metrics |
| **Connection Log (conn.log)** | Core Zeek log recording every observed connection with source/destination IPs, ports, protocol, duration, and byte counts |
| **Notice Framework** | Zeek subsystem for generating alerts when detection scripts identify suspicious activity, outputting to notice.log |
| **SumStats Framework** | Statistical analysis framework in Zeek for tracking metrics over time windows, enabling threshold-based detection of anomalies |
| **Intel Framework** | Zeek module for matching observed network indicators against threat intelligence feeds and generating alerts on matches |

## Tools & Systems

- **Zeek 6.0+**: Open-source network security monitor generating comprehensive protocol-level logs from passive traffic analysis
- **zeek-cut**: Zeek utility for extracting specific columns from tab-separated Zeek log files for quick analysis
- **zeekctl**: Zeek management tool for deploying, monitoring, and managing Zeek instances across single or clustered deployments
- **RITA (Real Intelligence Threat Analytics)**: Open-source tool that analyzes Zeek logs for beaconing, DNS tunneling, and other threat indicators
- **Filebeat**: Elastic agent for shipping Zeek JSON logs to Elasticsearch for centralized analysis and visualization

## Common Scenarios

### Scenario: Detecting Command-and-Control Beaconing in Enterprise Traffic

**Context**: A threat intelligence report indicates that a specific threat actor uses HTTPS beaconing with 60-second intervals to compromised hosts. The SOC team needs to analyze Zeek logs to identify any hosts exhibiting this pattern across the enterprise network carrying 2 Gbps of traffic.

**Approach**:
1. Deploy Zeek on a network tap at the internet egress point with AF_PACKET for high-throughput capture
2. Enable the custom beacon detection script with thresholds tuned for 60-second intervals over 1-hour observation windows
3. Query conn.log for connections to external IPs with consistent duration and inter-connection timing: filter connections where the standard deviation of inter-arrival times is less than 5 seconds
4. Cross-reference suspicious destination IPs against threat intelligence feeds loaded into Zeek's Intel framework
5. Examine ssl.log for the associated TLS certificates -- check for self-signed certificates, unusual issuer names, or certificates with short validity periods
6. Generate a notice for each identified beaconing source and feed into the SIEM for SOC triage

**Pitfalls**:
- Not tuning beacon detection thresholds for the environment, resulting in false positives from legitimate update services (Windows Update, AV updates)
- Failing to exclude CDN and cloud service provider IP ranges that naturally receive many repeat connections
- Running Zeek without sufficient CPU cores, causing packet drops on high-throughput links
- Not enabling JSON log output, making SIEM integration unnecessarily complex with custom parsers

## Output Format

```
## Zeek Network Anomaly Detection Report

**Sensor**: zeek-sensor-01 (10.10.1.250)
**Monitoring Interface**: eth1 (span port from Core-SW1)
**Analysis Period**: 2024-03-15 00:00 to 2024-03-16 00:00 UTC
**Total Connections Logged**: 2,847,392

### Anomalies Detected

| Notice Type | Source | Destination | Details |
|-------------|--------|-------------|---------|
| DNS_Tunneling_Detected | 10.10.3.45 | 8.8.8.8 | 847 queries to suspect-domain.xyz in 5 min |
| Possible_Beaconing | 10.10.5.12 | 203.0.113.50:443 | 62 connections with 59.8s avg interval |
| SSL::Invalid_Server_Cert | 10.10.8.22 | 198.51.100.33:443 | Self-signed cert, CN=localhost |
| SSH::Password_Guessing | 45.33.32.156 | 10.10.20.11:22 | 487 failed attempts in 30 min |

### Recommendations
1. Isolate 10.10.3.45 and investigate for DNS tunneling malware
2. Block 203.0.113.50 at firewall and forensically image 10.10.5.12
3. Investigate self-signed TLS certificate on 198.51.100.33
4. Block 45.33.32.156 and enforce SSH key-only authentication
```