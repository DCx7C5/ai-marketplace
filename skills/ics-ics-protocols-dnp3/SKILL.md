---
name: ics-ics-protocols-dnp3
description: - When monitoring SCADA systems in the energy sector where DNP3 is the primary protocol - When building detection rules for DNP3-based attacks against RTUs and substations - When investigating suspected unauthorized control commands sent via DNP3 - When deploying IDS with DNP3 deep packet inspection at utility substations - When responding to alert
domain: cybersecurity
---
DNP3 SESSION SUMMARY ---")
        for key, session in self.sessions.items():
            print(f"\n  {key}")
            print(f"    Packets: {session['packet_count']}")
            funcs = [DNP3_FUNCTIONS.get(f, f"0x{f:02x}") for f in session["function_codes"]]
            print(f"    Functions: {', '.join(funcs)}")
            print(f"    Control Commands: {session['control_commands']}")
            print(f"    File Operations: {session['file_operations']}")
            print(f"    Restart Commands: {session['restarts']}")

        if self.alerts:
            print(f"\n--- ALERTS ---")
            for alert in self.alerts:
                print(f"\n  [{alert['severity']}] {alert['type']}")
                print(f"    {alert['src']} -> {alert['dst']}")
                print(f"    Function: {alert['function']}")
                print(f"    Detail: {alert['description']}")
                print(f"    MITRE ICS: {alert.get('mitre', 'N/A')}")

if __name__ == "__main__":
    detector = DNP3AnomalyDetector(
        baseline_file=sys.argv[2] if len(sys.argv) > 2 else None
    )

    if len(sys.argv) >= 2:
        print(f"[*] Analyzing: {sys.argv[1]}")
        packets = rdpcap(sys.argv[1])
        for pkt in packets:
            detector.analyze_packet(pkt)
        detector.generate_report()
    else:
        print("Usage: python dnp3_detector.py <capture.pcap> [baseline.json]")
```

## Key Concepts

| Term | Definition |
|------|------------|
| DNP3 | Distributed Network Protocol version 3, the predominant SCADA protocol in the energy sector for communication between masters and outstations |
| Outstation | DNP3 slave device (typically an RTU or IED) that responds to master station polls and commands |
| Select-Before-Operate | DNP3 safety mechanism requiring a Select command before an Operate, preventing accidental control actions |
| Cold Restart (FC 0x0D) | DNP3 command that fully restarts an outstation, resetting all configuration -- a high-risk denial-of-service operation |
| DNP3 Secure Authentication | Optional DNP3 extension (SA v5) adding HMAC-based authentication to prevent command spoofing |
| PIPEDREAM | ICS attack framework with DNP3 capabilities for manipulating outstations and performing firmware updates |

## Output Format

```
DNP3 ANOMALY DETECTION REPORT
================================
Analysis Period: [start] to [end]
Monitoring Point: [substation/segment]

TRAFFIC SUMMARY:
  DNP3 Packets: [count]
  Unique Master-Outstation Pairs: [count]
  Control Commands: [count]
  File Operations: [count]

ALERTS:
  [CRITICAL] Unauthorized DNP3 master [IP]
  [CRITICAL] Cold restart command to outstation [addr]
  [HIGH] Unexpected control command from [IP]

RECOMMENDATIONS:
  1. Deploy DNP3 Secure Authentication (SA v5)
  2. Block unauthorized sources at firewall
  3. Enable DNP3 DPI on industrial firewall
```