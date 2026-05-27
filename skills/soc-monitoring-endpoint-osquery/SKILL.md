---
name: soc-monitoring-endpoint-osquery
description: Use this skill when: - Deploying osquery across Windows, macOS, and Linux endpoints for fleet-wide visibility - Building threat hunting queries using osquery's SQL interface - Monitoring endpoint compliance (installed software, open ports, running services) - Integrating osquery data with SIEM or Kolide/Fleet for centralized management **Do not use
domain: cybersecurity
---
---|-----------|
| **Osquery** | Open-source endpoint agent that exposes OS state as SQL tables for querying |
| **Schedule** | Periodic queries that run at defined intervals and log results |
| **Pack** | Collection of related queries grouped for specific use cases (IR, compliance) |
| **FleetDM** | Open-source osquery fleet management platform |
| **Differential Results** | Osquery logs only changes between query executions, reducing data volume |

## Tools & Systems

- **Osquery**: https://osquery.io/ - endpoint visibility agent
- **FleetDM**: https://fleetdm.com/ - centralized fleet management
- **Kolide**: Cloud-based osquery management with Slack integration
- **osquery-go**: Go client library for osquery extensions

## Common Pitfalls

- **Query performance**: Complex queries with large table scans impact endpoint performance. Use WHERE clauses and test query cost with `EXPLAIN`.
- **Schedule intervals too aggressive**: Running heavy queries every 60 seconds causes CPU spikes. Use 300-3600 second intervals for most queries.
- **Not using differential mode**: Without differential logging, osquery logs all results every interval. Differential mode logs only changes.
- **Missing event tables**: Some osquery tables require events framework enabled (process_events, socket_events). Enable with `--disable_events=false`.