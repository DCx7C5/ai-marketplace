---
name: webapp-api-42crunch
description: 42Crunch is an API security platform that combines Shift-Left security testing with Shield-Right runtime protection. It provides API Audit for static security analysis of OpenAPI definitions, API Conformance Scan for dynamic vulnerability detection, and API Protect for real-time threat prevention. The platform integrates into CI/CD pipelines and ID
domain: cybersecurity
---
------|----------|-----|
| No authentication defined | Critical | Add securitySchemes and security requirements |
| Missing input validation | High | Add type, format, pattern, maxLength constraints |
| Server URL uses HTTP | High | Change server URLs to HTTPS |
| No error responses defined | Medium | Add 4xx and 5xx response definitions |
| additionalProperties not restricted | Medium | Set additionalProperties: false on object schemas |
| Missing rate limiting | Medium | Add x-rateLimit extension or use API Protect |

## Key Security Checks

42Crunch evaluates APIs against these critical security areas:

- **BOLA Prevention**: Validates that object-level authorization patterns are defined
- **BFLA Prevention**: Checks for function-level access control definitions
- **Injection Prevention**: Ensures input parameters have proper type/format/pattern constraints
- **Data Exposure**: Verifies response schemas limit returned properties
- **Security Misconfiguration**: Checks authentication schemes, transport security, CORS settings
- **Mass Assignment**: Validates that request bodies use explicit property allowlists

## References

- 42Crunch API Security Platform: https://42crunch.com/api-security-platform/
- 42Crunch Documentation: https://docs.42crunch.com/
- Microsoft Defender for Cloud 42Crunch Integration: https://learn.microsoft.com/en-us/azure/defender-for-cloud/onboarding-guide-42crunch
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x00-header/
- Jenkins Plugin for 42Crunch: https://plugins.jenkins.io/42crunch-security-audit/