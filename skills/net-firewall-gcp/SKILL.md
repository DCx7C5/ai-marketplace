---
name: net-firewall-gcp
description: "Net Firewall Gcp."
domain: cybersecurity
---

|
| VPC Firewall Rule | Stateful network-level access control that allows or denies traffic to and from VM instances based on IP ranges, protocols, ports, and tags |
| Hierarchical Firewall Policy | Organization or folder-level firewall policy that is evaluated before VPC-level rules and applies across all child projects |
| Network Tag | Label applied to VM instances that determines which firewall rules apply, used for targeting ingress and egress rules |
| Service Account Firewall Rule | Firewall rule that targets instances based on their attached service account, providing more secure targeting than mutable network tags |
| VPC Flow Logs | Network telemetry captured at the subnet level that records traffic metadata for monitoring, forensics, and firewall rule validation |
| Implied Rules | Default GCP firewall rules that allow egress to all destinations and deny ingress from all sources, with lowest priority (65535) |

## Tools & Systems

- **gcloud compute firewall-rules**: CLI commands for creating, listing, and managing VPC firewall rules in GCP
- **Hierarchical Firewall Policies**: Organization and folder-level policies enforcing security controls across all projects
- **VPC Flow Logs**: Subnet-level traffic logging for monitoring, troubleshooting, and validating firewall effectiveness
- **Cloud Logging**: Query engine for analyzing VPC Flow Logs and firewall rule hit counts
- **Security Command Center**: GCP-native security platform with findings for overly permissive firewall configurations

## Common Scenarios

### Scenario: Locking Down a Production VPC After Discovery of Overly Permissive Rules

**Context**: A security audit reveals that the production VPC has default-allow rules permitting SSH from `0.0.0.0/0` and unrestricted egress. SCC reports 14 firewall findings.

**Approach**:
1. Enumerate all existing rules with `gcloud compute firewall-rules list` and categorize by risk
2. Enable VPC Flow Logs on all subnets to capture baseline traffic patterns for 7 days
3. Analyze flow logs to identify legitimate traffic that needs explicit allow rules
4. Create targeted ingress rules for each application tier (web: 443, app: 8080, db: 5432)
5. Replace the SSH-from-anywhere rule with SSH-from-bastion-subnet-only
6. Implement default-deny egress and add explicit allow rules for required outbound destinations
7. Delete the overly permissive default-allow rules after verifying applications function correctly

**Pitfalls**: Deleting firewall rules without understanding traffic patterns causes outages. Always enable flow logs and analyze traffic before removing rules. Network tags can be added by anyone with compute.instances.setTags permission, making them less secure than service-account-based targeting for critical rules.

## Output Format

```
GCP VPC Firewall Audit Report
================================
Project: production-project
VPC Network: production-vpc
Audit Date: 2026-02-23

RULE INVENTORY:
  Total firewall rules: 34
  Ingress rules: 22
  Egress rules: 12
  Disabled rules: 3

CRITICAL FINDINGS:
[FW-001] SSH Open to Internet
  Rule: default-allow-ssh
  Source: 0.0.0.0/0 -> tcp:22
  Target: All instances (no tags)
  Priority: 65534
  Remediation: Restrict to bastion subnet CIDR

[FW-002] No Egress Restrictions
  Issue: Only implied allow-all-egress rule exists
  Risk: No controls on outbound data exfiltration
  Remediation: Add default-deny egress and explicit allow rules

REMEDIATION ACTIONS COMPLETED:
  Rules deleted: 3 (overly permissive defaults)
  Rules created: 8 (targeted allow rules)
  Egress deny rule: Created at priority 65534
  Flow logs enabled: 6 subnets
```
