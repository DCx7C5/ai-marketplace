---
name: net-assessment-net
description: "Net Assessment Net."
domain: cybersecurity
---

|
| Purdue Reference Model | Hierarchical architecture model (Levels 0-5) for organizing industrial control systems, defining security zones from physical process to enterprise IT |
| IEC 62443 | International standard series for industrial automation and control systems (IACS) security, defining security levels, zones, conduits, and security requirements |
| Zone | A grouping of logical or physical assets that share common security requirements, defined by IEC 62443-3-2 |
| Conduit | A logical grouping of communication channels connecting two or more zones, subject to common security policies |
| SCADA | Supervisory Control and Data Acquisition - system architecture for high-level process supervisory management of industrial processes |
| DCS | Distributed Control System - control system architecture where control elements are distributed throughout the system |
| Air Gap | Physical isolation of OT networks from IT/internet, increasingly replaced by managed conduits with firewalls and data diodes |
| Safety Instrumented System (SIS) | Independent system designed to bring a process to a safe state when a hazardous condition is detected |

## Tools & Systems

- **Nozomi Networks Guardian**: Passive OT network monitoring platform providing asset discovery, vulnerability assessment, and anomaly detection for industrial environments
- **Dragos Platform**: OT cybersecurity platform with asset visibility, threat detection, and vulnerability management designed for critical infrastructure
- **Claroty xDome**: Cyber-physical systems protection platform providing comprehensive asset inventory and risk scoring across OT, IoT, and IIoT
- **Wireshark/tshark**: Network protocol analyzer with industrial protocol dissectors for Modbus, DNP3, S7comm, EtherNet/IP, OPC UA, and BACnet
- **Nmap with OT scripts**: Network scanner with NSE scripts for OT protocol enumeration (use only on Level 2+ with authorization)
- **Grassmarlin**: NSA-developed passive OT network mapping tool for identifying SCADA/ICS network topology

## Common Scenarios

### Scenario: Flat OT Network with No Segmentation

**Context**: A water utility has all OT devices on a single VLAN. Passive network monitoring reveals HMIs, PLCs, historians, and a domain controller all sharing the same Layer 2 broadcast domain. There is no DMZ between the corporate network and the OT environment.

**Approach**:
1. Deploy passive monitoring on the SPAN port to capture a complete communication baseline over 2-4 weeks
2. Map all device-to-device communication flows with protocols and data volumes
3. Classify assets into Purdue levels based on their function and communication patterns
4. Design zone architecture with VLANs and inter-zone firewalls per IEC 62443-3-2
5. Prioritize DMZ creation between Level 3 and Level 4 as the highest-impact segmentation
6. Present segmentation plan with migration phases that avoid production disruption

**Pitfalls**: Active scanning PLCs during production can cause communication timeouts and process disruptions. Implementing segmentation without a complete traffic baseline will break legitimate control system communications. Relying solely on network-layer firewalls without industrial protocol inspection leaves Modbus/TCP and EtherNet/IP write commands unchecked.

## Output Format

```
OT Network Security Assessment Report
=======================================
Facility: [Facility Name]
Assessment Date: YYYY-MM-DD
Standard: IEC 62443-3-3 / NIST SP 800-82r3

EXECUTIVE SUMMARY:
  [2-3 sentence overview of findings and risk level]

ASSET INVENTORY:
  Level 0-1: [count] field devices
  Level 2:   [count] control systems
  Level 3:   [count] operations systems
  Level 3.5: [count] DMZ systems
  Level 4:   [count] enterprise systems

FINDINGS BY SEVERITY:
  Critical: [count] (immediate action required)
  High:     [count] (30-day remediation)
  Medium:   [count] (90-day remediation)
  Low:      [count] (next maintenance window)

DETAILED FINDINGS:
  [OT-NNN] Finding Title
    Severity: Critical|High|Medium|Low
    Affected Assets: [list]
    IEC 62443 Reference: [section]
    NIST 800-82r3 Reference: [section]
    Description: [technical detail]
    Impact: [operational and safety impact]
    Remediation: [specific technical remediation steps]
```
