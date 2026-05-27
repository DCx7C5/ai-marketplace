---
name: webapp-api-wafgateway-monitor
description: - When deploying API Gateway endpoints that require protection against common web attacks - When implementing rate limiting and throttling to prevent API abuse and DDoS attacks - When building bot detection and mitigation for API endpoints exposed to the internet - When compliance requires WAF protection for all public-facing API endpoints - When c
domain: cybersecurity
---
---|------------|
| Web ACL | AWS WAF access control list that defines the collection of rules and their actions (allow, block, count) applied to associated resources |
| Managed Rule Group | Pre-configured set of WAF rules maintained by AWS or third-party vendors for common attack patterns like OWASP Top 10 |
| Rate-Based Rule | WAF rule that tracks request rates per IP address and blocks traffic exceeding a defined threshold within a 5-minute window |
| Bot Control | AWS WAF managed rule group that identifies and manages automated traffic including scrapers, crawlers, and attack bots |
| IP Reputation List | AWS-maintained list of IP addresses associated with malicious activity including botnets, scanners, and known attackers |
| Custom Response | WAF capability to return specific HTTP status codes and custom response bodies when blocking requests |

## Tools & Systems

- **AWS WAF**: Web application firewall service for protecting API Gateway, ALB, CloudFront, and AppSync endpoints
- **AWS Managed Rules**: Pre-built rule groups for common attack patterns maintained by AWS security team
- **AWS Firewall Manager**: Central management of WAF policies across multiple accounts in AWS Organizations
- **Kinesis Firehose**: Streaming delivery service for WAF logs to S3, Elasticsearch, or third-party analytics
- **CloudWatch**: Monitoring service for WAF metrics including allowed, blocked, and counted requests

## Common Scenarios

### Scenario: Protecting a Public API from Credential Stuffing and Bot Attacks

**Context**: A public REST API experiences thousands of authentication attempts per hour from automated bots attempting credential stuffing against the `/api/auth/login` endpoint.

**Approach**:
1. Create a Web ACL with AWS Managed Rules Common Rule Set for baseline protection
2. Add a rate-based rule limiting the login endpoint to 100 requests per IP per 5 minutes
3. Enable Bot Control managed rules to detect and block automated traffic
4. Add IP Reputation List to block known malicious IPs proactively
5. Create a custom rule blocking requests without proper User-Agent headers
6. Enable WAF logging and create CloudWatch alarms for high block rates
7. Review sampled blocked requests weekly to tune rules and reduce false positives

**Pitfalls**: Rate limiting by IP can block legitimate users behind shared NAT gateways or corporate proxies. Consider using API key or authenticated session-based rate limiting for more granular control. Bot Control rules in COMMON inspection level may block legitimate API clients; start in Count mode and review before switching to Block.

## Output Format

```
AWS WAF API Gateway Security Report
======================================
Web ACL: api-gateway-waf
Associated Resource: API Gateway - production-api (prod stage)
Report Period: 2026-02-16 to 2026-02-23

TRAFFIC SUMMARY:
  Total requests:              2,450,000
  Allowed requests:            2,380,000 (97.1%)
  Blocked requests:               70,000 (2.9%)

BLOCKS BY RULE:
  RateLimitPerIP:              28,000 (40%)
  AWSManagedRulesCommonRuleSet: 18,000 (25.7%)
  BotControl:                  12,000 (17.1%)
  SQLiRuleSet:                  5,000 (7.1%)
  IPReputationList:             4,000 (5.7%)
  RateLimitLogin:               2,000 (2.9%)
  GeoRestriction:               1,000 (1.4%)

TOP BLOCKED IPs:
  185.x.x.x:     8,400 requests (rate limited)
  45.x.x.x:      5,200 requests (bot detected)
  198.x.x.x:     3,100 requests (SQLi attempts)

ATTACK TYPES BLOCKED:
  Credential stuffing (login endpoint):  2,000
  SQL injection attempts:                5,000
  Cross-site scripting:                  3,200
  Known bad bot traffic:                12,000
  Rate limit violations:               28,000

WAF RULE HEALTH:
  Rules in Block mode:    8 / 10
  Rules in Count mode:    2 / 10 (under evaluation)
  False positive rate:    < 0.1%
```