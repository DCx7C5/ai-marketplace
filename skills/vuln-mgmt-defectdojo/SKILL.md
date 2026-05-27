---
name: vuln-mgmt-defectdojo
description: DefectDojo is an open-source application vulnerability management platform that aggregates findings from 200+ security tools, deduplicates results, tracks remediation progress, and provides executive dashboards. It serves as a central hub for vulnerability management, integrating with CI/CD pipelines, Jira for ticketing, and Slack for notifications
domain: cybersecurity
---
------|------------|--------|
| Nessus | Nessus Scan | CSV/XML |
| OpenVAS | OpenVAS CSV | CSV |
| Qualys | Qualys Scan | XML |
| OWASP ZAP | ZAP Scan | XML/JSON |
| Burp Suite | Burp XML | XML |
| Trivy | Trivy Scan | JSON |
| Semgrep | Semgrep JSON Report | JSON |
| Snyk | Snyk Scan | JSON |
| SonarQube | SonarQube Scan | JSON |
| Checkov | Checkov Scan | JSON |

### CI/CD Integration (GitHub Actions)
```yaml
# .github/workflows/security-scan.yml
name: vuln-mgmt-defectdojo
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep
        run: |
          pip install semgrep
          semgrep --config auto --json -o semgrep_results.json .
      - name: Upload to DefectDojo
        run: |
          curl -X POST "${{ secrets.DD_URL }}/api/v2/reimport-scan/" \
            -H "Authorization: Token ${{ secrets.DD_API_KEY }}" \
            -F "scan_type=Semgrep JSON Report" \
            -F "file=@semgrep_results.json" \
            -F "product_name=${{ github.event.repository.name }}" \
            -F "engagement_name=CI/CD" \
            -F "auto_create_context=true"
```

## Jira Integration

```python
# Configure Jira integration in DefectDojo settings
jira_config = {
    "url": "https://company.atlassian.net",
    "username": "jira-bot@company.com",
    "password": "jira_api_token",
    "default_issue_type": "Bug",
    "critical_mapping_severity": "Blocker",
    "high_mapping_severity": "Critical",
    "medium_mapping_severity": "Major",
    "low_mapping_severity": "Minor",
    "finding_text": "**Vulnerability**: {{ finding.title }}\n**Severity**: {{ finding.severity }}\n**CVE**: {{ finding.cve }}\n**Description**: {{ finding.description }}",
    "accepted_mapping_resolution": "Done",
    "close_status_key": 6,
}
```

## Metrics and Dashboards

### Key Metrics API Queries
```python
# Get finding counts by severity
resp = requests.get(f"{DD_URL}/findings/?limit=0&active=true",
                    headers=HEADERS)
findings = resp.json()

# Get SLA breach counts
resp = requests.get(f"{DD_URL}/findings/?limit=0&active=true&sla_breached=true",
                    headers=HEADERS)

# Get product-level metrics
resp = requests.get(f"{DD_URL}/products/{product_id}/",
                    headers=HEADERS)
product_data = resp.json()
```

## References

- [DefectDojo GitHub](https://github.com/DefectDojo/django-DefectDojo)
- [DefectDojo Documentation](https://defectdojo.github.io/django-DefectDojo/)
- [DefectDojo REST API](https://defectdojo.github.io/django-DefectDojo/integrations/api-v2-docs/)
- [OWASP DefectDojo Project](https://owasp.org/www-project-defectdojo/)
- [DefectDojo Integrations](https://defectdojo.com/integrations)

---

## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "defectdojo" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist