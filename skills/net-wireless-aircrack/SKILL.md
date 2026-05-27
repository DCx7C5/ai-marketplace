---
name: net-wireless-aircrack
description: - Assessing the strength of WPA/WPA2/WPA3 passphrases during authorized wireless penetration tests - Testing whether wireless networks are using weak or default passwords that can be cracked offline - Capturing and analyzing 4-way handshakes to evaluate wireless authentication security - Demonstrating the risks of WEP, weak WPA2 passphrases, and PM
domain: cybersecurity
---
---|------------|
| **4-Way Handshake** | WPA/WPA2 authentication exchange between client and AP that derives session keys from the PSK, captured for offline password cracking |
| **PMKID** | Pairwise Master Key Identifier included in the first EAPOL frame from the AP, allowing password cracking without capturing the full handshake or requiring a connected client |
| **Monitor Mode** | Wireless interface mode that captures all wireless frames on a channel without associating with any access point |
| **Deauthentication Attack** | Sending forged 802.11 management frames to disconnect a client from the AP, forcing a reconnection that generates a capturable handshake |
| **PSK (Pre-Shared Key)** | Static password used by all users to authenticate to a WPA/WPA2-Personal network, vulnerable to offline dictionary attacks |
| **802.1X/EAP** | Enterprise wireless authentication using RADIUS that provides per-user credentials, eliminating the shared password vulnerability |

## Tools & Systems

- **aircrack-ng suite**: Comprehensive wireless security toolkit including airodump-ng (capture), aireplay-ng (injection), and aircrack-ng (cracking)
- **hashcat**: GPU-accelerated password cracker supporting WPA/WPA2 handshakes (mode 22000) with dictionary, rule, and mask attacks
- **hcxtools**: Tools for capturing PMKID and converting wireless captures to hashcat-compatible formats
- **hcxdumptool**: Capture tool specifically designed for PMKID extraction without requiring client deauthentication
- **cowpatty**: WPA/WPA2 cracking tool with precomputed hash table support for faster dictionary attacks

## Common Scenarios

### Scenario: Wireless Penetration Test for a Corporate Office

**Context**: A financial services company wants to assess the security of their wireless networks. They have three SSIDs: Corp-WiFi (WPA2-Enterprise for employees), Guest-WiFi (WPA2-PSK for visitors), and IoT-WiFi (WPA2-PSK for IoT devices). The assessment is authorized to test all three networks.

**Approach**:
1. Scan for all three SSIDs and identify their BSSIDs, channels, and encryption types
2. Verify that Corp-WiFi uses 802.1X/EAP by examining beacon frames -- confirmed, no PSK to crack
3. Capture the 4-way handshake for Guest-WiFi by deauthenticating a connected device and capturing the reconnection
4. Run hashcat with rockyou.txt against the Guest-WiFi handshake -- password "Welcome2024!" cracked in 47 seconds
5. Capture PMKID from IoT-WiFi access point (no client deauth needed) and crack with hashcat -- password "iot12345" found in 12 seconds
6. Demonstrate that Guest-WiFi and IoT-WiFi passwords are weak and easily crackable
7. Recommend migrating Guest-WiFi to a captive portal with per-session passwords and strengthening IoT-WiFi to a 20+ character passphrase

**Pitfalls**:
- Sending excessive deauth frames that disrupt legitimate wireless users beyond the test scope
- Not using a wireless adapter that supports the target network's frequency band (2.4 GHz vs 5 GHz)
- Attempting to crack WPA3-SAE networks with traditional handshake capture (SAE is resistant to offline attacks)
- Running GPU cracking on shared systems without monitoring temperature and power consumption

## Output Format

```
## Wireless Security Assessment Report

**Assessment Date**: 2024-03-15
**Location**: Corporate Office, Building A

### Network Inventory

| SSID | BSSID | Encryption | Auth | Channel | Crackable |
|------|-------|------------|------|---------|-----------|
| Corp-WiFi | AA:BB:CC:11:22:33 | WPA2 | 802.1X | 36 | N/A (Enterprise) |
| Guest-WiFi | AA:BB:CC:44:55:66 | WPA2 | PSK | 6 | YES - 47 seconds |
| IoT-WiFi | AA:BB:CC:77:88:99 | WPA2 | PSK | 1 | YES - 12 seconds |

### Findings

**Finding 1: Weak Guest-WiFi Password (High)**
- Password: "Welcome2024!" (cracked via dictionary in 47 seconds)
- Present in rockyou.txt top 100,000 entries
- Shared among all visitors with no rotation policy

**Finding 2: Trivial IoT-WiFi Password (Critical)**
- Password: "iot12345" (cracked in 12 seconds)
- Default-pattern password providing access to IoT device network
- No network segmentation between IoT-WiFi and corporate resources

### Recommendations
1. Migrate Guest-WiFi to captive portal with per-session credentials
2. Change IoT-WiFi to 20+ character random passphrase with quarterly rotation
3. Implement network segmentation isolating IoT VLAN from corporate resources
4. Consider WPA3-SAE for PSK networks to prevent offline cracking
5. Enable 802.11w Protected Management Frames to prevent deauth attacks
```