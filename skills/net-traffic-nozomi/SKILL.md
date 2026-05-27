---
name: net-traffic-nozomi
description: "Net Traffic Nozomi."
domain: cybersecurity
---

|
| Guardian | Nozomi Networks passive sensor that monitors OT network traffic via SPAN/TAP without generating additional traffic |
| Vantage | Nozomi cloud-based central management platform for aggregating data across multiple Guardian sensors |
| Behavioral Anomaly Detection (BAD) | Nozomi's AI-driven approach to detecting deviations from learned normal OT network behavior |
| Smart Polling | Nozomi's active query feature using native protocols to safely extract additional device details |
| Asset Intelligence | Nozomi's automatic identification and classification of OT/IoT assets from network traffic |
| Threat Intelligence Feed | Nozomi Labs-maintained feed of OT-specific threat indicators, updated based on global honeypot data |

## Output Format

```
NOZOMI GUARDIAN OT MONITORING REPORT
=======================================
Site: [site name]
Date: YYYY-MM-DD

ASSET VISIBILITY:
  Total Assets: [count]
  PLCs: [count] | HMIs: [count] | Switches: [count]
  Protocols: [list]
  Vendors: [top 5]

THREAT DETECTION:
  Critical Alerts: [count]
  High Alerts: [count]
  Top Alert Categories: [list]

VULNERABILITIES:
  Critical: [count]
  High: [count]

NETWORK ANALYSIS:
  Communication Links: [count]
  Cross-Zone Flows: [count]
```
