---
name: identity-kerberos-constrained
description: Kerberos Constrained Delegation (KCD) is a Windows Active Directory feature that allows a service to impersonate a user and access specific services on their behalf. The delegation targets are defined in the msDS-AllowedToDelegateTo attribute. When an attacker compromises an account configured with Constrained Delegation (particularly with the TRUS
domain: cybersecurity
---
---|---------|----------|
| Rubeus | S4U Kerberos ticket manipulation | Windows (.NET) |
| getST.py | S4U service ticket requests (Impacket) | Linux (Python) |
| findDelegation.py | Delegation enumeration (Impacket) | Linux (Python) |
| PowerView | AD delegation enumeration | Windows (PowerShell) |
| BloodHound CE | Visual delegation path analysis | Docker |
| Kekeo | Advanced Kerberos toolkit | Windows |

## Delegation Types Comparison

| Type | Attribute | Scope | Attack Complexity |
|------|-----------|-------|-------------------|
| Unconstrained | TRUSTED_FOR_DELEGATION | Any service | Low (capture TGTs) |
| Constrained | msDS-AllowedToDelegateTo | Specific SPNs | Medium (S4U abuse) |
| Constrained + Protocol Transition | + TRUSTED_TO_AUTH_FOR_DELEGATION | Specific SPNs | Medium (no user auth needed) |
| Resource-Based (RBCD) | msDS-AllowedToActOnBehalfOfOtherIdentity | On target | Medium (writable attribute) |

## Detection Signatures

| Indicator | Detection Method |
|-----------|-----------------|
| S4U2self ticket requests | Event 4769 with unusual service and impersonation |
| S4U2proxy forwarded tickets | Event 4769 with delegation flags set |
| Alternate service name in ticket | Mismatch between requested SPN and actual service access |
| Rubeus.exe execution | EDR process detection, command-line logging |
| Delegation configuration changes | Event 5136 for msDS-AllowedToDelegateTo modifications |

## Validation Criteria

- [ ] Accounts with Constrained Delegation enumerated
- [ ] Delegation targets (msDS-AllowedToDelegateTo) identified
- [ ] S4U2self ticket obtained for target user
- [ ] S4U2proxy ticket forwarded to delegation target
- [ ] Privileged access to delegated service validated
- [ ] Alternate service name substitution tested
- [ ] Protocol transition capability assessed
- [ ] Evidence documented with ticket exports and access proof