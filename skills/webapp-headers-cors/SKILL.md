---
name: webapp-headers-cors
description: "-| | https://evil.com | Yes | Yes | | null | Yes | Yes | | http://localhost | Yes | Yes | | https://evil."
domain: cybersecurity
---

-|
| https://evil.com | Yes | Yes |
| null | Yes | Yes |
| http://localhost | Yes | Yes |
| https://evil.target.example.com | Yes | Yes |

### Impact
- Any website can read authenticated API responses in victim's browser
- User profile data (email, phone, address) exfiltrable
- Session tokens exposed via X-Auth-Token header
- CSRF protection bypassed (attacker can read and submit anti-CSRF tokens)

### Recommendation
1. Implement a strict allowlist of trusted origins
2. Never reflect arbitrary Origin values in Access-Control-Allow-Origin
3. Do not allow Origin: null with credentials
4. Validate origins with exact string matching, not regex substring matching
5. Set Access-Control-Max-Age to a reasonable value (600 seconds)
```
