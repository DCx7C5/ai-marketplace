---
name: net-wireless-aircrack
description: "Net Wireless Aircrack."
domain: cybersecurity
---

--|
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
