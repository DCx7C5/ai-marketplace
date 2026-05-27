---
name: net-traffic-nozomi
description: - When deploying passive OT network monitoring using Nozomi Networks Guardian sensors - When requiring asset visibility without active scanning in sensitive ICS environments - When building a Nozomi-based OT SOC with centralized management via Vantage or CMC - When integrating OT network monitoring with Fortinet, Splunk, or ServiceNow ecosystems - 
domain: cybersecurity
---
SYSTEM STATUS ---")
                print(f"  Version: {status.get('version', 'N/A')}")
                print(f"  Uptime: {status.get('uptime', 'N/A')}")
                print(f"  Packets Processed: {status.get('packets_processed', 'N/A')}")
                print(f"  Threat Intelligence: {status.get('threat_intelligence_version', 'N/A')}")
        except requests.RequestException as e:
            print(f"  [!] System status unavailable: {e}")

        # Asset discovery summary
        nodes = self.get_nodes()
        print(f"\n--- ASSET DISCOVERY ---")
        print(f"  Total Nodes Discovered: {len(nodes)}")

        type_counts = defaultdict(int)
        vendor_counts = defaultdict(int)
        protocol_set = set()
        for node in nodes:
            type_counts[node.get("type", "unknown")] += 1
            vendor_counts[node.get("vendor", "Unknown")] += 1
            for proto in node.get("protocols", []):
                protocol_set.add(proto)

        print(f"\n  By Type:")
        for ntype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"    {ntype}: {count}")

        print(f"\n  By Vendor:")
        for vendor, count in sorted(vendor_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"    {vendor}: {count}")

        print(f"\n  Protocols Observed: {', '.join(sorted(protocol_set))}")

        # Alert summary
        alerts = self.get_alerts(severity="high")
        print(f"\n--- ALERT SUMMARY ---")
        print(f"  High/Critical Alerts: {len(alerts)}")

        alert_types = defaultdict(int)
        for alert in alerts:
            alert_types[alert.get("type_id", "unknown")] += 1

        for atype, count in sorted(alert_types.items(), key=lambda x: -x[1])[:10]:
            print(f"    {atype}: {count}")

        # Vulnerability summary
        vulns = self.get_vulnerabilities()
        print(f"\n--- VULNERABILITY SUMMARY ---")
        print(f"  Total Vulnerabilities: {len(vulns)}")

        sev_counts = defaultdict(int)
        for vuln in vulns:
            sev_counts[vuln.get("severity", "unknown")] += 1

        for sev in ["critical", "high", "medium", "low"]:
            if sev in sev_counts:
                print(f"    {sev.capitalize()}: {sev_counts[sev]}")

    def analyze_communication_patterns(self):
        """Analyze OT communication patterns for anomalies."""
        links = self.get_links()
        nodes = {n.get("id"): n for n in self.get_nodes()}

        print(f"\n--- COMMUNICATION ANALYSIS ---")
        print(f"  Total Communication Links: {len(links)}")

        # Identify cross-zone communications
        cross_zone = []
        for link in links:
            src_node = nodes.get(link.get("source_id"), {})
            dst_node = nodes.get(link.get("destination_id"), {})
            src_zone = src_node.get("zone", "unknown")
            dst_zone = dst_node.get("zone", "unknown")

            if src_zone != dst_zone and src_zone != "unknown" and dst_zone != "unknown":
                cross_zone.append({
                    "source": src_node.get("label", "Unknown"),
                    "source_zone": src_zone,
                    "destination": dst_node.get("label", "Unknown"),
                    "dest_zone": dst_zone,
                    "protocols": link.get("protocols", []),
                })

        if cross_zone:
            print(f"\n  Cross-Zone Communications: {len(cross_zone)}")
            for comm in cross_zone[:10]:
                print(f"    {comm['source']} ({comm['source_zone']}) -> "
                      f"{comm['destination']} ({comm['dest_zone']}) "
                      f"via {', '.join(comm['protocols'])}")

if __name__ == "__main__":
    manager = NozomiGuardianManager(
        guardian_url="https://nozomi-guardian.plant.local",
        api_token="your-api-token",
    )

    manager.validate_deployment()
    manager.analyze_communication_patterns()
```

## Key Concepts

| Term | Definition |
|------|------------|
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