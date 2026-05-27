---
name: cloud-aws-guardduty-threatdetect
description: - When establishing continuous threat detection for new or existing AWS accounts - When investigating GuardDuty findings related to compromised instances, credential abuse, or data exfiltration - When building automated incident response playbooks triggered by GuardDuty findings - When extending threat coverage to container workloads running on EKS
domain: cybersecurity
---
---|------------|
| Extended Threat Detection | GuardDuty capability that correlates multiple signals across time to detect multi-stage attacks, generating Critical-severity attack sequence findings |
| Runtime Monitoring | Protection plan that deploys a security agent to EC2 instances, ECS tasks, and EKS pods to detect runtime threats at the OS level |
| Finding Severity | Four-tier classification (Low, Medium, High, Critical) where Critical indicates confirmed multi-stage attacks requiring immediate response |
| Malware Protection | On-demand and automatic EBS volume scanning triggered by suspicious EC2 behavior to detect malware without agent installation |
| Delegated Administrator | Organization member account designated to manage GuardDuty across all accounts in an AWS Organization |
| Suppression Rule | Filter that automatically archives findings matching specific criteria to reduce noise from known benign activity |
| Threat Intelligence | IP reputation lists and domain threat feeds used by GuardDuty to identify communication with known malicious infrastructure |

## Tools & Systems

- **Amazon GuardDuty**: Core threat detection service analyzing CloudTrail, VPC Flow Logs, DNS logs, and runtime telemetry
- **Amazon EventBridge**: Serverless event bus for routing GuardDuty findings to automated response targets
- **AWS Security Hub**: Centralized security findings aggregation supporting automated remediation workflows
- **Amazon Security Lake**: OCSF-normalized data lake for long-term security log retention and cross-service correlation
- **Amazon Detective**: Graph-based investigation service that visualizes relationships between GuardDuty findings, resources, and API activity

## Common Scenarios

### Scenario: Cryptocurrency Mining Detected on ECS Cluster

**Context**: GuardDuty generates a CryptoCurrency:Runtime/BitcoinTool.B finding with High severity targeting an ECS Fargate task. Runtime Monitoring detected the execution of a mining binary within a container.

**Approach**:
1. Review the finding details to identify the ECS cluster, task definition, and container image
2. Stop the affected ECS task immediately and quarantine the container image in ECR
3. Check CloudTrail for the ecs:RegisterTaskDefinition and ecs:RunTask calls to identify who deployed the malicious image
4. Scan the Docker image with ECR enhanced scanning to identify the embedded mining binary
5. Review IAM credentials used to push the image and revoke compromised access
6. Update ECR image scanning policies to block images with known mining signatures

**Pitfalls**: Stopping the task without preserving the container image loses forensic evidence. Failing to trace back to the RegisterTaskDefinition API call misses the initial compromise vector.

## Output Format

```
GuardDuty Threat Detection Summary
====================================
Account: 123456789012 (production)
Region: us-east-1
Period: 2025-02-01 to 2025-02-23

CRITICAL FINDINGS (Immediate Action Required):
[CRIT-001] AttackSequence:EC2/CompromisedInstanceGroup
  - Instances: i-0abc123def, i-0def456abc
  - Attack Chain: Credential theft -> Persistence -> Crypto mining
  - First Signal: 2025-02-15T08:23:00Z
  - Duration: 4 hours across 3 stages
  - Status: Auto-isolated via Lambda

HIGH FINDINGS:
[HIGH-001] UnauthorizedAccess:IAMUser/MaliciousIPCaller
  - Principal: arn:aws:iam::123456789012:user/ci-deploy
  - Source IP: 198.51.100.42 (Tor exit node)
  - API Calls: 47 calls to ec2:RunInstances
  - Status: Access key deactivated

[HIGH-002] CryptoCurrency:Runtime/BitcoinTool.B
  - Resource: ECS Task arn:aws:ecs:us-east-1:123456789012:task/cluster/task-id
  - Image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/app:v2.1
  - Process: /tmp/.hidden/xmrig --pool stratum+tcp://pool.example.com:3333
  - Status: Task stopped, image quarantined

STATISTICS:
  Total Findings: 23
  Critical: 1 | High: 3 | Medium: 8 | Low: 11
  Auto-Remediated: 4
  Pending Investigation: 2
```