---
name: soc-operations-alert-tuning
description: "Soc Operations Alert Tuning."
domain: cybersecurity
---

--|
| **Alert Fatigue** | Cognitive overload from excessive alert volumes leading analysts to dismiss or ignore valid alerts |
| **Risk-Based Alerting (RBA)** | Detection approach aggregating risk contributions from multiple events before generating a single high-context alert |
| **Signal-to-Noise Ratio** | Ratio of true positive alerts to false positives — higher ratio indicates better alert quality |
| **False Positive Rate** | Percentage of alerts classified as benign after investigation — target <30% for production rules |
| **Alert Consolidation** | Grouping related alerts from the same source/campaign into a single investigation unit |
| **Detection Tuning** | Process of refining rule logic to exclude known benign patterns while maintaining true positive detection |

## Tools & Systems

- **Splunk ES Risk-Based Alerting**: Framework converting individual detections into cumulative risk scores per entity
- **Splunk ES Adaptive Response**: Actions that can auto-close, suppress, or route alerts based on enrichment results
- **Elastic Detection Rules**: Built-in severity and risk score assignment with exception lists for tuning
- **Chronicle SOAR**: Google's SOAR platform with automated alert deduplication and grouping capabilities
- **Tines**: No-code SOAR platform enabling custom alert routing and automated enrichment workflows

## Common Scenarios

- **Post-RBA Implementation**: Convert 15 threshold alerts into risk contributions, reducing daily volume by 85%
- **Quarterly Tuning Cycle**: Review top 20 noisiest rules, apply exclusions, measure FP rate improvement
- **New Tool Deployment**: After deploying new EDR, tune initial detection rules to baseline the environment
- **Analyst Capacity Planning**: Calculate optimal alert-to-analyst ratio (target 40-60 alerts/analyst/shift)
- **Compliance Balance**: Maintain detection coverage for compliance while reducing operational alert volume

## Output Format

```
ALERT FATIGUE REDUCTION REPORT — Q1 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before (January 2024):
  Daily Alert Volume:     1,847
  Alerts/Analyst/Shift:   154
  False Positive Rate:    82%
  True Positive Rate:     8%
  Signal-to-Noise:        0.10
  Analyst Morale:         Low (2 resignations in Q4)

After (March 2024):
  Daily Alert Volume:     287 (-84%)
  Alerts/Analyst/Shift:   24
  False Positive Rate:    23% (-72% improvement)
  True Positive Rate:     41% (+413% improvement)
  Signal-to-Noise:        1.78

Changes Implemented:
  [1] Risk-Based Alerting deployed (15 rules converted)       -1,200 alerts/day
  [2] Top 10 noisy rules tuned with exclusion lists           -280 alerts/day
  [3] Alert consolidation (5-min dedup window)                -80 alerts/day
  [4] Tier 1 auto-close for low-confidence alerts             -N/A (removed from queue)

Detection Coverage Impact: NONE — ATT&CK coverage maintained at 67%
True Positive Detection Rate: IMPROVED — 12 additional true positives caught per week
```
