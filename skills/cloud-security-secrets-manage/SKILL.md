---
name: cloud-security-secrets-manage
description: - When applications store database passwords, API keys, or certificates in environment variables or config files - When migrating from static long-lived credentials to dynamic short-lived secrets - When Kubernetes workloads need secure access to database credentials or cloud provider APIs - When compliance requirements mandate centralized credentia
domain: cybersecurity
---
---|------------|
| Dynamic Secrets | Credentials generated on-demand with automatic expiration and revocation, eliminating long-lived static credentials |
| Secret Engine | Vault component that stores, generates, or encrypts data; includes KV, database, AWS, PKI, and Transit engines |
| Auto-Unseal | Cloud KMS-based mechanism that automatically unseals Vault nodes on restart without manual key entry |
| AppRole | Machine-oriented authentication method using Role ID and Secret ID for application and CI/CD pipeline access |
| Transit Engine | Encryption-as-a-service engine that handles cryptographic operations without exposing encryption keys to applications |
| Lease | Time-bound credential with a TTL that Vault automatically revokes on expiration unless renewed |
| Namespace | Vault Enterprise feature providing tenant isolation with separate auth, secrets, and policy management |
| Response Wrapping | Technique that wraps secret responses in a single-use token to prevent man-in-the-middle exposure during delivery |

## Tools & Systems

- **HashiCorp Vault**: Core secrets management platform providing dynamic secrets, encryption, and identity-based access
- **Vault Agent Injector**: Kubernetes mutating webhook that automatically injects Vault secrets into pod volumes via sidecar containers
- **Vault CSI Provider**: Kubernetes CSI driver that mounts Vault secrets directly into pod volumes without sidecar containers
- **consul-template**: Template rendering daemon that watches Vault secrets and re-renders configuration files when secrets change
- **Vault Radar**: Secret scanning tool that detects hardcoded credentials in source code, CI/CD pipelines, and cloud configurations

## Common Scenarios

### Scenario: Eliminating Hardcoded Database Credentials from CI/CD Pipeline

**Context**: A DevOps team stores PostgreSQL credentials in GitHub Actions secrets and Jenkins credential stores. The same credentials are shared across staging and production environments with no rotation for 18 months.

**Approach**:
1. Deploy Vault with AppRole auth enabled for CI/CD systems
2. Configure the database secrets engine with separate roles for staging (readwrite, 2h TTL) and production (readonly, 1h TTL)
3. Create separate Vault policies for each pipeline stage restricting access to the appropriate database role
4. Update GitHub Actions workflows to authenticate via AppRole and request dynamic credentials at the start of each job
5. Rotate the static PostgreSQL credentials and hand root access to Vault exclusively
6. Enable audit logging to track every credential request with pipeline job metadata

**Pitfalls**: Failing to rotate the original static credentials after Vault migration leaves the old credentials valid. Setting TTLs too short causes credential expiry mid-deployment for long-running jobs.

## Output Format

```
Vault Secrets Management Audit Report
=======================================
Vault Cluster: vault.internal.company.com
Version: 1.18.1 Enterprise
HA Mode: Raft (3 nodes)
Seal Type: AWS KMS Auto-Unseal
Report Date: 2025-02-23

SECRET ENGINES:
  database/         PostgreSQL dynamic creds   Leases Active: 47
  aws/              Dynamic IAM credentials    Leases Active: 12
  transit/          Encryption as a service    Keys: 8
  pki/              Root CA                    Certs Issued: 0
  pki_int/          Intermediate CA            Certs Issued: 234
  secret/           KV v2 static secrets       Versions: 1,892

AUTH METHODS:
  oidc/             Okta SSO for humans        Active Tokens: 23
  approle/          CI/CD pipelines            Active Tokens: 156
  kubernetes/       Pod-based auth             Active Tokens: 89

AUDIT FINDINGS:
  [WARN] 3 AppRole secret_id_num_uses set to 0 (unlimited)
  [WARN] 12 KV secrets not accessed in 90+ days (potential orphans)
  [PASS] All dynamic secret TTLs under 24 hours
  [PASS] Audit logging enabled on all nodes
  [PASS] Root token revoked after initial setup

CREDENTIAL HYGIENE:
  Static Secrets (KV): 234
  Dynamic Secrets Active: 59
  Average Lease TTL: 2.3 hours
  Secrets Rotated This Month: 12,456
```