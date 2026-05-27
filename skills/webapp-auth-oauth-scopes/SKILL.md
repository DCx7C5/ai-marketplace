---
name: webapp-auth-oauth-scopes
description: - Annual or quarterly review of third-party application OAuth permissions - After a security incident involving compromised OAuth tokens or unauthorized data access - Compliance audit requiring documentation of third-party data access (GDPR Article 28, SOC 2) - Discovery of shadow IT applications accessing organizational data via OAuth grants - Mig
domain: cybersecurity
---
---|------------|
| **OAuth Scope** | Permission string defining the specific API access level granted to a client application (e.g., Mail.Read, Files.ReadWrite.All) |
| **Delegated Permission** | OAuth scope exercised on behalf of a signed-in user, limited by both the app's permissions and the user's own access rights |
| **Application Permission** | OAuth scope granted directly to the application without user context, providing access to all users' data (high risk) |
| **Admin Consent** | Tenant-wide permission grant made by an administrator that applies to all users without individual consent |
| **Scope Minimization** | Security principle of reducing OAuth permissions to the minimum set required for application functionality |
| **Stale Grant** | OAuth permission that remains active but has no recent API usage, indicating the integration is abandoned or deprecated |

## Tools & Systems

- **Microsoft Entra Admin Center**: Portal for reviewing enterprise applications, consent permissions, and OAuth grant management
- **Nudge Security**: SaaS security platform for discovering OAuth grants, assessing third-party risk, and automating scope reviews
- **Cerby**: Non-SSO application management platform for auditing OAuth integrations and managing shared accounts
- **Microsoft Graph API**: Programmatic interface for enumerating and modifying OAuth permission grants at scale

## Common Scenarios

### Scenario: Post-Breach OAuth Scope Audit

**Context**: After a phishing attack compromised an admin account, investigation reveals the attacker registered a malicious OAuth application with Mail.ReadWrite and Files.ReadWrite.All scopes, exfiltrating 6 months of email. The organization needs a comprehensive OAuth scope review.

**Approach**:
1. Immediately revoke all OAuth grants from the compromised admin session
2. Enumerate all service principals and permission grants across the tenant
3. Flag all applications registered in the last 90 days for manual review
4. Classify all third-party application scopes using the risk framework
5. Identify applications with critical scopes (Mail.ReadWrite, Files.ReadWrite.All, Directory.ReadWrite.All)
6. Cross-reference against approved application catalog from IT procurement
7. Revoke all unapproved applications immediately
8. Downgrade over-permissioned approved applications to minimum required scopes
9. Implement admin consent workflow to prevent future uncontrolled OAuth grants
10. Enable consent policy requiring admin approval for high-risk scopes

**Pitfalls**:
- Revoking permissions for business-critical integrations without coordination causes service disruption
- Not checking for application-level permissions (vs delegated) which are higher risk and often overlooked
- Missing multi-tenant applications where the publisher tenant differs from the consuming tenant
- Not implementing ongoing monitoring to detect new unauthorized OAuth grants after remediation

## Output Format

```
OAUTH SCOPE MINIMIZATION REVIEW REPORT
=========================================
Tenant:              corp.onmicrosoft.com
Review Period:       2026-02-01 to 2026-02-24
Total Applications:  147
Third-Party Apps:    98
First-Party Apps:    49

PERMISSION INVENTORY
Total OAuth Grants:          487
  Delegated Permissions:     312
  Application Permissions:   175
  Admin-Consented:           89
  User-Consented:            223

RISK CLASSIFICATION
Critical Risk Apps:     7
  - UnknownCRMApp (Mail.ReadWrite, Files.ReadWrite.All - UNAPPROVED)
  - LegacySync (Directory.ReadWrite.All - EXCESSIVE)
  - DevToolX (Application.ReadWrite.All - OVERLY BROAD)
High Risk Apps:         18
Medium Risk Apps:       34
Low Risk Apps:          88

FINDINGS
Unapproved Applications:        12 (REVOKE IMMEDIATELY)
Excessive Scopes:               23 apps with scopes beyond approved list
Overly Broad Permissions:       15 apps that can be downgraded
Stale Grants (90+ days):        31 apps with no recent API activity

REMEDIATION PLAN
Priority 1 (Immediate):    12 unapproved app revocations
Priority 2 (This Week):    23 excessive scope removals
Priority 3 (This Month):   15 scope downgrades
Priority 4 (Next Quarter): 31 stale grant revocations

Estimated Scope Reduction:  34% of total permissions
```