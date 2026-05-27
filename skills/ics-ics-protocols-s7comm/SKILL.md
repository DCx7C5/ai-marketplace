---
name: ics-ics-protocols-s7comm
description: - When assessing the security posture of Siemens SIMATIC S7 PLC environments - When building detection rules for S7comm-based attacks against S7-300/400/1200/1500 controllers - When performing a security audit of Siemens Step 7/TIA Portal communications - When investigating suspected unauthorized access to Siemens PLC programs - When evaluating S7C
domain: cybersecurity
---
SESSION SUMMARY ---")
        for key, session in self.sessions.items():
            funcs = [S7_FUNCTIONS.get(f, f"0x{f:02x}") for f in session["functions_seen"]]
            print(f"\n  {key}")
            print(f"    Packets: {session['packets']}")
            print(f"    Functions: {', '.join(funcs)}")
            print(f"    Writes: {session['writes']}")
            print(f"    Program Downloads: {session['program_downloads']}")
            print(f"    CPU Commands: {session['cpu_commands']}")

        if self.findings:
            print(f"\n--- SECURITY FINDINGS ---")
            for f in self.findings:
                print(f"\n  [{f.severity}] {f.finding_type}")
                print(f"    Source: {f.src_ip} -> {f.dst_ip}")
                print(f"    Function: {f.function}")
                print(f"    Detail: {f.description}")
                if f.cve:
                    print(f"    Reference: {f.cve}")
                if f.recommendation:
                    print(f"    Action: {f.recommendation}")

        print(f"\n--- KNOWN VULNERABILITY ASSESSMENT ---")
        for vuln in self.check_known_vulnerabilities():
            print(f"\n  [{vuln['severity']}] {vuln['name']}")
            print(f"    CVE: {vuln['cve']}")
            print(f"    Affected: {vuln['affected']}")
            print(f"    Detail: {vuln['description']}")

if __name__ == "__main__":
    analyzer = S7commAnalyzer()
    analyzer.set_authorized_stations(["10.10.2.50", "10.10.2.51"])

    if len(sys.argv) >= 2:
        print(f"[*] Analyzing capture: {sys.argv[1]}")
        packets = rdpcap(sys.argv[1])
        for pkt in packets:
            analyzer.analyze_packet(pkt)
        analyzer.generate_report()
    else:
        print("Usage: python s7comm_analyzer.py <capture.pcap>")
        print("  Analyzes S7comm traffic for security vulnerabilities")
```

## Key Concepts

| Term | Definition |
|------|------------|
| S7comm | Siemens proprietary protocol for communication with SIMATIC S7 PLCs over TCP port 102, layered on COTP/TPKT |
| S7CommPlus | Enhanced version of S7comm used by S7-1200/1500 with integrity protection mechanisms |
| ROSCTR | Remote Operating Service Control field in S7comm header indicating PDU type (Job, Ack, Ack_Data, Userdata) |
| TIA Portal | Totally Integrated Automation Portal -- Siemens engineering software for programming S7 PLCs |
| CPU Stop (0x29) | S7comm function that halts PLC program execution, a critical denial-of-service operation |
| Program Download (0x1A) | S7comm function initiating transfer of new control logic to a PLC, representing the highest risk operation |

## Common Scenarios

### Scenario: Unauthorized PLC Program Modification

**Context**: A Dragos sensor alerts on S7comm program download traffic from an IP address that is not the authorized TIA Portal engineering workstation.

**Approach**:
1. Capture the complete S7comm session for forensic analysis
2. Identify the source host and determine if it is compromised or rogue
3. Compare the current PLC program against the last known-good backup
4. Check if the PLC CPU mode was changed (RUN to STOP to PROGRAM)
5. If the program was modified, restore from verified backup
6. Investigate the attack chain -- how did the attacker reach the S7comm network segment
7. Implement S7comm access protection (know-how protection, access passwords) on all PLCs

**Pitfalls**: S7-300/400 PLCs have no cryptographic integrity protection -- any device that can reach TCP port 102 can send commands. Do not rely solely on PLC passwords as they are transmitted in cleartext in S7comm (not S7CommPlus). Network segmentation is the primary defense.

## Output Format

```
S7COMM SECURITY ANALYSIS REPORT
===================================
Date: YYYY-MM-DD
Scope: [Network segments analyzed]

SESSION INVENTORY:
  Engineering stations: [count and IPs]
  PLCs communicating: [count and IPs]
  Unauthorized sources: [count]

CRITICAL FINDINGS:
  CPU Stop commands: [count]
  Program downloads: [count from unauthorized sources]
  Replay attack potential: [assessment]

VULNERABILITY ASSESSMENT:
  S7-300/400 (no integrity): [count of affected PLCs]
  S7-1200/1500 (S7CommPlus): [firmware assessment]
  Known CVEs applicable: [list]

RECOMMENDATIONS:
  1. [Highest priority remediation]
  2. [Network segmentation improvement]
  3. [Monitoring enhancement]
```