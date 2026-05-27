---
name: ics-ics-protocols-modbus-monitor
description: - Monitoring OT/ICS networks for unauthorized Modbus commands targeting PLCs, RTUs, or HMIs - Detecting reconnaissance activity such as Modbus device enumeration (function code 43, Read Device Identification) - Identifying unauthorized write operations (function codes 05, 06, 15, 16) to coils and holding registers that could alter physical process 
domain: cybersecurity
---
---|------------|
| **Modbus TCP** | An application-layer protocol encapsulating Modbus frames in TCP/IP, communicating on port 502. It uses a 7-byte MBAP header (transaction ID, protocol ID, length, unit ID) followed by the Modbus PDU containing the function code and data. |
| **Function Code** | A single-byte identifier in the Modbus PDU specifying the operation: read coils (01), read discrete inputs (02), read holding registers (03), read input registers (04), write single coil (05), write single register (06), write multiple coils (15), write multiple registers (16), diagnostics (08), and device identification (43). |
| **MBAP Header** | Modbus Application Protocol header used in Modbus TCP. Contains Transaction ID for request-response matching, Protocol ID (always 0x0000 for Modbus), Length of remaining bytes, and Unit Identifier for addressing slaves behind gateways. |
| **Holding Register** | A 16-bit read/write register in a Modbus slave addressed at range 40001-49999 (protocol address 0-9998). Used for setpoints, configuration, and control values that can be written by the master. Primary target for process manipulation attacks. |
| **Coil** | A single-bit read/write data element in a Modbus slave addressed at range 00001-09999. Controls discrete outputs (valves, pumps, breakers). Write operations (FC 05/15) to coils can directly affect physical equipment state. |
| **Deep Packet Inspection** | Analysis beyond TCP/IP headers into the Modbus application-layer payload to extract function codes, register addresses, and values. Required because standard firewalls only inspect IP/port, missing protocol-level attacks that use legitimate Modbus framing. |
| **Rogue Master** | An unauthorized device sending Modbus requests to slave devices. In OT environments, only designated HMI servers and engineering workstations should act as Modbus masters. A rogue master can read process data or write dangerous values to PLCs. |
| **Register Value Baseline** | The statistical profile (min, max, mean, standard deviation) of values observed in specific registers during normal operations. Deviations beyond physical process bounds indicate sensor failure or malicious manipulation. |

## Tools & Systems

- **pymodbus**: Python library for Modbus protocol implementation supporting TCP, RTU, and ASCII modes. Used for building custom Modbus clients/servers, packet parsing, and simulating master-slave communication in test environments.
- **Scapy (contrib.modbus)**: Packet manipulation framework with Modbus TCP dissector for crafting, parsing, and sniffing Modbus frames. Enables field-level access to MBAP headers, function codes, and register data in captured packets.
- **Zeek (formerly Bro)**: Network security monitor with native Modbus protocol analyzer that generates structured logs (modbus.log) for every Modbus transaction including function codes, register addresses, and exception responses.
- **Wireshark/tshark**: Network protocol analyzer with built-in Modbus TCP dissector for visual inspection of packet captures, filtering by function code (`modbus.func_code == 6`), and exporting specific fields for analysis.
- **GRFICSv2**: An open-source virtual ICS environment for security research featuring a simulated chemical process with Modbus-connected PLCs, HMI, and historian. Used for testing detection rules against realistic SCADA traffic.
- **Suricata**: Network IDS/IPS with Modbus protocol support via application-layer rules that can match on function codes, register addresses, and values for real-time alerting.

## Common Scenarios

### Scenario: Detecting Unauthorized Parameter Manipulation in a Water Treatment Plant

**Context**: A water treatment facility uses Modbus TCP to communicate between the SCADA server (10.1.1.10) and six PLCs controlling chemical dosing pumps, filtration valves, and flow meters. The security team deploys passive Modbus traffic monitoring after an industry advisory about attacks targeting water utilities.

**Approach**:
1. Deploy a network tap on the OT VLAN switch mirroring all port 502 traffic to the monitoring interface. Run Zeek with Modbus logging and the custom Python analyzer in parallel.
2. Establish a 72-hour baseline during normal operations, cataloging function code distribution, register access patterns, and polling intervals for all six master-slave pairs.
3. Baseline reveals the SCADA server only uses FC 03 (Read Holding Registers) and FC 06 (Write Single Register) to PLC-3 (chemical dosing), with writes occurring 2-4 times per day matching operator shift changes.
4. On day 5, the analyzer detects FC 16 (Write Multiple Registers) from 10.1.1.10 to PLC-3, a function code never seen in the baseline. The write targets registers 40050-40055, which control chlorine dosing rates.
5. Seconds later, a second alert fires: the chlorine dosing setpoint in register 40050 changed from 2.5 mg/L to 25.0 mg/L, exceeding the safe maximum of 4.0 mg/L defined in the register value limits.
6. Cross-referencing with IT network logs reveals the SCADA server was accessed via Remote Desktop from an unauthorized VPN connection 20 minutes before the anomalous Modbus traffic.
7. The operations team is notified, the chemical dosing PLC is placed in manual override, and the incident response team isolates the compromised SCADA server.

