---
name: webapp-api-inventory
description: - Mapping the complete API attack surface of an organization before a security assessment - Identifying shadow APIs deployed by development teams without security review - Discovering deprecated or zombie API versions that remain accessible but unmaintained - Finding undocumented API endpoints exposed through mobile applications, SPAs, or microserv
domain: cybersecurity
---
---|------------|
| **Shadow API** | An API deployed by a development team without going through the official API management or security review process |
| **Zombie API** | A deprecated or old API version that remains accessible and running but is no longer maintained or monitored |
| **API Inventory** | A comprehensive catalog of all APIs in an organization including endpoint URLs, owners, versions, authentication methods, and data classifications |
| **Improper Inventory Management** | OWASP API9:2023 - failure to maintain an accurate API inventory, leading to unmonitored and unprotected API endpoints |
| **Attack Surface** | The total set of API endpoints, methods, and parameters that an attacker can potentially interact with |
| **API Sprawl** | The uncontrolled proliferation of APIs in an organization, often resulting from microservice adoption without centralized governance |

## Tools & Systems

- **Amass**: OWASP tool for attack surface mapping through DNS enumeration, web scraping, and API discovery
- **httpx**: Fast HTTP probing tool for validating discovered domains and identifying live API endpoints
- **nuclei**: Template-based scanner for detecting exposed API documentation, debug endpoints, and misconfigured services
- **Swagger UI Detector**: Tool for finding exposed Swagger/OpenAPI documentation endpoints across the organization
- **Akto**: API security platform that discovers APIs through traffic analysis and maintains an automated inventory

## Common Scenarios

### Scenario: Enterprise API Attack Surface Assessment

**Context**: A large enterprise has 200+ development teams using microservices. The security team suspects many undocumented APIs are exposed to the internet. A comprehensive API inventory is needed for a security audit.

**Approach**:
1. DNS enumeration discovers 340 subdomains, 45 contain API-related keywords (api, rest, gateway, backend)
2. Active probing of all subdomains with API path wordlist discovers 127 live API endpoints
3. JavaScript analysis of the main web application reveals 34 API endpoints, 8 of which point to undocumented internal services
4. AWS API Gateway inventory shows 67 REST APIs and 23 HTTP APIs across 12 accounts
5. Cross-referencing against the official API catalog: 31 shadow APIs (undocumented), 14 zombie APIs (deprecated versions)
6. 3 zombie APIs have no authentication, exposing customer data through endpoints that were supposed to be decommissioned
7. 2 shadow APIs expose internal admin functions to the internet without authorization

**Pitfalls**:
- Only checking documented API endpoints and missing shadow APIs deployed outside the API gateway
- Not scanning JavaScript bundles where frontend applications hardcode API endpoint URLs
- Missing APIs behind non-standard ports or subpaths
- Not checking for multiple API versions where older versions may lack security controls
- Assuming all APIs go through the API gateway when some may be directly exposed

## Output Format

```
## API Inventory and Discovery Report

**Organization**: Example Corp
**Assessment Date**: 2024-12-15
**Domains Scanned**: 340

### Summary

| Category | Count |
|----------|-------|
| Total APIs Discovered | 127 |
| Documented APIs | 82 |
| Shadow APIs (undocumented) | 31 |
| Zombie APIs (deprecated) | 14 |
| APIs Without Authentication | 8 |
| APIs Exposing Sensitive Data | 5 |

### Critical Findings

1. **Zombie API**: api-v1.example.com/api/v1/users - Deprecated in 2022,
   still accessible, no authentication required, returns full user data
2. **Shadow API**: internal-tools.example.com/api/admin - Admin functions
   exposed to internet without authorization
3. **Exposed Documentation**: 12 Swagger UI instances accessible publicly,
   revealing full API schema and endpoint details
```