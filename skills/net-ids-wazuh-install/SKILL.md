---
name: net-ids-wazuh-install
description: Use this skill when: - Deploying HIDS agents (Wazuh, OSSEC, AIDE) across Windows and Linux endpoints - Configuring file integrity monitoring (FIM) for compliance (PCI DSS 11.5, NIST SI-7) - Monitoring system configuration changes, rootkit detection, and security policy violations - Integrating HIDS alerts with SIEM platforms for centralized monitor
domain: cybersecurity
---
---|-----------|
| **HIDS** | Host-based Intrusion Detection System; monitors individual endpoints for malicious activity |
| **FIM** | File Integrity Monitoring; detects unauthorized changes to files by comparing cryptographic hashes |
| **Syscheck** | Wazuh/OSSEC module for file integrity monitoring and registry monitoring |
| **Rootcheck** | Wazuh/OSSEC module for rootkit and malware detection |
| **Active Response** | Automated defensive action triggered by HIDS alert (IP block, account disable) |
| **CDB List** | Constant Database list used for custom lookups in Wazuh rules |

## Tools & Systems

- **Wazuh**: Open-source HIDS platform (fork of OSSEC) with manager, agent, and dashboard
- **OSSEC**: Original open-source HIDS (predecessor to Wazuh)
- **AIDE (Advanced Intrusion Detection Environment)**: Standalone file integrity checker for Linux
- **Tripwire**: Commercial file integrity monitoring solution
- **Samhain**: Open-source HIDS focused on file integrity and log monitoring

## Common Pitfalls

- **Monitoring too many directories**: FIM on entire filesystems generates excessive alerts. Focus on critical system binaries, configuration files, and web roots.
- **Not excluding noisy files**: Frequently changing files (logs, temp, caches) generate false positive FIM alerts. Maintain exclusion lists.
- **Ignoring baseline establishment**: First FIM scan creates a baseline. Changes detected before baseline stabilization are noise, not threats. Allow 48 hours for baseline.
- **Active response without testing**: Auto-blocking IPs or disabling accounts can cause outages. Test active response rules in a non-production environment first.
- **Agent enrollment failures**: Agents must successfully enroll with the manager before monitoring begins. Verify firewall rules allow port 1514 and 1515 traffic.