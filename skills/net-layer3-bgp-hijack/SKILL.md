---
name: net-layer3-bgp-hijack
description: "Net Layer3 Bgp Hijack."
domain: cybersecurity
---

--|
| More-specific /25 hijack | Enabled | BLOCKED (Invalid origin) |
| More-specific /25 hijack | Disabled | SUCCESSFUL (traffic diverted) |
| Exact-match origin hijack | Enabled | BLOCKED (Invalid origin) |
| Route leak via customer | Enabled | NOT BLOCKED (valid origin, wrong path) |

### Recommendations
1. Create ROA for 198.51.100.0/24 (currently unprotected)
2. Set max-length to /24 in ROAs to prevent more-specific hijacks
3. Request upstream ISPs enable RPKI Route Origin Validation
4. Deploy BGPalerter for continuous prefix monitoring
5. Register with IRR databases and request prefix filtering from peers
```
