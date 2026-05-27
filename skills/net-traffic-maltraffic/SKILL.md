---
name: net-traffic-maltraffic
description: "Net Traffic Maltraffic."
domain: cybersecurity
---

|
| **Beaconing** | Regular periodic connections from malware to C2 server, identifiable by consistent time intervals and packet sizes |
| **JA3/JA3S** | TLS fingerprinting method creating a hash from ClientHello/ServerHello parameters to uniquely identify malware TLS implementations |
| **DGA (Domain Generation Algorithm)** | Algorithm generating pseudo-random domain names that malware queries to locate C2 servers, evading static domain blocklists |
| **DNS Tunneling** | Encoding data in DNS queries and responses to establish a C2 channel or exfiltrate data through DNS infrastructure |
| **Fast Flux** | DNS technique rapidly rotating IP addresses for a domain to avoid takedown and distribute C2 across many compromised hosts |
| **SNI (Server Name Indication)** | TLS extension revealing the hostname the client is connecting to; visible even in encrypted HTTPS connections |
| **Network Signature** | Suricata/Snort rule matching specific patterns in network traffic (headers, payloads, timing) to detect malicious communications |

## Tools & Systems

- **Wireshark**: Open-source packet analyzer for deep interactive inspection of network traffic at the protocol level
- **Zeek**: Network analysis framework generating structured metadata logs (conn, dns, http, ssl) from live or captured traffic
- **Suricata**: High-performance network IDS/IPS for signature-based detection with Lua scripting for custom detection logic
- **NetworkMiner**: Network forensic analysis tool for extracting files, images, and credentials from PCAP files
- **Scapy**: Python packet manipulation library for programmatic packet analysis, beacon detection, and protocol decoding

## Common Scenarios

### Scenario: Decoding a Custom Binary C2 Protocol

**Context**: Malware communicates with its C2 server using a custom binary protocol over TCP port 8443. Standard HTTP analysis yields no results. The protocol structure needs to be reverse engineered from the PCAP.

**Approach**:
1. Filter the PCAP for TCP port 8443 conversations and follow the TCP stream
2. Identify the message framing (length prefix, delimiter, fixed-size headers)
3. Compare multiple messages to identify static header fields vs variable data fields
4. Cross-reference with reverse engineering findings from Ghidra (if the binary was analyzed)
5. Write a Wireshark dissector or Scapy parser for the custom protocol
6. Create Suricata rules matching the static header bytes for network detection
7. Document the full protocol specification for threat intelligence sharing

**Pitfalls**:
- Analyzing only the first few packets; some C2 protocols change behavior after initial handshake
- Not decrypting TLS traffic when the sandbox has MITM capabilities
- Confusing legitimate CDN or cloud traffic with C2 (validate destination IPs)
- Missing C2 traffic that uses DNS or ICMP instead of TCP/UDP

## Output Format

```
MALWARE NETWORK TRAFFIC ANALYSIS
===================================
PCAP File:        malware_sandbox.pcap
Duration:         300 seconds
Total Packets:    12,847
Total Bytes:      4.2 MB

DNS ACTIVITY
Total Queries:    47
DGA Detected:     Yes (23 high-entropy queries to .com TLD)
Tunneling:        No
Resolved C2:      update.malicious[.]com -> 185.220.101[.]42

C2 COMMUNICATION
Protocol:         HTTPS (TLS 1.2)
Server:           185.220.101[.]42:443
SNI:              update.malicious[.]com
JA3 Hash:         a0e9f5d64349fb13191bc781f81f42e1
Beacon Interval:  60.2s ± 6.8s (11.3% jitter)
Total Sessions:   237
Data Sent:        147 MB
Data Received:    2.3 MB
Certificate:      CN=update.malicious[.]com (self-signed, expired)

PAYLOAD DOWNLOADS
GET /payload.dll from compromised-site[.]com
  Size: 98,304 bytes
  SHA-256: abc123def456...
  Content-Type: application/octet-stream

EXFILTRATION
Method:           HTTPS POST to /gate.php
Content-Type:     application/octet-stream
Average Size:     15,432 bytes per request
Total Volume:     147 MB over 4 hours

SURICATA ALERTS
[1:2028401] ET MALWARE Generic C2 Beacon Pattern
[1:2028500] ET POLICY Self-Signed Certificate

GENERATED SIGNATURES
SID 9000001: MalwareX HTTP beacon pattern
SID 9000002: MalwareX DNS C2 domain
SID 9000003: MalwareX JA3 TLS fingerprint
```
