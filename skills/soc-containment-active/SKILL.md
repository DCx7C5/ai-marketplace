---
name: soc-containment-active
description: - A confirmed intrusion is in progress with an active adversary on the network - Malware is spreading laterally across endpoints or servers - A compromised account is being used for unauthorized access to systems - Ransomware encryption has been detected and is actively propagating - An attacker has established command-and-control communications fr
domain: cybersecurity
---
---|------------|
| **Short-Term Containment** | Immediate actions to stop active adversary operations; typically network isolation and credential disablement |
| **Long-Term Containment** | Sustainable measures allowing continued investigation while preventing adversary re-access |
| **KRBTGT Double Reset** | Resetting the KRBTGT password twice to invalidate all existing Kerberos tickets including golden tickets |
| **Network Containment** | EDR feature that isolates an endpoint from all network communication except the EDR management channel |
| **Lateral Movement** | Adversary technique of moving from one compromised system to another within a network using stolen credentials or exploits |
| **C2 Sinkholing** | Redirecting DNS queries for C2 domains to an internal server to prevent adversary communication and detect additional victims |
| **Microsegmentation** | Granular network access controls between workloads that limit lateral communication paths |

## Tools & Systems

- **CrowdStrike Falcon**: Endpoint containment with one-click network isolation preserving agent connectivity
- **Microsoft Defender for Endpoint**: Live response console for remote containment actions and evidence collection
- **Palo Alto Networks NGFW**: Application-aware firewall rules for C2 traffic blocking and microsegmentation
- **Velociraptor**: Open-source endpoint monitoring and response tool for artifact collection during containment
- **BloodHound**: Active Directory attack path mapping to identify potential lateral movement routes the adversary may exploit

## Common Scenarios

### Scenario: Ransomware Lateral Propagation via SMB

**Context**: EDR alerts on three file servers showing rapid file encryption. The ransomware is spreading via SMB using a compromised domain service account.

**Approach**:
1. Immediately isolate all three file servers via EDR network containment
2. Disable the compromised service account in Active Directory
3. Block SMB (TCP 445) between all server VLANs at the network switch layer
4. Deploy an emergency GPO disabling the SMB server service on non-critical endpoints
5. Capture memory from one encrypted server before it reboots
6. Search for the ransomware binary hash across all endpoints using EDR threat hunting

**Pitfalls**:
- Shutting down servers immediately, destroying volatile memory evidence
- Only disabling the known compromised account without checking for other persistence mechanisms
- Restoring from backup before confirming the adversary's access has been fully revoked

## Output Format

```
CONTAINMENT STATUS REPORT
=========================
Incident:        INC-2025-1547
Status:          CONTAINED (Short-Term)
Timestamp:       2025-11-15T15:47:00Z
Containment Lead: [Name]

ACTIONS TAKEN
Network:
- [x] 5 hosts isolated via CrowdStrike containment
- [x] C2 IP 185.220.x.x blocked at perimeter FW (rule #4521)
- [x] C2 domain evil.example[.]com sinkholed to 10.0.0.99

Identity:
- [x] jsmith account disabled
- [x] svc-backup account disabled, password rotated
- [x] admin-tier0 account disabled
- [x] KRBTGT first reset completed at 15:30 UTC

Endpoint:
- [x] Malicious hash blocked in EDR prevention policy
- [x] Malware processes terminated on all contained hosts

EVIDENCE PRESERVED
- Memory dumps: 3 of 5 hosts completed
- Event logs exported: all 5 hosts
- Network capture: running on finance VLAN

REMAINING RISKS
- Possible undiscovered implants on non-EDR endpoints (15 legacy hosts)
- KRBTGT second reset pending (scheduled 03:30 UTC +1 day)
- Adversary may have exfiltrated data before containment

BUSINESS IMPACT
- Finance file share offline (affects 42 users)
- 3 user workstations isolated (users reassigned to loaners)
- Estimated restoration: pending eradication completion
```