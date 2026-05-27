---
name: soc-endpoint-security-monitor
description: "Soc Endpoint Security Monitor."
domain: cybersecurity
---

--|
| **DLP** | Data Loss Prevention; technology that detects and prevents unauthorized transmission of sensitive data |
| **SIT** | Sensitive Information Type; pattern matching rules for identifying sensitive data (regex, keywords, ML classifiers) |
| **Policy Tip** | User-facing notification explaining why an action was blocked and how to request an override |
| **Content Inspection** | Deep inspection of file contents to identify sensitive data patterns |
| **Exact Data Match (EDM)** | DLP matching against a specific database of known sensitive values (exact SSNs, employee records) |

## Tools & Systems

- **Microsoft Purview DLP**: Cloud-managed endpoint DLP included in M365 E5
- **Symantec DLP (Broadcom)**: Enterprise DLP with endpoint, network, and cloud modules
- **Digital Guardian**: Endpoint DLP with data classification and protection
- **Forcepoint DLP**: Unified DLP platform with endpoint agent
- **Code42 Incydr**: Insider risk detection with file exfiltration monitoring

## Common Pitfalls

- **Over-blocking in enforcement mode**: Deploy DLP in audit mode first. Blocking common workflows without warning causes productivity loss.
- **Too many SIT false positives**: Phone numbers, dates, and random number sequences can match PCI/SSN patterns. Tune confidence levels and require corroborating keywords.
- **Ignoring user education**: DLP is most effective when users understand why data is protected. Policy tips should explain the restriction and provide approved alternatives.
- **Not monitoring overrides**: If users frequently override DLP blocks, the policy is either too restrictive or users are ignoring data protection requirements. Review override reasons.
