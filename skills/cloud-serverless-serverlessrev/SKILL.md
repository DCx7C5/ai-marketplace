---
name: cloud-serverless-serverlessrev
description: - When auditing serverless applications before production deployment - When investigating potential data exposure through function environment variables or logs - When assessing the blast radius of a compromised serverless function execution role - When compliance reviews require documentation of serverless security controls - When building secure-
domain: cybersecurity
---
---|------------|
| Execution Role | IAM role assumed by a serverless function during execution that defines what AWS/cloud resources the function can access |
| Event Injection | Serverless-specific attack where untrusted data in the event trigger payload is used unsafely in function logic |
| Function URL | Direct HTTP(S) endpoint for invoking Lambda functions without API Gateway, which may be configured without authentication |
| Cold Start | Initial function execution that includes container provisioning, during which security agents and extensions must initialize |
| Resource-Based Policy | Policy attached to the function itself that defines who can invoke it, separate from the execution role |
| Secrets Manager Integration | Pattern of retrieving sensitive configuration from a secrets management service rather than storing in environment variables |

## Tools & Systems

- **AWS Lambda**: Primary serverless compute platform with execution roles, layers, and resource policies
- **Checkov**: Static analysis tool for infrastructure-as-code with serverless-specific security policies
- **Prowler**: Cloud security tool with Lambda-specific checks for permissions, public access, and runtime versions
- **Bandit**: Python static analysis tool for detecting security issues in function source code
- **OWASP Serverless Top 10**: Security risk framework specific to serverless architectures

## Common Scenarios

### Scenario: Lambda Function with Admin Role Leaking Secrets via Environment Variables

**Context**: A security review discovers a Lambda function with `AdministratorAccess` execution role and database credentials stored in plaintext environment variables visible in CloudWatch logs.

**Approach**:
1. Enumerate the function's execution role and discover `AdministratorAccess` managed policy
2. Check environment variables and find `DB_PASSWORD`, `API_KEY`, and `STRIPE_SECRET_KEY` in plaintext
3. Review CloudWatch logs and find credentials printed in debug log statements
4. Create a scoped IAM policy granting only the specific DynamoDB and S3 actions needed
5. Migrate secrets to AWS Secrets Manager and update function to retrieve at runtime
6. Remove debug logging that outputs sensitive data
7. Rotate all exposed credentials and enable Lambda function encryption with KMS

**Pitfalls**: Changing a function's execution role can break it if the new role is too restrictive. Test in a staging environment first. Environment variable changes trigger a new function version, so ensure aliases and triggers are updated. Secrets Manager calls add latency; cache secrets within the execution context to avoid per-invocation lookups.

## Output Format

```
Serverless Function Security Review
=======================================
Account: 123456789012
Functions Reviewed: 34
Review Date: 2026-02-23

CRITICAL FINDINGS:
[SRVL-001] Overly Permissive Execution Role
  Function: payment-processor
  Role: AdministratorAccess (full AWS access)
  Required Permissions: DynamoDB:PutItem, S3:GetObject (2 actions)
  Remediation: Create scoped policy with only required permissions

[SRVL-002] Secrets in Environment Variables
  Function: payment-processor
  Variables: DB_PASSWORD, STRIPE_SECRET_KEY, API_KEY
  Risk: Visible in console, API, and CloudWatch logs
  Remediation: Migrate to Secrets Manager, remove from env vars

SUMMARY:
  Functions with admin roles:           3 / 34
  Functions with secrets in env vars:   8 / 34
  Functions with deprecated runtimes:   5 / 34
  Functions with public access:         2 / 34
  Functions without VPC:               28 / 34
  Functions with wildcard permissions: 12 / 34
```