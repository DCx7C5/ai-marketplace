---
name: soc-tuning-falsepositivereduction
description: False positive alerts are non-malicious events that trigger security rules, overwhelming SOC analysts with noise. Studies show that up to 45% of SIEM alerts are false positives, and a typical SOC analyst can only investigate 20-25 alerts per shift effectively. Reducing false positives requires systematic tuning across thresholds, correlation logic,
domain: cybersecurity
---
|---|---|
| False Positive Rate | FP / (FP + TP) * 100 | < 20% |
| Alert Volume Reduction | (Old Volume - New Volume) / Old Volume * 100 | 30-50% per quarter |
| Mean Triage Time | Total triage time / Total alerts | < 8 minutes |
| Rule Precision | TP / (TP + FP) | > 0.80 |
| Analyst Satisfaction | Survey score | > 4/5 |

## References

- [CyberSierra - Tune SIEM Alerts to Eliminate False Positives](https://cybersierra.co/blog/reduce-false-positives-siem/)
- [ConnectWise - 9 Ways to Eliminate SIEM False Positives](https://www.connectwise.com/blog/9-ways-to-eliminate-siem-false-positives)
- [Prophet Security - Alert Tuning Best Practices](https://www.prophetsecurity.ai/blog/security-operations-center-soc-best-practices-alert-tuning)
- [ManageEngine - Reducing SIEM Alert False Positives](https://www.manageengine.com/log-management/siem/reducing-siem-alert-false-positives.html)