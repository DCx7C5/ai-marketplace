---
name: identity-hardware-token-verify
description: - Deploying phishing-resistant multi-factor authentication (MFA) using FIDO2 hardware security keys for high-value accounts (administrators, developers, privileged users) - Building a WebAuthn relying party server that supports both roaming authenticators (USB/NFC security keys) and platform authenticators (Windows Hello, Touch ID, Android biometri
domain: cybersecurity
---
---|------------|
| **FIDO2** | An umbrella term for the combination of the W3C WebAuthn API and the FIDO Alliance CTAP2 protocol, enabling passwordless and phishing-resistant authentication using public key cryptography |
| **WebAuthn** | The W3C Web Authentication API that allows web applications to create and use public key credentials via `navigator.credentials.create()` (registration) and `navigator.credentials.get()` (authentication) |
| **CTAP2** | Client to Authenticator Protocol version 2; the protocol used by the browser (client) to communicate with external authenticators over USB, NFC, or BLE |
| **Relying Party (RP)** | The web application or service that requests authentication; identified by its RP ID (a domain) and RP name (display string) |
| **Discoverable Credential (Passkey)** | A credential stored on the authenticator that can be enumerated without the RP providing a credential ID, enabling username-less authentication flows |
| **Attestation** | Cryptographic proof from the authenticator about its identity and properties; used by the RP to verify the authenticator model and manufacturer |
| **AAGUID** | Authenticator Attestation Globally Unique Identifier; a 128-bit value identifying the authenticator model (e.g., all YubiKey 5 NFC devices share the same AAGUID) |
| **Sign Count** | A monotonically increasing counter maintained by the authenticator and included in each assertion; used by the RP to detect cloned authenticators |
| **User Verification (UV)** | Local authentication on the authenticator itself (PIN, fingerprint, face recognition) that proves the person holding the authenticator is the legitimate owner |

## Tools & Systems

- **python-fido2**: Yubico's official Python library (v2.0+) providing `Fido2Server` for relying party implementation and `CtapHidDevice`/`Fido2Client` for direct authenticator communication over USB
- **YubiKey 5 Series**: Yubico hardware security keys supporting FIDO2/CTAP2, U2F, PIV, OpenPGP, and OTP; available in USB-A, USB-C, NFC, and Nano form factors
- **py_webauthn**: Duo Labs' Python WebAuthn library providing `generate_registration_options()`, `verify_registration_response()`, `generate_authentication_options()`, and `verify_authentication_response()` functions
- **Yubico Authenticator**: Desktop and mobile application for managing YubiKey FIDO2 credentials, setting PINs, and viewing registered accounts
- **WebAuthn.io / demo.yubico.com**: Online testing tools for verifying WebAuthn registration and authentication flows against real authenticators

## Common Scenarios

### Scenario: Deploying FIDO2 MFA for a Development Team

**Context**: A software company wants to replace TOTP-based MFA with hardware security keys for its 50-person development team. Developers have root access to production infrastructure and are high-value targets for phishing attacks. The company has standardized on YubiKey 5 NFC.

**Approach**:
1. Provision YubiKey 5 NFC keys (2 per developer: primary + backup) and distribute in tamper-evident packaging with initial PIN setup instructions
2. Deploy the WebAuthn relying party server integrated with the company's SSO (OAuth 2.0 / OpenID Connect) provider, configured with `authenticator_attachment: cross-platform` and `user_verification: required`
3. Run enrollment sessions where each developer registers both keys to their account, with attestation verification confirming genuine YubiKey 5 NFC AAGUIDs
4. Configure the SSO provider to require FIDO2 as the second factor for all developer accounts, with a 30-day grace period where TOTP remains available
5. Implement a self-service portal for key management: view registered keys, register replacement keys, and report lost/stolen keys (which triggers immediate credential revocation and re-enrollment)
6. After the grace period, disable TOTP for developer accounts. Monitor authentication logs for any fallback attempts and provide 1:1 support for remaining holdouts
7. Achieve 100% FIDO2 adoption for the development team, reducing phishing risk to near-zero for production infrastructure access

**Pitfalls**:
- Not requiring backup key enrollment, leading to account lockouts when a single key is lost
- Setting `user_verification: discouraged` which allows anyone who physically possesses the key to authenticate without a PIN
- Forgetting to validate the sign counter, missing cloned key attacks
- Not supporting NFC for developers who primarily work from tablets or phones
- Allowing TOTP as a permanent fallback, which undermines the phishing resistance of the FIDO2 deployment

### Scenario: Implementing Passwordless Login for a Customer-Facing Application

**Context**: An e-commerce platform wants to offer passkey-based passwordless login to its 2 million users as an alternative to passwords, reducing account takeover from credential stuffing and phishing.

**Approach**:
1. Implement WebAuthn with `resident_key: required` to create discoverable credentials that enable username-less login
2. Support both platform authenticators (Touch ID, Windows Hello, Android biometrics) and roaming authenticators (security keys) by omitting `authenticator_attachment`
3. Add a "Sign in with a passkey" button to the login page that triggers `navigator.credentials.get()` with an empty `allowCredentials` list, prompting the authenticator to present available passkeys
4. After successful passkey creation, prompt users to create a passkey on a second device for redundancy
5. Maintain password login as a fallback during the rollout period, with a persistent prompt encouraging passkey setup after each password login
6. Track metrics: passkey registration rate (target 30% in first quarter), passkey vs. password login ratio, authentication failure rates, and account takeover incidents
7. After 6 months, offer incentives (extended session duration, reduced CAPTCHA) for users who switch to passkey-only authentication

**Pitfalls**:
- Not handling the case where a user's platform authenticator (e.g., laptop Touch ID) is unavailable and they need cross-device authentication via QR code
- Assuming all users have biometric-capable devices; some will need to fall back to PIN-based verification
- Not implementing proper account recovery for users who lose access to all registered passkeys
- Ignoring browser compatibility gaps, particularly in older Safari versions on iOS

## Output Format

```
## FIDO2 Deployment Report

**Application**: auth.example.com
**RP ID**: example.com
**Date**: 2026-03-19

### Enrollment Summary
- **Total Users**: 50
- **Users with Primary Key**: 50 (100%)
- **Users with Backup Key**: 47 (94%)
- **Authenticator Models**: YubiKey 5 NFC (48), YubiKey 5C NFC (2)

### Authentication Metrics (Last 30 Days)
- **Total Authentications**: 12,847
- **FIDO2 Authentications**: 12,203 (95.0%)
- **TOTP Fallback**: 644 (5.0%) -- grace period active
- **Mean Authentication Time**: 2.3 seconds
- **Authentication Failures**: 127 (0.99%)
  - User cancelled: 89
  - Timeout: 23
  - Invalid signature: 12
  - Sign count regression (possible clone): 3

### Security Events
- **Lost Key Reports**: 2
  - User A: primary key lost 2026-03-12, revoked, backup promoted, new backup enrolled
  - User B: backup key damaged 2026-03-15, revoked, replacement enrolled

### Credential Details
| User | Key Label | AAGUID | Registered | Last Used | Sign Count |
|------|-----------|--------|------------|-----------|------------|
| alice | YubiKey Primary | 2fc0579f... | 2026-02-15 | 2026-03-19 | 847 |
| alice | YubiKey Backup | 2fc0579f... | 2026-02-15 | 2026-03-01 | 12 |
| bob | YubiKey Primary | 2fc0579f... | 2026-02-16 | 2026-03-19 | 631 |
```