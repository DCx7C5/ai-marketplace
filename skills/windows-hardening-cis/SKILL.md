---
name: windows-hardening-cis
description: Use this skill when: - Deploying new Windows 10/11 or Server 2019/2022 endpoints that require security hardening - Establishing organization-wide security baselines using CIS Level 1 or Level 2 profiles - Remediating findings from compliance audits (PCI DSS, HIPAA, SOC 2) that reference CIS benchmarks - Validating existing endpoint configurations a
domain: cybersecurity
---
---|-----------|
| **CIS Benchmark** | Consensus-based security configuration guide developed by CIS with input from government, industry, and academia |
| **Level 1 Profile** | Practical security baseline suitable for most organizations with minimal operational impact |
| **Level 2 Profile** | Extended security baseline for high-security environments that may reduce functionality |
| **CIS-CAT** | CIS Configuration Assessment Tool that automates benchmark compliance checking |
| **Build Kit** | Pre-configured GPO templates provided by CIS that implement benchmark recommendations |
| **Scoring** | CIS recommendations are either Scored (compliance-measurable) or Not Scored (best-practice guidance) |

## Tools & Systems

- **CIS-CAT Pro Assessor**: Automated benchmark compliance scanner (requires CIS SecureSuite license)
- **Microsoft Security Compliance Toolkit (SCT)**: Microsoft's own GPO baselines (complementary to CIS)
- **Group Policy Management Console (GPMC)**: Enterprise GPO deployment and management
- **LGPO.exe**: Microsoft tool for applying GPOs to standalone (non-domain) systems
- **Nessus/Tenable**: Vulnerability scanner with CIS benchmark audit files

## Common Pitfalls

- **Applying L2 to all endpoints**: Level 2 restrictions (disabling Autoplay, restricting Remote Desktop) break workflows on standard workstations. Reserve L2 for endpoints handling sensitive data.
- **Not testing GPOs in pilot OU**: Deploy CIS GPOs to a test OU with representative hardware/software before organization-wide rollout to avoid breaking line-of-business applications.
- **Ignoring CIS benchmark version updates**: CIS benchmarks update with each Windows feature release. Running an outdated benchmark misses new security settings and generates false compliance reports.
- **Forgetting local admin accounts**: CIS benchmarks assume domain-joined endpoints. Standalone systems require LGPO.exe or Microsoft Intune for baseline enforcement.
- **No exception process**: Applying 100% of CIS recommendations is rarely feasible. Without a formal exception process, teams either ignore hardening or break applications.