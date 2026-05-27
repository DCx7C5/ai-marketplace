---
name: vuln-remediation-bucket
description: - When AWS Config or Security Hub reports S3 buckets with public access or missing encryption - When a security scan reveals S3 bucket policies granting access to Principal "*" (everyone) - When preparing for a data protection audit requiring evidence of storage security controls - When responding to a data exposure incident involving publicly acce
domain: cybersecurity
---
---|------------|
| S3 Block Public Access | Four account-level and bucket-level settings that override any policy or ACL granting public access to S3 resources |
| Bucket Policy | JSON-based resource policy attached to an S3 bucket defining who can access what objects under which conditions |
| ACL (Access Control List) | Legacy S3 access mechanism that grants permissions at the bucket or object level; should be disabled via BucketOwnerEnforced |
| BucketOwnerEnforced | Ownership control setting that disables all ACLs on a bucket, making the bucket owner the sole authority for access control |
| Server-Side Encryption | Automatic encryption of objects at rest using AES-256 (SSE-S3), AWS KMS (SSE-KMS), or customer-provided keys (SSE-C) |
| VPC Endpoint | Private connection between a VPC and S3 that restricts bucket access to traffic originating from within the VPC |
| S3 Access Analyzer | IAM Access Analyzer capability that identifies S3 buckets shared with external entities outside the account or organization |

## Tools & Systems

- **AWS Config**: Evaluates S3 bucket compliance against managed rules and triggers auto-remediation for non-compliant resources
- **Amazon Macie**: Discovers and classifies sensitive data in S3 buckets to identify which misconfigurations pose the highest data exposure risk
- **IAM Access Analyzer**: Identifies S3 buckets with policies or ACLs that grant access to external principals
- **S3 Storage Lens**: Provides organization-wide visibility into S3 usage patterns, access metrics, and security anomalies
- **Prowler**: Open-source tool that checks S3 security configurations against CIS benchmarks and best practices

## Common Scenarios

### Scenario: Data Breach from Publicly Readable S3 Bucket Containing PII

**Context**: A security researcher reports that an S3 bucket containing 273,000 bank transfer PDFs is publicly readable. The bucket was created by a developer who needed to share files with an external partner and set the ACL to public-read.

**Approach**:
1. Immediately enable Block Public Access on the specific bucket to stop the exposure
2. Revoke all public ACLs by setting BucketOwnerEnforced ownership controls
3. Audit CloudTrail and S3 access logs to determine which IP addresses accessed the exposed objects
4. Run Macie on the bucket to classify the types of PII exposed and assess regulatory notification requirements
5. Enable account-level Block Public Access to prevent recurrence across all buckets
6. Deploy an SCP preventing any principal except SecurityAdmin from modifying Block Public Access settings
7. Create a pre-signed URL mechanism or S3 Access Point for the legitimate partner sharing use case

**Pitfalls**: Enabling Block Public Access without notifying the team that set up the public access breaks their workflow. Not running access log analysis before remediation loses evidence of who accessed the exposed data.

## Output Format

```
S3 Bucket Security Remediation Report
=======================================
Account: 123456789012
Assessment Date: 2025-02-23
Buckets Scanned: 156

ACCOUNT-LEVEL CONTROLS:
  Block Public Access: ENABLED (all four settings)
  SCP Preventing Removal: DEPLOYED

CRITICAL FINDINGS (Remediated):
  [S3-001] production-uploads - Public READ via ACL
    Status: REMEDIATED - BucketOwnerEnforced applied
    Objects Exposed: 273,412
    Duration of Exposure: 47 days
    Unique External IPs Accessed: 1,247

  [S3-002] analytics-export - Public bucket policy (Principal: *)
    Status: REMEDIATED - Policy replaced with VPC endpoint restriction
    Sensitive Data (Macie): 12,400 objects with PII detected

HIGH FINDINGS:
  [S3-003] 14 buckets missing default encryption
    Status: REMEDIATED - KMS encryption enabled
  [S3-004] 8 buckets without server access logging
    Status: REMEDIATED - Logging enabled to centralized log bucket

SUMMARY:
  Buckets Remediated: 24/156
  Encryption Coverage: 100%
  Access Logging Coverage: 100%
  Block Public Access: 156/156 buckets
```

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "bucket" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist