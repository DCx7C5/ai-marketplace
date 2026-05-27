---
name: ics-ics-scada-attack
description: - When deploying intrusion detection capabilities in a SCADA environment for the first time - When investigating suspected cyber attacks against industrial control systems - When building detection rules for OT-specific attack patterns (Stuxnet, TRITON, Industroyer) - When integrating OT network monitoring with an enterprise SOC for unified threat 
domain: cybersecurity
---
Modbus Attack Detection ---

# Unauthorized Modbus write to PLC from non-engineering workstation
alert modbus any any -> $OT_PLC_SUBNET 502 (
  msg:"OT-DETECT Modbus write from unauthorized source";
  modbus_func:!read_coils; modbus_func:!read_discrete_inputs;
  modbus_func:!read_holding_registers; modbus_func:!read_input_registers;
  flow:to_server,established;
  threshold:type both, track by_src, count 1, seconds 60;
  classtype:attempted-admin;
  sid:3000001; rev:1;
)

# Modbus diagnostic/restart command (FC 8) - potential PLC DoS
alert modbus any any -> $OT_PLC_SUBNET 502 (
  msg:"OT-DETECT Modbus diagnostics command to PLC";
  modbus_func:diagnostics;
  flow:to_server,established;
  classtype:attempted-dos;
  sid:3000002; rev:1;
)

# Modbus broadcast write (unit ID 0) - affects all slaves
alert modbus any any -> $OT_PLC_SUBNET 502 (
  msg:"OT-CRITICAL Modbus broadcast write command";
  modbus_unit_id:0;
  flow:to_server,established;
  classtype:attempted-admin;
  sid:3000003; rev:1;
  priority:1;
)

# --- S7comm Attack Detection (Siemens) ---

# S7comm CPU STOP command - shuts down PLC execution
alert tcp any any -> $SIEMENS_PLC_SUBNET 102 (
  msg:"OT-CRITICAL S7comm CPU STOP command detected";
  content:"|03 00|"; offset:0; depth:2;
  content:"|29|"; offset:17; depth:1;
  flow:to_server,established;
  classtype:attempted-dos;
  sid:3000010; rev:1;
  priority:1;
)

# S7comm PLC program upload (potential logic modification)
alert tcp any any -> $SIEMENS_PLC_SUBNET 102 (
  msg:"OT-CRITICAL S7comm program download to PLC";
  content:"|03 00|"; offset:0; depth:2;
  content:"|1a|"; offset:17; depth:1;
  flow:to_server,established;
  classtype:attempted-admin;
  sid:3000011; rev:1;
  priority:1;
)

# --- DNP3 Attack Detection ---

# DNP3 cold restart command
alert tcp any any -> $OT_RTU_SUBNET 20000 (
  msg:"OT-CRITICAL DNP3 cold restart command";
  content:"|05 64|"; offset:0; depth:2;
  content:"|0d|"; offset:12; depth:1;
  flow:to_server,established;
  classtype:attempted-dos;
  sid:3000020; rev:1;
  priority:1;
)

# DNP3 firmware update command - potential PIPEDREAM indicator
alert tcp any any -> $OT_RTU_SUBNET 20000 (
  msg:"OT-CRITICAL DNP3 file transfer / firmware update";
  content:"|05 64|"; offset:0; depth:2;
  content:"|19|"; offset:12; depth:1;
  flow:to_server,established;
  classtype:attempted-admin;
  sid:3000021; rev:1;
  priority:1;
)

# --- Network Anomaly Detection ---

# New device communicating with PLCs (not in baseline)
alert ip !$AUTHORIZED_OT_HOSTS any -> $OT_PLC_SUBNET any (
  msg:"OT-DETECT Unauthorized device communicating with PLC subnet";
  flow:to_server;
  threshold:type limit, track by_src, count 1, seconds 3600;
  classtype:network-scan;
  sid:3000030; rev:1;
)

# Port scan targeting OT protocols
alert tcp any any -> $OT_NETWORK any (
  msg:"OT-DETECT Port scan targeting industrial protocols";
  flags:S;
  threshold:type threshold, track by_src, count 10, seconds 60;
  classtype:network-scan;
  sid:3000031; rev:1;
)
```

### Step 3: Implement Process Data Anomaly Detection

Monitor physical process data from the historian to detect attacks that manipulate the process while hiding their effects from operators (the Stuxnet attack pattern).

```python
#!/usr/bin/env python3
"""SCADA Process Data Anomaly Detector.

Monitors historian data to detect physical process anomalies
that may indicate cyber attacks manipulating control logic
while spoofing sensor readings (Stuxnet-style attacks).
"""

