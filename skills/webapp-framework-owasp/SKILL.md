---
name: webapp-framework-owasp
description: - When testing running web applications for vulnerabilities like XSS, SQLi, CSRF, and misconfigurations - When SAST alone is insufficient and runtime behavior testing is required - When compliance mandates dynamic security testing of web applications before production - When testing APIs (REST/GraphQL) for authentication, authorization, and injecti
domain: cybersecurity
---
---|------------|
| DAST | Dynamic Application Security Testing — tests running applications by sending requests and analyzing responses |
| Baseline Scan | Quick passive scan that spiders the application without active attacks, suitable for CI/CD |
| Full Scan | Active scan including attack payloads for XSS, SQLi, and other injection vulnerabilities |
| API Scan | Targeted scan using OpenAPI/Swagger specs to test all documented API endpoints |
| Spider | ZAP's crawler that discovers application pages and endpoints by following links |
| Active Scan | Phase where ZAP sends attack payloads to discovered endpoints to find exploitable vulnerabilities |
| Passive Scan | Analysis of HTTP responses for security headers, cookies, and information disclosure without sending attacks |
| Scan Policy | Configuration defining which attack types to enable and their intensity levels |

## Tools & Systems

- **OWASP ZAP**: Open-source web application security scanner for DAST testing
- **zaproxy/action-baseline**: GitHub Action for ZAP passive baseline scanning
- **zaproxy/action-full-scan**: GitHub Action for ZAP active full scanning
- **zaproxy/action-api-scan**: GitHub Action for API-focused scanning with OpenAPI support
- **Nuclei**: Alternative vulnerability scanner with template-based detection for CI/CD integration

## Common Scenarios

### Scenario: Integrating DAST into a Staging Deployment Pipeline

**Context**: A team deploys to staging before production and needs automated DAST scanning between stages to catch runtime vulnerabilities.

**Approach**:
1. Add a DAST job in the pipeline that triggers after successful staging deployment
2. Run ZAP baseline scan first for quick passive feedback (2-5 minutes)
3. Follow with a targeted API scan using the application's OpenAPI specification
4. Configure rules.tsv to FAIL on critical findings (XSS, SQLi) and WARN on headers/cookies
5. Upload ZAP reports as pipeline artifacts for review
6. Block production deployment if any FAIL-level findings are detected
7. Schedule weekly full scans against staging for deeper coverage

**Pitfalls**: ZAP full scans can take 30+ minutes and may overwhelm staging servers with attack traffic. Use baseline scans in CI and full scans on schedule. Running DAST against production without coordination can trigger WAF blocks and incident alerts.

## Output Format

```
ZAP DAST Scan Report
======================
Target: https://staging.example.com
Scan Type: Baseline + API
Date: 2026-02-23
Duration: 4m 32s

FINDINGS:
  FAIL: 3
  WARN: 7
  INFO: 12
  PASS: 45

FAILING ALERTS:
  [HIGH] 40012 - Cross Site Scripting (Reflected)
    URL: https://staging.example.com/search?q=<script>
    Method: GET
    Evidence: <script>alert(1)</script>

  [MEDIUM] 10021 - X-Content-Type-Options Missing
    URL: https://staging.example.com/api/v1/*
    Evidence: Response header missing

  [MEDIUM] 10035 - Strict-Transport-Security Missing
    URL: https://staging.example.com/
    Evidence: HSTS header not present

QUALITY GATE: FAILED (1 HIGH, 2 MEDIUM findings)
```