---
name: ics-sector-power-grid-assess
description: - When conducting periodic cybersecurity assessments of power grid facilities per NERC CIP requirements - When assessing substation automation systems using IEC 61850 GOOSE and MMS protocols - When evaluating the security of an Energy Management System (EMS) or SCADA control center - When assessing synchrophasor (PMU) networks and wide-area monitor
domain: cybersecurity
---
{sev.upper()} ({len(findings)}) ---")
                for f in findings:
                    report.append(f"  [{f.finding_id}] {f.title}")
                    report.append(f"    {f.description[:100]}...")
                    report.append(f"    NERC CIP: {f.nerc_cip_ref}")
                    report.append(f"    Remediation: {f.remediation[:80]}...")

        return "\n".join(report)

if __name__ == "__main__":
    assessment = SubstationAssessment("Substation Alpha - 345kV")

    assessment.assess_iec61850_security({
        "goose_authentication": False,
        "mms_authentication": False,
        "station_bus_segmented": False,
        "goose_publishers": ["SEL-411L-01", "SEL-411L-02", "SEL-487E-01"],
        "mms_servers": ["SEL-3530-RTAC", "ABB-REF615-01"],
    })

    assessment.assess_remote_access({
        "direct_vendor_access": True,
    })

    print(assessment.generate_report())
```

## Key Concepts

| Term | Definition |
|------|------------|
| IEC 61850 | International standard for communication networks and systems in substations, using GOOSE for protection signaling and MMS for SCADA data |
| GOOSE | Generic Object Oriented Substation Event - multicast protocol for fast peer-to-peer protection signaling between IEDs (< 4ms trip time) |
| MMS | Manufacturing Message Specification - client/server protocol for reading/writing IED data and operating circuit breakers |
| IEC 62351 | Security standard series for power system communication protocols providing authentication and encryption for IEC 61850, DNP3, and IEC 104 |
| ICCP/TASE.2 | Inter-Control Center Communications Protocol for data exchange between control centers of different utilities |
| Synchrophasor (PMU) | Phasor Measurement Unit providing time-synchronized voltage/current measurements at 30-60 samples/second for wide-area monitoring |

## Tools & Systems

- **Dragos Platform**: OT security platform with specific threat intelligence on power grid-targeting groups (ELECTRUM, KAMACITE)
- **SEL-3620 Ethernet Security Gateway**: Substation security device providing encryption, access control, and intrusion detection
- **GRIDsure**: Power grid cybersecurity assessment framework by Idaho National Laboratory
- **Wireshark with IEC 61850 Dissector**: Protocol analysis for GOOSE and MMS traffic in substations

## Output Format

```
Power Grid Cybersecurity Assessment Report
=============================================
Facility: [Name and Type]
NERC Registration: [Entity ID]
BES Impact Rating: [High/Medium/Low]

SUBSTATION FINDINGS: [N]
EMS/SCADA FINDINGS: [N]
COMMUNICATION FINDINGS: [N]

NERC CIP COMPLIANCE:
  CIP-002: [Status]
  CIP-005: [Status]
  CIP-007: [Status]
```