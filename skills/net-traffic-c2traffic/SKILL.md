---
name: net-traffic-c2traffic
description: "| | **Beaconing** | Periodic check-in communication from malware to C2 server at regular intervals, often with jitter to avoid pattern detection | | **Jitter** | Randomization applied to beacon interval (e."
domain: cybersecurity
---

|
| **Beaconing** | Periodic check-in communication from malware to C2 server at regular intervals, often with jitter to avoid pattern detection |
| **Jitter** | Randomization applied to beacon interval (e.g., 60s +/- 15%) to make the timing pattern less predictable and harder to detect |
| **Malleable C2** | Cobalt Strike feature allowing operators to customize all aspects of C2 traffic (URIs, headers, encoding) to mimic legitimate services |
| **Dead Drop** | Intermediate location (paste site, cloud storage, social media) where C2 commands are posted for the malware to retrieve |
| **Domain Fronting** | Using a trusted CDN domain in the TLS SNI while routing to a different backend, making C2 traffic appear to go to a legitimate service |
| **Fast Flux** | Rapidly changing DNS records for C2 domains to distribute across many IPs and resist takedown efforts |
| **C2 Framework** | Software toolkit providing C2 server, implant generator, and operator interface (Cobalt Strike, Metasploit, Sliver, Covenant) |

## Tools & Systems

- **Wireshark**: Packet analyzer for detailed C2 protocol analysis at the packet level
- **RITA (Real Intelligence Threat Analytics)**: Open-source tool analyzing Zeek logs for beacon detection and DNS tunneling
- **CobaltStrikeParser**: Tool extracting Cobalt Strike beacon configuration from samples and memory dumps
- **JA3/JA3S**: TLS fingerprinting method for identifying C2 frameworks by their TLS implementation characteristics
- **Shodan/Censys**: Internet scanning platforms for mapping C2 infrastructure and identifying related servers

## Common Scenarios

### Scenario: Reverse Engineering a Custom C2 Protocol

**Context**: A malware sample communicates with its C2 server using an unknown binary protocol over TCP port 8443. The protocol needs to be decoded to understand the command set and build detection signatures.

**Approach**:
1. Filter PCAP for TCP port 8443 conversations and extract the TCP streams
2. Analyze the first few exchanges to identify the handshake/authentication mechanism
3. Map the message structure (length prefix, type field, payload encoding)
4. Cross-reference with Ghidra disassembly of the send/receive functions in the malware
5. Identify the command dispatcher and document each command code's function
6. Build a protocol decoder in Python for ongoing traffic analysis
7. Create Suricata rules matching the protocol handshake or static header bytes

**Pitfalls**:
- Assuming the protocol is static; some C2 frameworks negotiate encryption during the handshake
- Not capturing enough traffic to see all command types (some commands are rare)
- Missing fallback C2 channels (DNS, ICMP) that activate when the primary channel fails
- Confusing encrypted payload data with the protocol framing structure

## Output Format

```
C2 COMMUNICATION ANALYSIS REPORT
===================================
Sample:           malware.exe (SHA-256: e3b0c44...)
C2 Framework:     Cobalt Strike 4.9

BEACON CONFIGURATION
C2 Server:        hxxps://185.220.101[.]42/updates
Beacon Type:      HTTPS (reverse)
Sleep:            60 seconds
Jitter:           15%
User-Agent:       Mozilla/5.0 (Windows NT 10.0; Win64; x64)
URI (GET):        /dpixel
URI (POST):       /submit.php
Watermark:        1234567890

PROTOCOL ANALYSIS
Transport:        HTTPS (TLS 1.2)
JA3 Hash:         a0e9f5d64349fb13191bc781f81f42e1
Certificate:      CN=Microsoft Update (self-signed)
Encoding:         Base64 with XOR key 0x69
Command Format:   [4B length][4B command_id][payload]

COMMAND SET
0x01 - Sleep          Change beacon interval
0x02 - Shell          Execute cmd.exe command
0x03 - Download       Transfer file from C2
0x04 - Upload         Exfiltrate file to C2
0x05 - Inject         Process injection
0x06 - Keylog         Start keylogger
0x07 - Screenshot     Capture screen

INFRASTRUCTURE
Primary:          185.220.101[.]42 (AS12345, Hosting Co, NL)
Failover:         91.215.85[.]17 (AS67890, VPS Provider, RU)
DNS:              update.malicious[.]com -> 185.220.101[.]42
Registrar:        NameCheap
Registration:     2025-09-01

DETECTION SIGNATURES
SID 9000010:      HTTP beacon pattern
SID 9000011:      JA3 TLS fingerprint
SID 9000013:      C2 certificate match
```
