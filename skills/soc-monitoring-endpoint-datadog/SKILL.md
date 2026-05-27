---
name: soc-monitoring-endpoint-datadog
description: "Soc Monitoring Endpoint Datadog."
domain: cybersecurity
---

|
| **Cloud SIEM** | Datadog's security information and event management service that analyzes ingested logs in real-time to detect threats using detection rules |
| **Security Signal** | An alert generated when a detection rule matches incoming log data; signals have severity, status (open/triage/closed), and investigation context |
| **Detection Rule** | A query-based rule that evaluates logs or events against conditions (threshold, anomaly, new value, impossible travel) to generate security signals |
| **CSM (Cloud Security Management)** | Datadog platform for infrastructure security including Misconfigurations (compliance benchmarks), Threats (runtime detection), and Vulnerabilities |
| **Workload Protection** | CSM Threats component that monitors file, process, and network activity on hosts and containers using eBPF-based Agent rules |
| **Content Pack** | Pre-built collection of detection rules, dashboards, and log parsers for a specific integration (AWS, Azure, GCP, Okta, etc.) |
| **Agent Rule** | A kernel-level rule evaluated by the Datadog Agent on the host to collect security-relevant events before sending to Datadog for threat detection |
| **Suppression Query** | A filter applied to a detection rule to prevent signals from being generated for known-good activity (reduces false positives) |

## Verification

- [ ] Datadog Agent is installed and reporting on all target hosts (`datadog-agent status` shows security agent running)
- [ ] Security-relevant log sources are ingesting into Datadog (CloudTrail, auth.log, Windows Security Events visible in Log Explorer)
- [ ] Cloud SIEM Content Packs are enabled for all cloud providers in use (AWS, Azure, GCP)
- [ ] Out-of-the-box detection rules are active and generating signals for test events
- [ ] Custom detection rules trigger correctly (test with a simulated failed login burst)
- [ ] Workload Protection (CSM Threats) is enabled and Agent rules are evaluating on hosts
- [ ] Security dashboard displays signal counts, top rules, severity breakdown, and geographic data
- [ ] Notification workflows deliver alerts to Slack, PagerDuty, or Jira for critical and high signals
- [ ] Suppression queries are configured to reduce false positives on noisy rules
- [ ] Security Signals API returns results programmatically for automation integration
