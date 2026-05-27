---
name: webapp-api-inventory
description: "-| | Total APIs Discovered | 127 | | Documented APIs | 82 | | Shadow APIs (undocumented) | 31 | | Zombie APIs (deprecated) | 14 | | APIs Without Authentication | 8 | | APIs Exposing Sensitive Data | 5 |  ### Critical Findings  1."
domain: cybersecurity
---

-|
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
