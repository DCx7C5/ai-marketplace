---
name: cloud-threat-cryptomining
description: "Cloud Threat Cryptomining."
domain: cybersecurity
---

|
| Cryptojacking | Unauthorized use of cloud compute resources to mine cryptocurrency, typically Monero (XMR) due to its CPU-friendly algorithm |
| Stratum Protocol | Mining pool communication protocol operating on TCP ports 3333, 4444, or custom ports, identifiable in network flow logs |
| XMRig | Open-source Monero mining software commonly found in cryptojacking attacks, often deployed as a hidden binary in containers |
| API Termination Protection | EC2 attribute that attackers enable to prevent security teams from quickly terminating compromised mining instances |
| Cost Anomaly Detection | AWS service that uses machine learning to identify unusual spending patterns that may indicate unauthorized resource usage |
| Runtime Monitoring | GuardDuty capability that deploys agents to detect process-level activity including crypto mining binary execution |
| Attack Sequence | GuardDuty Extended Threat Detection finding correlating credential theft, infrastructure deployment, and mining execution into a single Critical event |

## Tools & Systems

- **Amazon GuardDuty**: Detects cryptocurrency mining through network traffic analysis, DNS queries, and runtime process monitoring
- **AWS Cost Anomaly Detection**: Machine learning-based service identifying unexpected cost increases from mining instance deployment
- **VPC Flow Logs**: Network traffic metadata showing connections to mining pool IP addresses and ports
- **Falco**: Open-source runtime security tool for detecting crypto mining process execution in containers
- **Amazon Detective**: Graph-based investigation tool for tracing the attack path from initial access to mining deployment

## Common Scenarios

### Scenario: Compromised IAM Credentials Used for Large-Scale EC2 Mining

**Context**: Exposed IAM credentials from a public GitHub repository are used to launch 200 GPU instances across 8 AWS regions within 10 minutes. The attacker enables API termination protection and disables CloudTrail in each region.

**Approach**:
1. AWS Cost Anomaly Detection triggers an immediate alert for $15,000+ hourly EC2 spend
2. GuardDuty generates Stealth:IAMUser/CloudTrailLoggingDisabled and CryptoCurrency:EC2/BitcoinTool.B findings
3. Immediately deactivate the compromised IAM access key
4. Re-enable CloudTrail in all affected regions to restore visibility
5. Disable API termination protection on all 200 instances and terminate them
6. Create forensic snapshots of representative instances before termination
7. Review the GitHub commit history to identify and remove the exposed credentials
8. Deploy AWS Config rules preventing CloudTrail disabling and enforcing IMDSv2

**Pitfalls**: Failing to check all AWS regions for mining instances leaves active miners running in overlooked regions. Not disabling API termination protection before attempting to stop instances wastes response time.

## Output Format

```
Cryptomining Incident Response Report
=======================================
Incident ID: INC-2025-0223-CRYPTO
Detection Time: 2025-02-23T14:23:00Z
Containment Time: 2025-02-23T14:41:00Z (18 minutes)

INITIAL ACCESS:
  Vector: Exposed IAM access key in public GitHub repository
  Credential: AKIAIOSFODNN7EXAMPLE (user: ci-deploy)
  First Malicious Activity: 2025-02-23T14:12:00Z

IMPACT:
  Instances Launched: 200 (p3.2xlarge GPU instances)
  Regions Affected: 8 (us-east-1, us-west-2, eu-west-1, eu-central-1, ...)
  Estimated Cost: $4,200 (18 minutes at $15,400/hour)
  Mining Pool: stratum+tcp://pool.supportxmr.com:3333
  Cryptocurrency: Monero (XMR)

DETECTION SIGNALS:
  [14:15] GuardDuty: Stealth:IAMUser/CloudTrailLoggingDisabled (HIGH)
  [14:18] Cost Anomaly: EC2 spend 4,200% above baseline
  [14:23] GuardDuty: CryptoCurrency:EC2/BitcoinTool.B (HIGH) x 200

CONTAINMENT ACTIONS:
  [14:25] IAM access key AKIAIOSFODNN7EXAMPLE deactivated
  [14:30] CloudTrail re-enabled in all 8 regions
  [14:35] API termination protection disabled on 200 instances
  [14:41] All 200 instances terminated

REMEDIATION:
  - Compromised access key deleted
  - GitHub repository secret scanning enabled
  - AWS Config rule deployed: cloudtrail-enabled (auto-remediate)
  - SCP deployed: deny ec2:RunInstances for GPU instance types without approval
```
