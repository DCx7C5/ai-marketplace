---
name: net-capture-wireshark
description: "Net Capture Wireshark."
domain: cybersecurity
---

|
| **Capture Filter (BPF)** | Berkeley Packet Filter syntax applied at capture time to limit which packets are recorded, reducing file size and improving performance |
| **Display Filter** | Wireshark-specific filter syntax applied to already-captured packets for focused analysis without altering the capture file |
| **PCAPNG** | Next-generation packet capture format supporting multiple interfaces, name resolution, annotations, and metadata in a single file |
| **TCP Stream** | Reassembled sequence of TCP segments representing a complete bidirectional conversation between two endpoints |
| **Protocol Dissector** | Wireshark module that decodes a specific protocol's fields and structure, enabling deep inspection of packet contents |
| **IO Graph** | Time-series visualization of packet or byte rates over the capture duration, useful for identifying traffic spikes or beaconing |

## Tools & Systems

- **Wireshark 4.0+**: GUI-based packet analyzer with protocol dissectors for 3,000+ protocols, stream reassembly, and export capabilities
- **tshark**: Command-line version of Wireshark for headless capture, batch processing, and scripted analysis pipelines
- **tcpdump**: Lightweight packet capture tool for quick captures on remote systems without GUI dependencies
- **mergecap**: Wireshark utility for combining multiple capture files into a single PCAP for unified analysis
- **editcap**: Wireshark utility for splitting, filtering, and converting between capture file formats

## Common Scenarios

### Scenario: Investigating Suspected Data Exfiltration via DNS Tunneling

**Context**: The SOC team detected unusually high DNS query volumes from a workstation (10.10.3.45) to an external domain. The SIEM alert flagged DNS queries averaging 200 per minute compared to the baseline of 15. A packet capture was initiated from the network tap on the workstation's VLAN.

**Approach**:
1. Capture traffic from the workstation's subnet using `tshark -i eth2 -f "host 10.10.3.45 and port 53" -w dns_exfil_investigation.pcapng`
2. Analyze DNS query patterns: `tshark -r dns_exfil_investigation.pcapng -Y "dns.qry.name contains \"suspect-domain.xyz\"" -T fields -e frame.time -e dns.qry.name`
3. Examine subdomain labels for encoded data (long base64-like subdomains indicate tunneling): `tshark -r dns_exfil_investigation.pcapng -Y "dns.qry.type == 16" -T fields -e dns.qry.name -e dns.txt`
4. Calculate data volume by summing query name lengths to estimate exfiltration bandwidth
5. Extract unique query names and decode base64 subdomains to recover exfiltrated content
6. Export evidence packets to a separate PCAP and generate SHA-256 hash for chain of custody

**Pitfalls**:
- Capturing unfiltered traffic on a busy network and running out of disk space before collecting relevant data
- Using display filters instead of capture filters, resulting in massive files that are slow to process
- Overlooking encrypted DNS (DoH/DoT) traffic that bypasses traditional DNS capture on port 53
- Failing to establish packet capture hash and chain of custody documentation for forensic evidence

## Output Format

```
## Traffic Analysis Report

**Case ID**: IR-2024-0847
**Capture File**: dns_exfil_investigation.pcapng
**SHA-256**: a3f2b8c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
**Duration**: 2024-03-15 14:00:00 to 14:45:00 UTC
**Source Interface**: eth2 (VLAN 30 span port)

### Findings

**1. DNS Tunneling Confirmed**
- Source: 10.10.3.45
- Destination DNS: 8.8.8.8 (forwarded to ns1.suspect-domain.xyz)
- Query volume: 9,247 queries in 45 minutes (205/min vs 15/min baseline)
- Average subdomain label length: 63 characters (base64-encoded data)
- Estimated data exfiltrated: ~2.3 MB via TXT record responses

**2. Indicators of Compromise**
- Domain: suspect-domain.xyz (registered 3 days prior)
- Nameserver: ns1.suspect-domain.xyz (203.0.113.50)
- Query pattern: TXT record requests with base64-encoded subdomains
- Response pattern: TXT records containing base64-encoded payloads
```
