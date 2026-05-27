---
name: vuln-scanning-openvas
description: OpenVAS (Open Vulnerability Assessment Scanner) is the scanner component of the Greenbone Vulnerability Management (GVM) framework. Authenticated scans use valid credentials (SSH for Linux, SMB for Windows, ESXi for VMware) to log into target systems, enabling detection of local vulnerabilities, missing patches, and misconfigurations that unauthent
domain: cybersecurity
---
---------|-----|----------|
| Full and fast | daba56c8-73ec-11df-a475-002264764cea | Standard production scan |
| Full and deep | 708f25c4-7489-11df-8094-002264764cea | Thorough scan, may be disruptive |
| System Discovery | 8715c877-47a0-438d-98a3-27c7a6ab2196 | Host and service enumeration |

### Create Custom Scan Config for Authenticated Scan
```bash
# Clone "Full and fast" config and customize
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<create_config>
    <copy>daba56c8-73ec-11df-a475-002264764cea</copy>
    <name>Authenticated Full Scan</name>
  </create_config>'
```

## Running the Scan

### Create and Start Scan Task
```bash
# Create scan task
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<create_task>
    <name>Weekly Authenticated Scan - Linux Prod</name>
    <config id="CONFIG_UUID"/>
    <target id="TARGET_UUID"/>
    <scanner id="08b69003-5fc2-4037-a479-93b440211c73"/>
  </create_task>'

# Start the scan task
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<start_task task_id="TASK_UUID"/>'

# Check scan progress
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<get_tasks task_id="TASK_UUID"/>'
```

### Schedule Recurring Scans
```bash
# Create weekly schedule (every Sunday at 2:00 AM UTC)
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<create_schedule>
    <name>Weekly Sunday 2AM</name>
    <icalendar>
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART:20240101T020000Z
RRULE:FREQ=WEEKLY;BYDAY=SU
DURATION:PT12H
END:VEVENT
END:VCALENDAR
    </icalendar>
    <timezone>UTC</timezone>
  </create_schedule>'
```

## Exporting Results

```bash
# Export scan report as XML
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<get_reports report_id="REPORT_UUID" format_id="a994b278-1f62-11e1-96ac-406186ea4fc5"/>'

# Export as CSV
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<get_reports report_id="REPORT_UUID" format_id="c1645568-627a-11e3-a660-406186ea4fc5"/>'

# Use python-gvm for programmatic access
python3 -c "
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeCheckCommandTransform

connection = UnixSocketConnection(path='/run/gvmd/gvmd.sock')
transform = EtreeCheckCommandTransform()
with Gmp(connection=connection, transform=transform) as gmp:
    gmp.authenticate('admin', 'password')
    reports = gmp.get_reports()
    print(f'Total reports: {len(reports)}')
"
```

## Validating Authentication Success

```bash
# Check if credentials were accepted during scan
# In the scan report, look for NVT "Authentication tests" results:
# - OID 1.3.6.1.4.1.25623.1.0.103591 (SSH authentication successful)
# - OID 1.3.6.1.4.1.25623.1.0.90023 (SMB authentication successful)

# Verify via gvm-cli
gvm-cli socket --socketpath /run/gvmd/gvmd.sock --gmp-username admin --gmp-password <password> --xml \
  '<get_results filter="name=SSH rows=10 sort-reverse=severity"/>'
```

## References

- [OpenVAS Official Site](https://www.openvas.org/)
- [Greenbone Community Edition Docs](https://greenbone.github.io/docs/latest/)
- [GVM GitHub Repository](https://github.com/greenbone/openvas-scanner)
- [python-gvm Library](https://github.com/greenbone/python-gvm)
- [GVM Docker Deployment](https://greenbone.github.io/docs/latest/22.4/container/)

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "openvas" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist