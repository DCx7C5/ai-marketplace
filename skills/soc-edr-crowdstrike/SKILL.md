---
name: soc-edr-crowdstrike
description: "Soc Edr Crowdstrike."
domain: cybersecurity
---

--|
| **Falcon Sensor** | Lightweight kernel-mode agent (25-30 MB) that collects endpoint telemetry and enforces prevention policies |
| **CID (Customer ID)** | Unique identifier that associates the sensor with your CrowdStrike Falcon tenant |
| **RFM (Reduced Functionality Mode)** | State where sensor operates with limited capability due to cloud connectivity loss |
| **Sensor Grouping Tags** | Labels applied during installation to auto-assign hosts to groups and policies |
| **RTR (Real-Time Response)** | Remote shell capability for incident responders to interact with endpoints through Falcon |
| **IOA (Indicators of Attack)** | Behavioral detections based on adversary techniques rather than static signatures |

## Tools & Systems

- **CrowdStrike Falcon Console**: Cloud-hosted management platform for all Falcon modules
- **Falcon SIEM Connector**: Streams detection and audit events to SIEM platforms
- **Falcon Data Replicator (FDR)**: Streams raw endpoint telemetry to S3/cloud storage for hunting
- **CrowdStrike Falcon API (OAuth2)**: RESTful API for automation, integration, and custom workflows
- **PSFalcon**: PowerShell module for CrowdStrike Falcon API automation

## Common Pitfalls

- **Missing CID during installation**: Sensor installs but never connects to Falcon cloud. Always pass CID during install, not after.
- **Proxy not configured**: In environments with web proxies, configure proxy during installation: `/install /quiet CID=<CID> APP_PROXYNAME=proxy.corp.com APP_PROXYPORT=8080`.
- **macOS System Extension blocked**: macOS requires explicit approval for kernel/system extensions. Use MDM to pre-approve CrowdStrike extensions before deployment.
- **Conflicting security products**: Running multiple EDR/AV products causes performance issues and false positives. Coordinate exclusions or remove legacy AV before Falcon deployment.
- **Sensor version pinning**: Falcon auto-updates sensors by default. Pin sensor versions in the console for change-controlled environments before testing new versions.
