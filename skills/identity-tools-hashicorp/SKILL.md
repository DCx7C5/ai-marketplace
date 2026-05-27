---
name: identity-tools-hashicorp
description: "Identity Tools Hashicorp."
domain: cybersecurity
---

|
| **Dynamic Secrets** | Credentials generated on-demand by Vault with automatic expiration, ensuring each consumer receives unique short-lived credentials |
| **Lease** | Time-bound agreement where Vault guarantees the credential is valid; consumers must renew before expiration or request new credentials |
| **Secrets Engine** | Vault plugin that generates, stores, or encrypts data; database, AWS, PKI, and KV are common engines |
| **AppRole** | Vault authentication method designed for machine-to-machine authentication using role ID and secret ID pairs |
| **Root Credential Rotation** | Process of having Vault take exclusive ownership of the admin credential used to create dynamic secrets, eliminating human knowledge of the root password |
| **Lease Revocation** | Immediate invalidation of dynamic credentials, used during incident response to revoke all credentials for compromised paths |

## Tools & Systems

- **HashiCorp Vault**: Secrets management platform providing dynamic secrets, encryption as a service, and identity-based access control
- **Vault Agent**: Sidecar process that handles Vault authentication, token renewal, and secret caching for applications
- **Vault Secrets Operator**: Kubernetes operator that syncs Vault secrets into Kubernetes Secrets for pod consumption
- **hvac**: Python client library for HashiCorp Vault API operations

## Common Scenarios

### Scenario: Eliminating Static Database Credentials in Microservices

**Context**: 50 microservices share 3 static PostgreSQL credentials stored in environment variables across Kubernetes deployments. A credential leak requires rotating all 50 services simultaneously.

**Approach**:
1. Deploy Vault with Raft storage in a 3-node HA cluster within Kubernetes
2. Configure database secrets engine with PostgreSQL connection using admin credentials
3. Create per-service Vault roles with least-privilege SQL grants
4. Deploy Vault Secrets Operator to inject dynamic credentials into pod environment variables
5. Update application connection logic to handle credential rotation via lease renewal
6. Rotate the Vault root credential to remove human knowledge of the admin password
7. Monitor lease lifecycle and set alerts for renewal failures

**Pitfalls**:
- Not handling credential rotation in application connection pools (connections using expired credentials fail)
- Setting TTLs too short causes excessive credential generation load on the database
- Not configuring proper revocation statements leaves orphaned database users after lease expiration
- Running Vault without HA causes single point of failure for all application authentication

## Output Format

```
HASHICORP VAULT DYNAMIC SECRETS REPORT
=========================================
Vault Version:     1.16.2 Enterprise
Cluster Status:    HA Active (3 nodes)
Seal Type:         AWS KMS (auto-unseal)

SECRETS ENGINES
database/:         PostgreSQL, MySQL (2 connections)
aws/:              IAM User, Assumed Role, Federation Token
pki_int/:          Internal CA (EC P-256)

DYNAMIC CREDENTIAL METRICS (Last 24 Hours)
Total Credentials Generated:    4,287
  Database (PostgreSQL):        2,891
  Database (MySQL):             543
  AWS STS:                      612
  PKI Certificates:             241

ACTIVE LEASES
Total Active:                   387
  database/creds/app-readonly:  198
  database/creds/app-readwrite: 89
  aws/creds/s3-readonly:        67
  pki_int/issue/web-server:     33

LEASE LIFECYCLE
Average TTL:                    45 minutes
Renewals (24h):                 12,847
Revocations (24h):              3,901
Expired (not renewed):          12

SECURITY
Failed Auth Attempts (24h):     3
Root Credential Rotated:        YES (all databases)
Audit Logging:                  ENABLED (file + syslog)
Policy Violations (24h):        7 (permission denied)
```
