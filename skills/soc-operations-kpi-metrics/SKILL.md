---
name: soc-operations-kpi-metrics
description: "Soc Operations Kpi Metrics."
domain: cybersecurity
---

--|
| **MTTD** | Mean Time to Detect — average time from threat occurrence to SOC alert generation |
| **MTTR** | Mean Time to Respond — average time from detection to incident resolution |
| **MTTA** | Mean Time to Acknowledge — average time from alert generation to analyst assignment |
| **Signal-to-Noise Ratio** | Ratio of true positive alerts to total alerts — higher is better |
| **Dwell Time** | Duration an attacker remains undetected in the environment — key indicator of detection effectiveness |
| **Analyst Utilization** | Percentage of analyst time spent on productive investigation vs. overhead tasks |

## Tools & Systems

- **Splunk Dashboard Studio**: Advanced visualization framework for building interactive SOC metric dashboards
- **Grafana**: Open-source analytics and visualization platform supporting multiple data sources
- **Power BI**: Microsoft business intelligence tool for executive-level reporting and trend analysis
- **ATT&CK Navigator**: MITRE tool for visualizing detection coverage as layered heatmaps
- **ServiceNow Performance Analytics**: ITSM analytics module for tracking incident lifecycle metrics

## Common Scenarios

- **Quarterly Business Review**: Present MTTD/MTTR trends, detection coverage growth, and alert quality improvements
- **Staffing Justification**: Use workload metrics to justify additional analyst headcount or shift adjustments
- **Tool ROI Assessment**: Compare alert quality and response times before and after new tool deployment
- **Compliance Evidence**: Provide documented SOC performance metrics for ISO 27001 or SOC 2 audits
- **Vendor Comparison**: Benchmark SOC metrics against industry peers using surveys (SANS, Ponemon)

## Output Format

```
SOC PERFORMANCE REPORT — March 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY METRICS:
  Metric              Current    Target     Trend    Status
  MTTD                8.3 min    <15 min    -12%     GREEN
  MTTR                3.2 hrs    <4 hrs     -18%     GREEN
  FP Rate             27%        <30%       -5%      GREEN
  TP Rate             41%        >40%       +3%      GREEN
  ATT&CK Coverage     64%        >60%       +3%      GREEN
  Alerts/Analyst/Day  24         <50        -84%     GREEN

INCIDENT SUMMARY:
  Total Incidents:     147 (Critical: 3, High: 23, Medium: 78, Low: 43)
  Avg Resolution:      3.2 hours (Critical: 1.8h, High: 2.9h, Medium: 4.1h)
  SLA Compliance:      94% (Target: >90%)

IMPROVEMENT HIGHLIGHTS:
  [1] RBA deployment reduced daily alerts from 1,847 to 287 (-84%)
  [2] New Sigma rules added 12 ATT&CK techniques to coverage
  [3] SOAR phishing playbook reduced phishing MTTR by 60%

AREAS FOR IMPROVEMENT:
  [1] Lateral movement detection coverage at 58% (below 60% target)
  [2] Night shift MTTD 23% slower than day shift
  [3] 4 critical vulnerability scan tickets overdue on SLA
```
