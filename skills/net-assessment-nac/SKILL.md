---
name: net-assessment-nac
description: - Enforcing identity-based network access where only authenticated and compliant devices connect to the network - Implementing zero-trust networking at the access layer with dynamic VLAN assignment based on user role - Quarantining non-compliant devices that fail endpoint posture checks (missing patches, disabled AV) - Meeting compliance requiremen
domain: cybersecurity
---
---|------------|
| **802.1X** | IEEE standard for port-based network access control that authenticates devices before granting network access via EAP and RADIUS |
| **RADIUS** | Remote Authentication Dial-In User Service protocol used by network devices to authenticate users and receive authorization attributes (VLAN, ACL) |
| **MAB (MAC Authentication Bypass)** | Fallback authentication method that uses a device's MAC address as credentials for devices that cannot run an 802.1X supplicant |
| **EAP-PEAP** | Protected Extensible Authentication Protocol that wraps EAP in a TLS tunnel, commonly used with MSCHAPv2 for username/password authentication |
| **Posture Assessment** | Evaluation of endpoint compliance status (OS patches, antivirus, encryption) before granting full network access |
| **Dynamic VLAN Assignment** | RADIUS-driven automatic VLAN placement based on user identity, group membership, or device type, eliminating static port-based VLAN configuration |

## Tools & Systems

- **FreeRADIUS**: Open-source RADIUS server supporting EAP-TLS, PEAP, LDAP integration, and dynamic VLAN assignment
- **PacketFence**: Open-source NAC solution providing 802.1X integration, posture assessment, captive portal, and device registration
- **Cisco ISE**: Enterprise NAC platform with profiling, posture, guest management, and TrustSec integration
- **wpa_supplicant**: Open-source 802.1X supplicant for Linux and embedded systems supporting EAP-TLS, PEAP, and TTLS
- **Microsoft NPS**: Windows Server RADIUS implementation integrating natively with Active Directory for 802.1X authentication

## Common Scenarios

### Scenario: Deploying 802.1X NAC in a Hospital Network

**Context**: A hospital needs to enforce network access control to meet HIPAA requirements. The network includes clinical workstations (domain-joined), medical devices (no 802.1X support), physician BYOD devices, and guest WiFi. The deployment must not disrupt patient care if the RADIUS server becomes unavailable.

**Approach**:
1. Deploy FreeRADIUS integrated with Active Directory for user authentication and group-based VLAN assignment
2. Configure domain-joined workstations for EAP-PEAP via Group Policy with auto-enrollment
3. Register medical devices (infusion pumps, monitors) for MAB authentication using their MAC addresses in the RADIUS database
4. Configure switches with authentication order dot1x then mab, with critical VLAN fallback to the clinical VLAN if RADIUS is unreachable
5. Deploy PacketFence captive portal for physician BYOD onboarding with limited-access VLAN
6. Configure posture checks requiring Windows Update compliance and BitLocker encryption for full access
7. Test failover scenarios by stopping RADIUS and verifying devices remain on critical VLAN without disruption

**Pitfalls**:
- Not configuring critical VLAN fallback, causing devices to lose network access when RADIUS is unavailable
- MAB MAC address databases becoming stale as medical devices are replaced or moved
- 802.1X timeouts causing delays at workstation login, especially with slow RADIUS responses
- Not testing multi-host mode on ports with IP phones and workstations daisy-chained

## Output Format

```
## NAC Deployment Report

**RADIUS Server**: freeradius-01 (10.10.100.200)
**NAC Platform**: PacketFence 13.1
**Switches Configured**: 12 access switches
**Total Ports**: 576 access ports

### Authentication Summary (24-hour)

| Auth Type | Success | Failure | Total |
|-----------|---------|---------|-------|
| 802.1X (PEAP) | 342 | 12 | 354 |
| MAB | 87 | 3 | 90 |
| Guest Portal | 23 | 5 | 28 |

### VLAN Assignment Distribution

| VLAN | Name | Assigned Devices |
|------|------|------------------|
| 10 | Corporate | 245 |
| 15 | Development | 67 |
| 20 | Finance | 30 |
| 40 | Guest | 23 |
| 50 | Medical Devices | 87 |
| 999 | Quarantine | 15 (posture fail) |

### Compliance Status
- 802.1X coverage: 100% of access ports
- Posture pass rate: 95.8% (15 devices quarantined for missing patches)
- RADIUS failover tested: Successful (critical VLAN activated in 3 seconds)
```