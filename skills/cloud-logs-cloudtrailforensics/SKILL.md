---
name: cloud-logs-cloudtrailforensics
description: - When investigating suspected AWS account compromise - After detecting unauthorized API calls or credential exposure - During incident response involving cloud infrastructure - When analyzing S3 data exfiltration or IAM privilege escalation - For post-incident forensic timeline reconstruction
domain: cybersecurity
---
------|-------------|
| LookupEvents | CloudTrail API to query management events (last 90 days) |
| Athena Queries | SQL queries against CloudTrail logs in S3 for historical analysis |
| User Agent Analysis | Identify tool signatures (AWS CLI, SDK, console, custom) |
| AccessKeyId | Track activity by specific IAM access key |
| EventName | AWS API action name (e.g., GetObject, CreateUser, AssumeRole) |
| sourceIPAddress | Origin IP of API call for geolocation analysis |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| boto3 CloudTrail client | Programmatic CloudTrail event lookup |
| AWS Athena | SQL-based analysis of CloudTrail S3 logs |
| AWS CLI | Command-line CloudTrail queries |
| jq | JSON processing for CloudTrail event parsing |
| CloudTrail Lake | Advanced event data store with SQL query support |

## Output Format

```
Forensic Report: AWS-IR-[DATE]-[SEQ]
Account: [AWS Account ID]
Timeframe: [Start] to [End]
Compromised Credentials: [Access Key IDs]
Suspicious Events: [Count]
Source IPs: [List of attacker IPs]
Actions Taken: [API calls by attacker]
Data Accessed: [S3 objects, secrets, etc.]
Persistence Mechanisms: [New users, keys, roles]
```