---
name: ics-ics-historian-attack
description: - When monitoring historian servers that bridge IT and OT networks for compromise indicators - When detecting unauthorized queries or data manipulation in process historian databases - When investigating lateral movement through historian servers between IT and OT zones - When responding to alerts about exploitation of historian-specific vulnerabil
domain: cybersecurity
---
ALERTS ---")
            for alert in self.alerts:
                print(f"\n  [{alert['severity']}] {alert['type']}")
                print(f"    Time: {alert['timestamp']}")
                print(f"    Detail: {alert['details']}")
                print(f"    MITRE ICS: {alert.get('mitre', 'N/A')}")

        print(f"\n--- LATERAL MOVEMENT CHECKS ---")
        for indicator in self.check_lateral_movement_indicators():
            print(f"\n  Check: {indicator['check']}")
            print(f"    Risk: {indicator['description']}")
            print(f"    Detection: {indicator['detection']}")

if __name__ == "__main__":
    detector = HistorianAttackDetector(
        historian_type="osisoft_pi",
        historian_url="https://pi-server.plant.local",
        api_credentials={"username": "pi_reader", "password": "api_key_here"},
    )

    detector.set_baseline(
        authorized_clients=["10.10.2.10", "10.10.2.20", "10.10.3.50", "10.10.150.10"],
        authorized_query_patterns={},
    )

    detector.check_active_connections()
    detector.check_data_integrity(tags=["REACTOR_01.TEMP", "PUMP_03.FLOW"], hours_back=24)
    detector.generate_report()
```

## Key Concepts

| Term | Definition |
|------|------------|
| OT Historian | Database server (OSIsoft PI, Ignition, Wonderware) storing time-series process data from SCADA/DCS systems |
| Pivot Point | Historian's position between IT and OT networks makes it a prime target for attackers to move between zones |
| Data Replay Attack | Feeding historical data to an HMI to mask real-time process manipulation (Stuxnet technique) |
| OSIsoft PI | Most widely deployed OT historian, used by 65% of Global 500 process companies |
| Ignition | Inductive Automation SCADA platform with historian module, increasingly targeted due to Python scripting capabilities |
| CVE-2025-0921 | Ignition SCADA privileged file system vulnerability allowing escalation through malicious project files |

## Output Format

```
HISTORIAN ATTACK DETECTION REPORT
====================================
Historian: [type and hostname]
Date: YYYY-MM-DD

CONNECTION ANALYSIS:
  Authorized Clients: [count]
  Unauthorized Clients Detected: [count with IPs]

DATA INTEGRITY:
  Tags Checked: [count]
  Integrity Issues: [count]
  Flatline Detections: [count]
  Data Gaps: [count]

LATERAL MOVEMENT INDICATORS:
  Outbound PLC Connections: [found/not found]
  Unauthorized Processes: [found/not found]
  Anomalous Authentication: [found/not found]
```