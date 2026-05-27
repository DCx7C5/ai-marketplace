---
name: webapp-ui-clickjacking
description: "--|-| | / | Not set | Not set | Yes | | /account/settings | Not set | Not set | Yes | | /account/delete | Not set | Not set | Yes | | /transfer | Not set | Not set | Yes | | /login | SAMEORIGIN | - | No |  ### Sensitive Actions Exploitable 1."
domain: cybersecurity
---

--|-|
| / | Not set | Not set | Yes |
| /account/settings | Not set | Not set | Yes |
| /account/delete | Not set | Not set | Yes |
| /transfer | Not set | Not set | Yes |
| /login | SAMEORIGIN | - | No |

### Sensitive Actions Exploitable
1. Account deletion (single click, no re-authentication)
2. Email change (single click, no confirmation)
3. 2FA disable (two clicks, multi-step PoC)
4. Fund transfer (pre-filled form, single click)

### Impact
- Account takeover via email change clickjacking
- Account destruction via delete clickjacking
- Financial loss via transfer clickjacking
- Security downgrade via 2FA disable clickjacking

### Recommendation
1. Add `Content-Security-Policy: frame-ancestors 'none'` to all pages
2. Set `X-Frame-Options: DENY` as fallback for older browsers
3. Require re-authentication for sensitive actions (delete, transfer)
4. Add confirmation dialogs that cannot be pre-filled or auto-submitted
5. Implement SameSite=Strict cookies to reduce session availability in frames
```
