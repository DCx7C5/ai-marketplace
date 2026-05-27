---
name: net-wireless-bluetooth
description: "--| | **BLE (Bluetooth Low Energy)** | Low-power wireless protocol (Bluetooth 4."
domain: cybersecurity
---

--|
| **BLE (Bluetooth Low Energy)** | Low-power wireless protocol (Bluetooth 4.0+) optimized for IoT devices, operating on 2.4 GHz with 40 channels (3 advertising, 37 data) |
| **GATT (Generic Attribute Profile)** | BLE data model organizing device capabilities into services, characteristics, and descriptors; the primary interface for reading/writing BLE device data |
| **Ubertooth One** | Open-source 2.4 GHz wireless development platform capable of passive BLE and Bluetooth Classic sniffing across all BLE channels |
| **nRF Sniffer** | Nordic Semiconductor firmware for nRF52840 USB dongle that enables BLE packet capture with Wireshark integration via extcap |
| **Replay Attack** | Attack where previously captured BLE commands are retransmitted to a device to trigger unauthorized actions without knowledge of encryption keys |
| **Just Works Pairing** | BLE Legacy Pairing method using TK=0 with no user confirmation, providing zero protection against passive eavesdropping and MITM attacks |
| **LE Secure Connections** | BLE 4.2+ pairing mode using ECDH key exchange (P-256 curve) that provides protection against passive eavesdropping; recommended over Legacy Pairing |
| **Crackle** | Open-source tool that exploits weaknesses in BLE Legacy Pairing to recover the Long Term Key (LTK) and decrypt captured BLE traffic |
| **GATTacker** | BLE MITM framework that clones a peripheral's GATT profile and advertising data, then relays traffic between the real device and the victim central |

## Tools & Systems

- **Ubertooth One + ubertooth-btle**: Hardware sniffer and CLI tool for passive BLE packet capture in pcapng/pcap format
- **nRF52840 USB Dongle + nRF Sniffer**: Nordic Semiconductor BLE sniffer with native Wireshark extcap integration
- **bleak**: Cross-platform Python asyncio BLE GATT client library for device scanning, connection, and characteristic read/write
- **crackle**: BLE Legacy Pairing encryption cracker that recovers LTK from captured pairing exchanges
- **Wireshark**: Network protocol analyzer with BLE/BTLE dissectors for packet-level inspection of captured traffic
- **GATTacker / BTLEjuice**: BLE Man-in-the-Middle frameworks for intercepting and modifying BLE traffic between central and peripheral
- **tshark**: Command-line Wireshark for scripted BLE packet extraction and field analysis

## Common Pitfalls

- **Ubertooth channel hopping limitations**: Ubertooth follows one connection at a time. If multiple BLE connections are active, you must target a specific device address with `-t` to follow its data channels.
- **BLE 5.0 extended advertising**: Devices using BLE 5.0 extended advertising on secondary channels may not be captured by older Ubertooth firmware. Update to the latest firmware.
- **bleak platform differences**: BLE scanning behavior varies across OS backends. On Linux, scanning requires root or appropriate capabilities. On macOS, device addresses are randomized UUIDs.
- **crackle requires Legacy Pairing**: crackle only works against BLE Legacy Pairing (Bluetooth 4.0/4.1). LE Secure Connections (4.2+) use ECDH and cannot be cracked with this approach.
- **BLE address randomization**: Many modern BLE devices use random resolvable private addresses (RPA) that rotate periodically, making device tracking and connection following more difficult.
- **Capture format matters**: Use PCAP with PPI headers (`-c` flag) for crackle compatibility. PcapNG (`-r` flag) is recommended for Wireshark analysis but not supported by crackle.

## Output Format

```
## Finding: BLE Smart Lock Accepts Replayed Unlock Commands

**ID**: BLE-001
**Severity**: Critical (CVSS 9.3)
**Device**: SmartLock-Pro (AA:BB:CC:DD:EE:FF)
**Attack Type**: Replay Attack

**Description**:
The BLE smart lock accepts previously captured GATT write commands
on characteristic 0000fff1-0000-1000-8000-00805f9b34fb without
any freshness validation. An attacker who captures a single unlock
command can replay it indefinitely to unlock the device.

**Proof of Concept**:
1. Capture unlock command: ubertooth-btle -f -t AA:BB:CC:DD:EE:FF -r capture.pcap
2. Extract write payload from characteristic fff1: 01 42 A3 7F 00
3. Replay via bleak: await client.write_gatt_char(CHAR_UUID, bytes.fromhex('0142a37f00'))
4. Lock disengages without re-authentication

**Impact**:
Any attacker within BLE range (~100m with directional antenna) who
captures a single unlock event can replay it to gain physical access
to the protected area indefinitely.

**Remediation**:
Implement challenge-response authentication with per-session nonces.
Each command should include a server-generated challenge that expires
after use. Use LE Secure Connections for pairing to prevent passive
capture of the pairing exchange.
```