**Pitfalls**:
- Relying solely on IT-side network monitoring (firewall logs, IDS) that does not inspect Modbus application-layer content and would see only a normal TCP connection on port 502
- Not defining per-register safe operating ranges, which would miss the dangerous dosing rate change despite detecting the unusual function code
- Setting the baseline period too short (e.g., 4 hours) and missing legitimate but infrequent write operations that occur only during shift changes or maintenance windows
- Failing to correlate OT network anomalies with IT network events, missing the RDP session that was the actual attack vector

### Scenario: Identifying Modbus Device Enumeration from a Compromised Engineering Workstation

**Context**: A manufacturing plant's SOC observes unusual network activity from an engineering workstation (10.1.2.20) that is authorized for PLC programming. The OT security team uses Modbus traffic monitoring to determine if the workstation is being used for reconnaissance.

**Approach**:
1. Filter Modbus traffic logs for all activity from 10.1.2.20 over the past 24 hours and compare against the baseline communication profile for that workstation.
2. Baseline shows 10.1.2.20 communicates with PLC-1 (10.1.1.50) only during scheduled maintenance windows using FC 03 and FC 06, approximately 200 packets per session.
3. Anomaly detection identifies 10.1.2.20 sent FC 43 (Read Device Identification) to 15 different IP addresses on the OT VLAN within a 10-minute window, none of which it has previously communicated with.
4. Further analysis shows FC 03 read requests to register ranges 0-9999 in blocks of 125 registers per request, systematically mapping the entire register space of each PLC contacted.
5. The engineering workstation is isolated, forensic imaging initiated, and all Modbus communication from that IP is blocked at the OT firewall. The device identification responses captured reveal the PLC firmware versions that the attacker obtained.

**Pitfalls**:
- Not flagging the engineering workstation because it is in the authorized masters list, missing that its communication pattern deviated drastically from its baseline profile
- Not detecting sequential register scanning because each individual read request is a valid FC 03 operation; only the aggregate pattern reveals the reconnaissance
- Blocking the workstation before capturing forensic evidence of the attack scope and exfiltrated data

## Output Format

```
## Modbus Traffic Anomaly Report

**Monitoring Period**: 2026-03-15 00:00:00 UTC to 2026-03-15 23:59:59 UTC
**Network Segment**: OT VLAN 10 (10.1.1.0/24)
**Packets Analyzed**: 2,847,320
**Anomalies Detected**: 4

---
### Alert 1: Unauthorized Write Operation

**Timestamp**: 2026-03-15 14:23:17 UTC
**Severity**: CRITICAL
**Source**: 10.1.2.20 (Engineering Workstation)
**Destination**: 10.1.1.52 (PLC-3 Chemical Dosing)
**Function Code**: 16 (Write Multiple Registers)
**Registers**: 40050-40055
**Values Written**: [250, 100, 0, 1, 3600, 1]
**Baseline**: FC 16 never observed for this source-destination pair

**Context**: Register 40050 (Chlorine Dosing Rate) changed from 25 to 250
(safe range: 10-40). Register 40054 (Dosing Timer) changed from 1800 to 3600.
Combined effect would double chlorine concentration over extended period.

**Recommended Action**: Immediately verify physical process state. Isolate
source device. Check register values against expected setpoints with
plant operator.

domain: cybersecurity
---
### Alert 2: Device Enumeration Detected

**Timestamp**: 2026-03-15 14:20:05 to 14:20:47 UTC
**Severity**: HIGH
**Source**: 10.1.2.20
**Targets**: 10.1.1.50, 10.1.1.51, 10.1.1.52, 10.1.1.53, 10.1.1.54 (+10 more)
**Function Code**: 43 (Read Device Identification)
**Baseline**: FC 43 never observed from this source

**Context**: Sequential scanning of 15 devices in 42 seconds. Device
identification responses reveal PLC vendor, model, and firmware versions
for all scanned devices.

**Recommended Action**: Investigate source workstation for compromise
indicators. Block FC 43 from non-engineering subnets at OT firewall.
```