# Hardware USB Device Detect

## Overview

Detect unauthorized or suspicious USB devices on Linux endpoints using kernel event logs, udev, and audit log correlation.

## Prerequisites

- `lsusb`, `udevadm` available; root or `adm` group for dmesg

## Procedure

### Step 1 — Enumerate connected devices

```bash
lsusb
dmesg | grep -iE "usb|hid|storage" | tail -50
journalctl -k --since "1 hour ago" | grep -iE "usb|hid"
```

### Step 2 — Audit log correlation

```bash
ausearch -m USER_DEVICE 2>/dev/null | tail -20
```

### Step 3 — Record artifact

```bash
ARTIFACT="/tmp/usb-devices-$(date +%s).txt"
lsusb -v > "$ARTIFACT" 2>&1
HASH=$(b2sum -l 256 "$ARTIFACT" | awk '{print $1}')
echo "blake2b:$HASH  $ARTIFACT"
```

## MITRE ATT&CK

| Technique | Name |
|-----------|------|
| T1200 | Hardware Additions |
| T1091 | Replication Through Removable Media |