import json
import sys
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from statistics import mean, stdev
from typing import Optional

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

@dataclass
class ProcessVariable:
    """Represents a monitored process variable."""
    tag_name: str
    description: str
    unit: str
    low_limit: float
    high_limit: float
    rate_of_change_limit: float  # Maximum change per second
    engineering_low: float
    engineering_high: float

@dataclass
class Anomaly:
    """Represents a detected process anomaly."""
    timestamp: str
    tag_name: str
    anomaly_type: str
    severity: str
    current_value: float
    expected_range: str
    description: str
    attack_pattern: str = ""

class ProcessAnomalyDetector:
    """Detects anomalies in SCADA process data from historian."""

    def __init__(self, historian_url, api_key=None):
        self.historian_url = historian_url
        self.api_key = api_key
        self.variables = {}
        self.history = defaultdict(lambda: deque(maxlen=1000))
        self.anomalies = []

    def add_variable(self, var: ProcessVariable):
        """Register a process variable to monitor."""
        self.variables[var.tag_name] = var

    def fetch_current_values(self):
        """Fetch current values from historian API."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        tag_list = list(self.variables.keys())
        params = {"tags": ",".join(tag_list), "count": 1}

        try:
            resp = requests.get(
                f"{self.historian_url}/api/v1/streams/values/current",
                params=params,
                headers=headers,
                timeout=10,
                verify=not os.environ.get("SKIP_TLS_VERIFY", "").lower() == "true",  # Set SKIP_TLS_VERIFY=true for self-signed certs in lab environments
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"[ERROR] Historian API error: {e}")
            return {}

    def check_value(self, tag_name, value, timestamp):
        """Check a process variable value against all detection rules."""
        var = self.variables.get(tag_name)
        if not var:
            return

        self.history[tag_name].append((timestamp, value))

        # Rule 1: Value out of engineering limits
        if value < var.engineering_low or value > var.engineering_high:
            self.anomalies.append(Anomaly(
                timestamp=timestamp,
                tag_name=tag_name,
                anomaly_type="OUT_OF_RANGE",
                severity="critical",
                current_value=value,
                expected_range=f"{var.engineering_low}-{var.engineering_high} {var.unit}",
                description=f"{tag_name} ({var.description}) at {value} {var.unit} - outside engineering limits",
                attack_pattern="Process manipulation - value driven outside safe operating range",
            ))

        # Rule 2: Rate of change exceeds physical limits
        history = list(self.history[tag_name])
        if len(history) >= 2:
            prev_ts, prev_val = history[-2]
            try:
                dt = (datetime.fromisoformat(timestamp) - datetime.fromisoformat(prev_ts)).total_seconds()
                if dt > 0:
                    rate = abs(value - prev_val) / dt
                    if rate > var.rate_of_change_limit:
                        self.anomalies.append(Anomaly(
                            timestamp=timestamp,
                            tag_name=tag_name,
                            anomaly_type="RATE_OF_CHANGE_VIOLATION",
                            severity="high",
                            current_value=value,
                            expected_range=f"Max rate: {var.rate_of_change_limit} {var.unit}/s",
                            description=(
                                f"{tag_name} changing at {rate:.2f} {var.unit}/s "
                                f"(limit: {var.rate_of_change_limit} {var.unit}/s)"
                            ),
                            attack_pattern="Possible sensor spoofing or actuator manipulation",
                        ))
            except (ValueError, TypeError):
                pass

        # Rule 3: Flatline detection (sensor reading not changing when process is active)
        if len(history) >= 20:
            recent_values = [v for _, v in list(history)[-20:]]
            if len(set(recent_values)) == 1:
                self.anomalies.append(Anomaly(
                    timestamp=timestamp,
                    tag_name=tag_name,
                    anomaly_type="FLATLINE_DETECTED",
                    severity="high",
                    current_value=value,
                    expected_range="Expected variation during active process",
                    description=f"{tag_name} flatlined at {value} for 20+ consecutive readings",
                    attack_pattern="Stuxnet-style replay attack - frozen sensor value while process is manipulated",
                ))

        # Rule 4: Statistical anomaly (z-score based)
        if len(history) >= 50:
            values = [v for _, v in list(history)[-50:]]
            avg = mean(values)
            std = stdev(values) if len(values) > 1 else 0
            if std > 0:
                z_score = abs(value - avg) / std
                if z_score > 3.5:
                    self.anomalies.append(Anomaly(
                        timestamp=timestamp,
                        tag_name=tag_name,
                        anomaly_type="STATISTICAL_ANOMALY",
                        severity="medium",
                        current_value=value,
                        expected_range=f"Mean: {avg:.2f}, StdDev: {std:.2f} (z={z_score:.1f})",
                        description=f"{tag_name} value {value} is {z_score:.1f} standard deviations from mean",
                        attack_pattern="Possible gradual process manipulation",
                    ))

    def report_anomalies(self):
        """Print detected anomalies."""
        if not self.anomalies:
            print("[*] No anomalies detected")
            return

        print(f"\n{'='*70}")
        print(f"PROCESS ANOMALY DETECTION REPORT - {len(self.anomalies)} anomalies")
        print(f"{'='*70}")

        for a in self.anomalies:
            print(f"\n  [{a.severity.upper()}] {a.anomaly_type}")
            print(f"    Time: {a.timestamp}")
            print(f"    Tag: {a.tag_name}")
            print(f"    Value: {a.current_value}")
            print(f"    Expected: {a.expected_range}")
            print(f"    Detail: {a.description}")
            if a.attack_pattern:
                print(f"    Attack Pattern: {a.attack_pattern}")

if __name__ == "__main__":
    from collections import defaultdict

    detector = ProcessAnomalyDetector(
        historian_url="https://10.30.1.50:5450",
    )

    # Define monitored process variables for a chemical reactor
    detector.add_variable(ProcessVariable(
        tag_name="REACTOR_01.TEMP",
        description="Reactor 1 Temperature",
        unit="C",
        low_limit=150, high_limit=280,
        rate_of_change_limit=5.0,
        engineering_low=100, engineering_high=350,
    ))
    detector.add_variable(ProcessVariable(
        tag_name="REACTOR_01.PRESSURE",
        description="Reactor 1 Pressure",
        unit="bar",
        low_limit=2.0, high_limit=8.0,
        rate_of_change_limit=0.5,
        engineering_low=0, engineering_high=12.0,
    ))
    detector.add_variable(ProcessVariable(
        tag_name="PUMP_03.FLOW",
        description="Feed Pump 3 Flow Rate",
        unit="m3/h",
        low_limit=5.0, high_limit=25.0,
        rate_of_change_limit=2.0,
        engineering_low=0, engineering_high=30.0,
    ))

    print("[*] Starting process anomaly monitoring...")
    print("[*] Press Ctrl+C to stop and generate report")

    try:
        while True:
            data = detector.fetch_current_values()
            for item in data.get("items", []):
                detector.check_value(
                    item.get("tag"),
                    item.get("value"),
                    item.get("timestamp", datetime.now().isoformat()),
                )
            time.sleep(5)
    except KeyboardInterrupt:
        detector.report_anomalies()
```

### Step 4: Detect Known ICS Malware Indicators

Monitor for indicators of compromise (IOCs) associated with known ICS-targeting malware families.

```yaml
# Known ICS Malware Detection Signatures
# Reference: MITRE ATT&CK for ICS, CISA ICS-CERT advisories

malware_families:
  TRITON_TRISIS:
    description: "Targets Schneider Electric Triconex Safety Instrumented Systems"
    target: "Safety controllers (SIS)"
    network_indicators:
      - protocol: "TriStation"
        port: 1502
        pattern: "Unusual TriStation commands from non-engineering workstation"
      - protocol: "TCP"
        pattern: "Connection to Triconex controller from unauthorized IP"
    host_indicators:
      - "trilog.exe present on engineering workstation"
      - "inject.bin in System32 directory"
      - "imain.bin payload targeting Triconex firmware"
    detection_rule: |
      alert tcp !$SIS_ENGINEERING_WS any -> $SIS_CONTROLLERS 1502 (
        msg:"OT-CRITICAL Unauthorized TriStation connection to SIS";
        flow:to_server; sid:3000100; rev:1; priority:1;)

  INDUSTROYER_CRASHOVERRIDE:
    description: "Targets power grid SCADA via IEC 60870-5-101/104, IEC 61850, OPC DA"
    target: "Power grid substations and SCADA"
    network_indicators:
      - protocol: "IEC 60870-5-104"
        port: 2404
        pattern: "Rapid sequence of control commands outside normal polling"
      - protocol: "OPC DA"
        pattern: "Enumeration of OPC servers followed by write commands"
    host_indicators:
      - "haslo.exe (backdoor launcher)"
      - "61850.dll (IEC 61850 attack module)"
      - "OPC.dll (OPC DA attack module)"
      - "104.dll (IEC 104 attack module)"
    detection_rule: |
      alert tcp any any -> $SUBSTATION_RTU 2404 (
        msg:"OT-CRITICAL Rapid IEC 104 control commands - Industroyer pattern";
        flow:to_server,established;
        threshold:type threshold, track by_src, count 50, seconds 10;
        sid:3000110; rev:1; priority:1;)

  PIPEDREAM_INCONTROLLER:
    description: "Modular ICS attack framework targeting Schneider/OMRON PLCs and OPC UA"
    target: "Multiple PLC vendors (Schneider, OMRON) and OPC UA servers"
    network_indicators:
      - protocol: "CODESYS"
        port: 1217
        pattern: "CODESYS runtime exploitation attempts"
      - protocol: "OPC UA"
        port: 4840
        pattern: "OPC UA server enumeration and unauthorized method calls"
      - protocol: "Modbus"
        port: 502
        pattern: "Rapid Modbus write commands to multiple unit IDs"
    host_indicators:
      - "TAGRUN tool for OPC UA scanning"
      - "CODECALL tool for CODESYS exploitation"
      - "OMSHELL tool for OMRON PLC interaction"
    detection_rule: |
      alert tcp any any -> $OT_NETWORK 1217 (
        msg:"OT-CRITICAL CODESYS runtime connection - PIPEDREAM indicator";
        flow:to_server,established;
        sid:3000120; rev:1; priority:1;)
```

## Key Concepts

| Term | Definition |
|------|------------|
| SCADA | Supervisory Control and Data Acquisition - architecture for remote monitoring and control of industrial processes via RTUs and communication infrastructure |
| IDS/IPS for OT | Intrusion Detection/Prevention Systems designed for industrial protocols, using both signature-based and anomaly-based detection methods |
| Process Anomaly | Deviation in physical process behavior (temperature, pressure, flow) that may indicate cyber manipulation of control systems |
| Man-in-the-Middle (MITM) | Attack intercepting communication between SCADA master and field devices to modify commands or spoof sensor readings |
| Replay Attack | Capturing legitimate SCADA traffic and replaying it to mask malicious changes to the process (used by Stuxnet) |
| Protocol Anomaly | Deviation from expected industrial protocol behavior including unauthorized function codes, unusual polling patterns, or command sequences |

## Tools & Systems

- **Dragos Platform**: OT cybersecurity platform with threat detection powered by Dragos threat intelligence on ICS-targeting activity groups
- **Nozomi Networks Guardian**: OT/IoT visibility and threat detection using asset intelligence, anomaly detection, and vulnerability assessment
- **Claroty xDome**: Cyber-physical systems protection with continuous threat monitoring and alert prioritization
- **Suricata with ET Open ICS rules**: Open-source IDS/IPS with community-maintained rules for industrial protocol detection
- **Zeek (Bro) with OT scripts**: Network security monitor with protocol analyzers for Modbus, DNP3, and BACnet

## Common Scenarios

### Scenario: Detecting TRITON-Style Attack on Safety Systems

**Context**: An OT security monitoring system alerts on unusual TriStation protocol traffic to a Triconex safety controller from an IP address that is not the authorized SIS engineering workstation.

**Approach**:
1. Immediately verify the source IP of the TriStation traffic - is it the authorized SIS engineering workstation or a compromised host?
2. Check if there is an authorized maintenance activity scheduled for the SIS controllers
3. Capture full packet payload of the TriStation communication for forensic analysis
4. Alert the process safety team - SIS compromise is a safety-critical event
5. If unauthorized, isolate the source host from the network immediately
6. Verify SIS controller logic integrity by comparing running logic against known-good backup
7. Check all engineering workstations in the facility for TRITON indicators (trilog.exe, inject.bin)

**Pitfalls**: Never assume SIS traffic anomalies are false positives - TRITON demonstrated that sophisticated attackers specifically target safety systems. Do not restart the SIS controller without first verifying firmware and logic integrity. Avoid alerting only the IT SOC; the process safety team must be immediately engaged for any SIS-related incident.

## Output Format

```
SCADA Attack Detection Report
===============================
Detection Time: YYYY-MM-DD HH:MM:SS UTC
Detection Source: [IDS/Anomaly Detector/Process Monitor]

ALERT DETAILS:
  Alert ID: [unique identifier]
  Severity: Critical/High/Medium/Low
  Attack Category: [Protocol Anomaly/Process Manipulation/Unauthorized Access]
  MITRE ATT&CK for ICS: [Technique ID and name]

  Source: [IP/hostname]
  Target: [IP/hostname - device type]
  Protocol: [Modbus/DNP3/S7comm/etc]
  Detail: [Specific finding description]

BASELINE COMPARISON:
  Normal: [Expected behavior]
  Observed: [Actual behavior that triggered alert]
  Deviation: [How the observed differs from baseline]

RECOMMENDED RESPONSE:
  1. [Immediate containment action]
  2. [Verification step]
  3. [Escalation path]
```