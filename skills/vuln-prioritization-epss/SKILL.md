---
name: vuln-prioritization-epss
description: The Exploit Prediction Scoring System (EPSS) is a data-driven model developed by FIRST (Forum of Incident Response and Security Teams) that estimates the probability of a CVE being exploited in the wild within the next 30 days. EPSS produces scores from 0.0 to 1.0 (0% to 100%) using machine learning trained on real-world exploitation data. Unlike C
domain: cybersecurity
---
--------|-----------|----------|--------|
| > 0.7 | >= 9.0 | P0 - Immediate | Remediate within 24 hours |
| > 0.7 | >= 7.0 | P1 - Urgent | Remediate within 48 hours |
| > 0.4 | >= 7.0 | P2 - High | Remediate within 7 days |
| > 0.1 | >= 4.0 | P3 - Medium | Remediate within 30 days |
| <= 0.1 | >= 7.0 | P3 - Medium | Remediate within 30 days |
| <= 0.1 | < 7.0 | P4 - Low | Remediate within 90 days |

### EPSS Percentile Thresholds
- **Top 1% (percentile >= 0.99)**: Extremely likely to be exploited; treat as Critical
- **Top 5% (percentile >= 0.95)**: High exploitation probability; prioritize remediation
- **Top 10% (percentile >= 0.90)**: Elevated risk; schedule for near-term remediation
- **Bottom 50%**: Low exploitation probability; handle in normal patch cycle

## Implementation

```python
import requests
import pandas as pd
from datetime import datetime

def fetch_epss_scores(cve_list):
    """Fetch EPSS scores for a list of CVEs from FIRST API."""
    scores = {}
    batch_size = 100
    for i in range(0, len(cve_list), batch_size):
        batch = cve_list[i:i + batch_size]
        resp = requests.get(
            "https://api.first.org/data/v1/epss",
            params={"cve": ",".join(batch)},
            timeout=30
        )
        if resp.status_code == 200:
            for entry in resp.json().get("data", []):
                scores[entry["cve"]] = {
                    "epss": float(entry["epss"]),
                    "percentile": float(entry["percentile"]),
                    "date": entry.get("date", ""),
                }
    return scores

def prioritize_vulnerabilities(scan_results_csv, output_csv):
    """Enrich scan results with EPSS scores and assign priorities."""
    df = pd.read_csv(scan_results_csv)
    cve_list = df["cve_id"].dropna().unique().tolist()

    epss_data = fetch_epss_scores(cve_list)

    df["epss_score"] = df["cve_id"].map(lambda c: epss_data.get(c, {}).get("epss", 0))
    df["epss_percentile"] = df["cve_id"].map(lambda c: epss_data.get(c, {}).get("percentile", 0))

    def assign_priority(row):
        epss = row.get("epss_score", 0)
        cvss = row.get("cvss_score", 0)
        if epss > 0.7 and cvss >= 9.0:
            return "P0"
        if epss > 0.7 and cvss >= 7.0:
            return "P1"
        if epss > 0.4 and cvss >= 7.0:
            return "P2"
        if epss > 0.1 or cvss >= 7.0:
            return "P3"
        return "P4"

    df["priority"] = df.apply(assign_priority, axis=1)
    df = df.sort_values(["priority", "epss_score"], ascending=[True, False])
    df.to_csv(output_csv, index=False)
    print(f"[+] Prioritized {len(df)} vulnerabilities -> {output_csv}")
    print(f"    P0: {len(df[df['priority']=='P0'])}")
    print(f"    P1: {len(df[df['priority']=='P1'])}")
    print(f"    P2: {len(df[df['priority']=='P2'])}")
    print(f"    P3: {len(df[df['priority']=='P3'])}")
    print(f"    P4: {len(df[df['priority']=='P4'])}")
    return df
```

## EPSS Trend Analysis

```python
def fetch_epss_timeseries(cve_id):
    """Get historical EPSS scores for trend analysis."""
    resp = requests.get(
        "https://api.first.org/data/v1/epss",
        params={"cve": cve_id, "scope": "time-series"},
        timeout=30
    )
    if resp.status_code == 200:
        return resp.json().get("data", [])
    return []

def detect_epss_spikes(cve_id, threshold=0.3):
    """Detect significant EPSS score increases indicating emerging threats."""
    timeseries = fetch_epss_timeseries(cve_id)
    if len(timeseries) < 2:
        return False
    sorted_data = sorted(timeseries, key=lambda x: x.get("date", ""))
    latest = float(sorted_data[-1].get("epss", 0))
    previous = float(sorted_data[-2].get("epss", 0))
    increase = latest - previous
    if increase >= threshold:
        print(f"[!] EPSS spike detected for {cve_id}: {previous:.3f} -> {latest:.3f} (+{increase:.3f})")
        return True
    return False
```

## References

- [FIRST EPSS Official](https://www.first.org/epss/)
- [EPSS API Documentation](https://www.first.org/epss/api)
- [EPSS Model Documentation](https://www.first.org/epss/model)
- [EPSS Data Downloads](https://epss.cyentia.com/)
- [Cyentia Institute Research](https://www.cyentia.com/epss/)

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "epss" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist