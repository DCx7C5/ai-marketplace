---
name: webapp-cache-cachepoisoning
description: "-| | CDN/Cache | Cloudflare | | Cache-Control | max-age=3600, public | | Unkeyed Headers | X-Forwarded-Host, X-Forwarded-Proto | | Affected Pages | All HTML pages (/*."
domain: cybersecurity
---

-|
| CDN/Cache | Cloudflare |
| Cache-Control | max-age=3600, public |
| Unkeyed Headers | X-Forwarded-Host, X-Forwarded-Proto |
| Affected Pages | All HTML pages (/*.html) |

### Reproduction Steps
1. Send request with X-Forwarded-Host: evil.example.com
2. Response includes: <link href="https://evil.example.com/style.css">
3. This response is cached by Cloudflare for 3600 seconds
4. All subsequent visitors receive the poisoned response

### Impact
- JavaScript execution in all users' browsers (via poisoned script src)
- Credential theft, session hijacking, defacement
- Affects estimated 50,000 daily visitors during 1-hour cache window
- Can be re-poisoned continuously for persistent attack

### Recommendation
1. Include X-Forwarded-Host and similar headers in the cache key via Vary header
2. Do not reflect unkeyed headers in response content
3. Configure the cache to strip unknown headers before forwarding to origin
4. Use application-level hardcoded base URLs instead of deriving from headers
5. Implement cache key normalization to prevent key manipulation
```
