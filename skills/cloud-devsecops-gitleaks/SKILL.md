---
name: cloud-devsecops-gitleaks
description: "Cloud Devsecops Gitleaks."
domain: cybersecurity
---

|
| Secret | Any credential, token, key, or sensitive string that should not appear in source code |
| Pre-commit Hook | Git hook that runs before a commit is created, blocking commits containing detected secrets |
| Entropy | Measure of randomness in a string; high-entropy strings are more likely to be secrets |
| Baseline | Snapshot of existing findings used to differentiate new secrets from pre-existing ones |
| Allowlist | Configuration specifying paths, patterns, or commits to exclude from detection |
| SARIF | Static Analysis Results Interchange Format for uploading findings to security dashboards |
| git-filter-repo | Tool for rewriting git history to remove sensitive data from all commits |

## Tools & Systems

- **Gitleaks**: Open-source secret detection tool supporting pre-commit hooks, CI/CD, and historical scanning
- **pre-commit**: Framework for managing and maintaining multi-language pre-commit hooks
- **git-filter-repo**: History rewriting tool for removing secrets from git history
- **TruffleHog**: Alternative secret scanner with verified secret detection capabilities
- **GitHub Secret Scanning**: Native GitHub feature that detects secrets matching partner patterns

## Common Scenarios

### Scenario: Onboarding Secret Scanning on a Legacy Repository

**Context**: A 5-year-old repository has never been scanned. The team needs to enable secret scanning without blocking all development while historical secrets are rotated.

**Approach**:
1. Run `gitleaks detect` against full history and generate a baseline JSON file
2. Triage each finding: classify as active (needs rotation), inactive (already rotated), or false positive
3. Immediately rotate all active secrets and update consuming services
4. Commit the baseline file (excluding active secrets that have been fixed)
5. Enable pre-commit hooks for new development immediately
6. Add CI/CD scanning with the baseline to catch only new secrets
7. Progressively reduce the baseline as historical secrets are rotated

**Pitfalls**: Generating a baseline without triaging means accepting risk on unrotated secrets. Never assume a historical secret is inactive without verifying with the service provider. Running git-filter-repo on a shared repository without coordination will cause rebase conflicts for all team members.

## Output Format

```
Gitleaks Secret Scanning Report
=================================
Repository: org/web-application
Scan Type: Full History
Commits Scanned: 4,523
Date: 2026-02-23

FINDINGS:
  Total: 12
  New (not in baseline): 3
  Baseline (pre-existing): 9

NEW FINDINGS (blocking):
  [1] AWS Access Key ID
      Rule: aws-access-key-id
      File: src/config/aws.py:23
      Commit: a1b2c3d (2026-02-22, dev@company.com)
      Secret: AKIA...REDACTED
      Entropy: 3.8

  [2] GitHub Personal Access Token
      Rule: github-pat
      File: scripts/deploy.sh:15
      Commit: d4e5f6g (2026-02-21, ops@company.com)
      Secret: ghp_...REDACTED
      Entropy: 4.2

  [3] Internal API Token
      Rule: internal-api-token
      File: src/services/auth.py:89
      Commit: h7i8j9k (2026-02-20, dev@company.com)

QUALITY GATE: FAILED (3 new findings)
Action: Rotate exposed credentials immediately.
```
