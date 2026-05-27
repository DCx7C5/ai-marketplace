---
name: soc-containment-cloud
description: Cloud incident containment requires cloud-native approaches that differ significantly from traditional on-premises response. Containment procedures must leverage platform-specific controls including security groups, IAM policies, network ACLs, and service-level isolation to restrict compromised resources while preserving forensic evidence. Accordin
domain: cybersecurity
---
--------|-------------------|
| T1078 - Valid Accounts | Disable accounts, revoke tokens |
| T1530 - Data from Cloud Storage | Lock down bucket/storage policies |
| T1537 - Transfer to Cloud Account | Block cross-account access |
| T1578 - Modify Cloud Compute | Isolate instances, snapshot disks |
| T1552 - Unsecured Credentials | Rotate all access keys and secrets |

## References

- [Sygnia: Cloud Incident Response Best Practices](https://www.sygnia.co/blog/incident-response-to-cloud-security-incidents-aws-azure-and-gcp-best-practices/)
- [Unit 42: Responding to Cloud Incidents](https://unit42.paloaltonetworks.com/responding-to-cloud-incidents/)
- [Wiz: Cloud Incident Response Checklist](https://www.wiz.io/academy/incident-response-checklist)
- [Microsoft Cloud Security Benchmark - IR](https://learn.microsoft.com/en-us/security/benchmark/azure/mcsb-incident-response)