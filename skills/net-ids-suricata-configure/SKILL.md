---
name: net-ids-suricata-configure
description: - Deploying a high-performance IDS/IPS capable of multi-threaded packet processing for 10+ Gbps network links - Monitoring network traffic with protocol-aware inspection for HTTP, TLS, DNS, SMB, and other protocols - Generating structured EVE JSON logs for direct SIEM ingestion without custom parsers - Running in inline (IPS) mode to actively block
domain: cybersecurity
---
---|------------|
| **EVE JSON** | Suricata's primary logging format producing structured JSON events for alerts, protocol metadata, flow records, and statistics |
| **AF_PACKET** | Linux kernel packet capture mechanism used by Suricata for high-performance traffic capture with kernel-bypass capabilities |
| **JA3/JA3S** | TLS fingerprinting method that creates hash values from TLS Client Hello and Server Hello parameters for identifying applications and malware |
| **HASSH** | SSH fingerprinting method similar to JA3 that creates hashes from SSH key exchange parameters to identify SSH client and server implementations |
| **Community ID** | Standardized flow identifier hash that enables correlation of the same network flow across different monitoring tools (Suricata, Zeek, Wireshark) |
| **suricata-update** | Official rule management tool that downloads, merges, and manages multiple rulesets with enable/disable controls |

## Tools & Systems

- **Suricata 7.0+**: Open-source multi-threaded IDS/IPS/NSM engine with protocol detection, file extraction, and JA3/HASSH fingerprinting
- **suricata-update**: Ruleset management tool supporting ET Open, ET Pro, Snort rules, and custom rule sources
- **Elastic Stack (ELK)**: Log aggregation and visualization platform with native Suricata module in Filebeat for dashboards and alerting
- **Scirius**: Web-based Suricata rule management interface for editing, enabling/disabling, and monitoring rule performance
- **Evebox**: Lightweight event viewer for Suricata EVE JSON logs with alert management and escalation capabilities

## Common Scenarios

### Scenario: Deploying Suricata IDS on a 10 Gbps Enterprise Network Perimeter

**Context**: A technology company needs to deploy IDS at their internet egress point handling 10 Gbps of traffic. They require protocol-level metadata logging for threat hunting, signature-based alerting for known threats, and JA3 fingerprinting for detecting malware C2 communications. Alerts must feed into their Elastic SIEM.

**Approach**:
1. Deploy Suricata on a server with 16 CPU cores, 64 GB RAM, and dual 10G NICs using AF_PACKET with 14 worker threads
2. Enable ET Open and ptresearch/attackdetection rulesets via suricata-update, totaling approximately 35,000 active rules
3. Configure EVE JSON logging with community-id, extended HTTP/TLS/DNS metadata, and file hashing (MD5 + SHA256)
4. Enable JA3 and HASSH fingerprinting for TLS and SSH traffic profiling
5. Write custom rules for organization-specific threats: known bad JA3 hashes, DNS queries to DGA domains, large data uploads to uncommon destinations
6. Integrate with Elastic via Filebeat's Suricata module, deploying pre-built Kibana dashboards for real-time visibility
7. Tune rules over a 2-week baseline period, disabling false-positive generators and adjusting thresholds

**Pitfalls**:
- Not allocating sufficient CPU threads, causing packet drops at peak traffic volumes
- Enabling all available rules without tuning, overwhelming analysts with false positives
- Forgetting to disable NIC offloading, resulting in incorrect checksums and missed detections
- Not enabling community-id, making it difficult to correlate Suricata events with Zeek or other tools

## Output Format

```
## Suricata IDS Deployment Report

**Sensor**: suricata-gw-01 (10.10.1.251)
**Interface**: eth1 (span from border router)
**Configuration**: /etc/suricata/suricata.yaml
**Worker Threads**: 14 AF_PACKET threads
**Active Rules**: 35,247 (ET Open + Custom)

### Performance Metrics (24-hour)

| Metric | Value |
|--------|-------|
| Packets Processed | 847,293,421 |
| Kernel Drops | 0 (0.000%) |
| Alerts Generated | 1,247 |
| Unique Signatures Fired | 89 |
| JA3 Fingerprints Observed | 342 unique |
| Files Extracted | 2,847 |

### Top 10 Alert Signatures

| Count | SID | Signature | Severity |
|-------|-----|-----------|----------|
| 312 | 2024897 | ET POLICY curl User-Agent Outbound | 3 |
| 189 | 9000003 | LOCAL Cobalt Strike JA3 Hash | 1 |
| 145 | 2028765 | ET SCAN Nmap SYN Scan | 2 |
| 98 | 9000002 | LOCAL DNS Tunneling Long Query | 2 |

### Critical Alerts Requiring Immediate Triage
1. SID 9000003: Cobalt Strike JA3 from 10.10.5.12 to 203.0.113.50 (189 alerts)
2. SID 9000002: DNS tunneling from 10.10.3.45 to suspect-domain.xyz (98 alerts)
```