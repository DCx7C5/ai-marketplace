---
name: webapp-auth-oauth-tokentheft
description: "Webapp Auth Oauth Tokentheft."
domain: cybersecurity
---

|
| **Primary Refresh Token (PRT)** | A long-lived token issued to a registered device that provides SSO to all Azure AD-integrated applications, cryptographically bound to the device's TPM |
| **Token Protection** | Entra ID conditional access feature that binds sign-in session tokens to the device, preventing replay from other devices |
| **Continuous Access Evaluation (CAE)** | Protocol that enables near-real-time enforcement of security policies by allowing resource providers to subscribe to Entra ID critical events |
| **AitM (Adversary-in-the-Middle)** | Phishing technique where an attacker proxies the legitimate authentication flow to capture session cookies after the victim completes MFA |
| **Device Code Flow** | OAuth 2.0 authorization grant for input-constrained devices; abused by attackers who send device codes to victims via phishing |
| **Proof of Possession (PoP)** | Cryptographic mechanism where a token includes a claim tied to a device key, ensuring the token can only be used by the device that obtained it |
| **Refresh Token** | Long-lived OAuth token (up to 90 days) used to obtain new access tokens without re-authentication; primary target for persistent access |

## Verification

- [ ] Identity Protection risk detections are enabled and generating alerts for anomalous token activity
- [ ] Conditional access policies block high-risk sign-ins and require MFA for medium-risk
- [ ] Token Protection policy is applied to pilot group and confirmed working (test from unregistered device fails)
- [ ] KQL queries in Sentinel return results when tested against synthetic token anomaly events
- [ ] Continuous Access Evaluation is enabled and verified (revoke session, confirm access blocked within minutes)
- [ ] Defender for Cloud Apps session policies are active and monitoring download activity
- [ ] Device code flow is restricted via conditional access (block or require compliant device)
- [ ] Incident response runbook includes token revocation, password reset, and OAuth consent review steps
- [ ] Mail forwarding rules and OAuth app grants are audited for compromised accounts
