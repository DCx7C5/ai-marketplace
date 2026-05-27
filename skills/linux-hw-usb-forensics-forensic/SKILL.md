---
name: linux-hw-usb-forensics-forensic
description: - When investigating potential data exfiltration via removable storage devices - During insider threat investigations to track USB device usage - For compliance audits verifying removable media policy enforcement - When correlating USB connections with file access and copy events - For establishing a timeline of device connections during an inciden
domain: cybersecurity
---
------|-------------|
| USBSTOR | Registry key storing USB mass storage device identification and connection data |
| VID/PID | Vendor ID and Product ID uniquely identifying USB device manufacturer and model |
| Device serial number | Unique identifier for individual USB devices (some devices share serials) |
| MountedDevices | Registry key mapping volume GUIDs and drive letters to physical devices |
| MountPoints2 | Per-user registry key showing which volumes a user accessed |
| SetupAPI log | Windows driver installation log recording first-time device connections |
| DeviceContainers | Registry key in SOFTWARE hive with device metadata and timestamps |
| EMDMgmt | Registry key tracking ReadyBoost-compatible devices with serial numbers and timestamps |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| USB Forensic Tracker | Specialized tool for USB device history extraction |
| USBDeview | NirSoft tool listing all USB devices connected to a system |
| RegRipper (usbstor plugin) | Automated USB artifact extraction from registry hives |
| Registry Explorer | Interactive registry analysis for USB-related keys |
| KAPE | Automated collection of USB-related artifacts |
| Plaso/log2timeline | Timeline creation including USB connection events |
| FTK Imager | Forensic imaging including removable media |
| Velociraptor | Endpoint agent with USB device history hunting artifacts |

## Common Scenarios

**Scenario 1: Data Exfiltration by Departing Employee**
Extract USBSTOR entries to identify all USB devices ever connected, correlate device serial numbers with MountPoints2 to confirm user access, cross-reference timestamps with file access logs and jump list recent files, check for large file copy patterns in USN journal.

**Scenario 2: Unauthorized Device on Secure System**
Audit all USBSTOR entries against approved device list, identify unauthorized devices by VID/PID not matching corporate-approved hardware, determine when the unauthorized device was first and last connected, check if any data was transferred.

**Scenario 3: Malware Delivery via USB**
Identify USB device connected just before malware execution (Prefetch timestamps), extract the device serial and vendor information, check if autorun was enabled for the device, look for executable launch from the removable drive letter in Prefetch and ShimCache.

**Scenario 4: Tracking a Specific USB Drive Across Multiple Systems**
Search for the same device serial number in USBSTOR across all forensic images, build a map of which systems the drive was connected to and when, identify the chronological path of the device through the organization, correlate with network share access logs.

## Output Format

```
USB Device History Analysis:
  System: DESKTOP-ABC123 (Windows 10 Pro)
  Total USB Storage Devices: 12
  Analysis Sources: USBSTOR, MountedDevices, MountPoints2, SetupAPI, Event Logs

  Device Inventory:
    1. Kingston DataTraveler 3.0 (Serial: 0019E06B4521A2B0)
       First Connected:  2024-01-10 09:15:32 (SetupAPI)
       Last Connected:   2024-01-18 14:30:00 (USBSTOR)
       Drive Letter:     E:
       User Access:      suspect_user (MountPoints2)

    2. WD My Passport (Serial: 575834314131363035)
       First Connected:  2024-01-15 20:00:00
       Last Connected:   2024-01-15 23:45:00
       Drive Letter:     F:
       User Access:      suspect_user

  Suspicious Findings:
    - Kingston drive connected 15 times during investigation period
    - WD Passport connected only once, late evening (unusual hours)
    - Unknown device (VID_1234&PID_5678) connected 2024-01-17, no matching approved device

  Timeline: /cases/case-2024-001/analysis/usb_timeline.csv
```