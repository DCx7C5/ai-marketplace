---
name: net-capture-pcapforensics
description: - When analyzing captured network traffic (PCAP files) from a security incident - For identifying command-and-control (C2) communications in captured traffic - When reconstructing data exfiltration activities from packet captures - During malware analysis to identify network indicators of compromise - For extracting files, credentials, and artifact
domain: cybersecurity
---
------|-------------|
| PCAP/PCAPNG | Packet capture file formats storing raw network traffic |
| TCP stream | Complete bidirectional communication between two endpoints |
| Deep packet inspection | Analysis of packet payload content beyond header information |
| Beaconing | Regular-interval callbacks from malware to C2 servers |
| DNS tunneling | Encoding data within DNS queries for covert exfiltration |
| TLS/SNI | Server Name Indication revealing the target hostname in encrypted connections |
| Network flow | Summary of communication between endpoints (IPs, ports, bytes, duration) |
| Protocol hierarchy | Statistical breakdown of protocols present in a capture |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Wireshark | GUI-based packet analyzer with deep protocol dissection |
| tshark | Command-line version of Wireshark for scripted analysis |
| NetworkMiner | Automated network forensic analysis and file extraction |
| tcpdump | Command-line packet capture utility |
| zeek (Bro) | Network security monitor generating structured connection logs |
| ngrep | Network grep for pattern matching in packet content |
| capinfos | PCAP file statistics and metadata utility |
| mergecap | Merge multiple PCAP files into a single capture |

## Common Scenarios

**Scenario 1: Malware C2 Communication Analysis**
Load PCAP in Wireshark, identify beaconing patterns to external IPs, examine TLS certificates for self-signed or unusual issuers, extract HTTP POST data containing encoded commands, correlate C2 IPs with threat intelligence feeds.

**Scenario 2: Data Exfiltration Detection**
Analyze traffic statistics for unusually large outbound transfers, examine DNS query lengths for DNS tunneling indicators, track FTP and HTTP file uploads to external servers, reconstruct exfiltrated files from packet data.

**Scenario 3: Lateral Movement in Enterprise Network**
Filter for SMB, RDP, WMI, and PSExec traffic between internal hosts, identify credential usage patterns across multiple systems, trace the propagation path of the attacker through the network, correlate with Windows Event Log authentication events.

**Scenario 4: Web Application Attack Reconstruction**
Filter HTTP traffic to the web server, identify SQL injection, XSS, and directory traversal attempts, follow the TCP stream of the successful exploit, extract uploaded webshells or payloads, document the attack chain for the incident report.

## Output Format

```
Network Forensics Summary:
  Capture: capture.pcap
  Duration: 1 hour (14:00-15:00 UTC, 2024-01-15)
  Packets: 1,245,678 | Size: 856 MB

  Top Suspicious Connections:
    192.168.1.50 -> 185.0.0.1:443   (C2, 58 connections, 4.2MB out)
    192.168.1.50 -> 10.0.0.25:445   (SMB lateral movement)
    192.168.1.50 -> 10.0.0.30:3389  (RDP lateral movement)

  Extracted Artifacts:
    Files:        23 (3 malicious per VT)
    Credentials:  2 plaintext FTP logins
    DNS Queries:  1,234 suspicious (possible tunneling)
    TLS Certs:    5 self-signed certificates

  IOCs Identified:
    IPs:     185.0.0.1, 203.0.113.50
    Domains: update-service.malware-c2.com, data.evil-dns.com
    Hashes:  3 file hashes flagged as malware
```