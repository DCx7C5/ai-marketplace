---
name: ics-ics-protocols-s7comm
description: "Ics Ics Protocols S7Comm."
domain: cybersecurity
---

|
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
