---
name: linux-hw-usb-policy-create-configure
description: "Linux Hw Usb Policy Create Configure."
domain: cybersecurity
---

--|
| **VID/PID** | Vendor ID and Product ID that uniquely identify USB device models |
| **Device Instance ID** | Unique identifier for a specific physical USB device |
| **Device Control** | EDR/endpoint feature restricting device access based on type, vendor, or serial number |
| **USB Class** | USB device category (mass storage 08h, HID 03h, printer 07h) |

## Tools & Systems

- **Microsoft Defender Device Control**: MDE module for USB restriction policies
- **CrowdStrike Falcon Device Control**: EDR-based USB policy enforcement
- **Group Policy (Removable Storage Access)**: Built-in Windows USB restriction via GPO
- **Endpoint Protector**: Third-party device control and DLP solution

## Common Pitfalls

- **Blocking all USB without exception**: Keyboards and mice are USB HID devices. Block only mass storage class, not all USB.
- **Not communicating policy to users**: USB blocks without user notification generate helpdesk tickets. Display a notification explaining the policy.
- **Ignoring USB-C and Thunderbolt**: Modern devices use USB-C for docking, charging, and storage. Policies must distinguish between USB storage and USB peripherals.
- **No approved device process**: Users with legitimate USB needs (presentations, field data collection) require an exception process with approved, encrypted devices.
