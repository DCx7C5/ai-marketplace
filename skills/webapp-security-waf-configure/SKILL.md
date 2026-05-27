---
name: webapp-security-waf-configure
description: - When deploying new web applications or APIs behind cloud load balancers requiring OWASP protection - When application penetration testing reveals SQL injection, XSS, or other injection vulnerabilities - When experiencing brute force, credential stuffing, or bot attacks against authentication endpoints - When compliance requirements mandate a WAF 
domain: cybersecurity
---
---|------------|
| Web ACL | Web Access Control List defining the set of rules evaluated against every HTTP request to a protected resource |
| Managed Rule Group | Pre-configured rule set maintained by the cloud provider or third-party vendor covering common attack patterns |
| Rate-Based Rule | WAF rule that tracks request rates per IP address and blocks IPs exceeding the threshold within a time window |
| Count Mode | WAF action that logs matching requests without blocking them, used for rule validation before enforcement |
| Rule Priority | Numerical ordering determining which rules are evaluated first; lower numbers have higher priority |
| Custom Response | WAF capability to return specific HTTP status codes and headers when blocking requests |
| Scope-Down Statement | Condition that narrows a rate-based rule to specific URI paths, methods, or headers |
| False Positive | Legitimate request incorrectly blocked by a WAF rule, requiring rule tuning or exclusion |

## Tools & Systems

- **AWS WAF**: Cloud-native WAF integrated with ALB, CloudFront, API Gateway, and AppSync
- **Azure WAF**: Web application firewall on Application Gateway or Front Door with OWASP CRS rule sets
- **AWS Firewall Manager**: Centralized WAF policy management across multiple AWS accounts in an Organization
- **WAF Security Automations**: AWS solution that deploys Lambda-based automated WAF rule updates based on log analysis
- **CloudWatch Metrics**: Monitoring dashboard for tracking WAF rule match rates, block counts, and allowed requests

## Common Scenarios

### Scenario: Credential Stuffing Attack Against Authentication API

**Context**: An e-commerce application experiences 50,000 login attempts per hour from a botnet using stolen credential lists. The attacker rotates source IPs every few minutes to evade simple IP-based blocking.

**Approach**:
1. Deploy rate-based rules limiting login endpoint requests to 10 per 5 minutes per IP
2. Enable AWS WAF Bot Control managed rule group to detect automated request patterns beyond IP rotation
3. Add a custom rule requiring valid CAPTCHA tokens for login requests exceeding 5 failures
4. Implement IP reputation blocking using AWSManagedRulesAmazonIpReputationList
5. Create a custom rule matching on User-Agent patterns common to credential stuffing tools
6. Monitor blocked request metrics and adjust thresholds based on legitimate traffic patterns

**Pitfalls**: Setting rate limits too aggressively blocks legitimate users behind shared NAT IPs. Blocking by User-Agent alone is easily bypassed by rotating agent strings.

## Output Format

```text
Cloud WAF Configuration Report
================================
Web ACL: production-waf
Scope: Regional (us-east-1)
Protected Resources: ALB (arn:aws:elasticloadbalancing:...)
Report Date: 2025-02-23

RULE CONFIGURATION:
  [P0] RateLimitLogin          - BLOCK (100 req/5min/IP)
  [P1] AWSManagedRulesCommon   - BLOCK (1 exclusion: SizeRestrictions_BODY)
  [P2] AWSManagedRulesSQLi     - BLOCK
  [P3] AWSManagedRulesKnownBad - BLOCK
  [P4] AWSManagedRulesBotControl - COUNT (evaluation phase)
  [P5] GeoBlockRule            - BLOCK (12 countries blocked)

TRAFFIC ANALYSIS (Last 7 Days):
  Total Requests:    2,847,293
  Allowed:           2,791,456 (98.0%)
  Blocked:              51,234 (1.8%)
  Counted:               4,603 (0.2%)

TOP BLOCKED RULES:
  RateLimitLogin:              23,456 blocks (45.8%)
  SQLi Detection:               8,234 blocks (16.1%)
  CommonRuleSet (XSS):          7,891 blocks (15.4%)
  GeoBlockRule:                 6,543 blocks (12.8%)
  KnownBadInputs:              5,110 blocks (10.0%)

FALSE POSITIVE ANALYSIS:
  Reported False Positives: 3
  Confirmed False Positives: 1 (SizeRestrictions_BODY for /api/upload)
  Action Taken: Rule exclusion applied
```