---
name: webapp-cache-cachepoisoning
description: - During authorized penetration tests when the application uses CDN or reverse proxy caching (Cloudflare, Akamai, Varnish, Nginx) - When assessing web applications for cache-based vulnerabilities that could affect all users - For testing whether unkeyed HTTP headers are reflected in cached responses - When evaluating cache key behavior and cache de
domain: cybersecurity
---
------|-------------|
| **Cache Key** | The set of request attributes (host, path, query) used to identify cached responses |
| **Unkeyed Input** | HTTP headers or parameters not included in the cache key but reflected in responses |
| **Cache Poisoning** | Injecting malicious content into cached responses that are served to other users |
| **Cache Deception** | Tricking the cache into storing authenticated/private responses as public content |
| **Vary Header** | HTTP header specifying which request headers should be included in the cache key |
| **Cache Buster** | A unique query parameter used to prevent affecting the real cache during testing |
| **TTL (Time to Live)** | Duration a cached response remains valid before being refreshed |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Request interception and cache behavior analysis |
| **Param Miner (Burp Extension)** | Automated discovery of unkeyed HTTP headers and parameters |
| **Web Cache Vulnerability Scanner** | Automated cache poisoning detection tool |
| **curl** | Manual HTTP request crafting with precise header control |
| **Varnishlog** | Varnish cache debugging and log analysis |
| **CDN-specific tools** | Cloudflare Analytics, Akamai Pragma headers for cache diagnostics |

## Common Scenarios

### Scenario 1: X-Forwarded-Host Script Injection
The application reflects the `X-Forwarded-Host` header in script src URLs. This header is not part of the cache key. Sending a request with `X-Forwarded-Host: evil.com` poisons the cache to load JavaScript from the attacker's server for all subsequent visitors.

### Scenario 2: Web Cache Deception on Account Page
A Cloudflare-cached application ignores unknown path segments. Requesting `/account/profile/logo.png` returns the account page while Cloudflare caches it as a static image. Any unauthenticated user can then access the cached account page.

### Scenario 3: Parameter-Based XSS via Cache
UTM tracking parameters are excluded from the cache key but rendered in the page HTML. Injecting `<script>` tags via `utm_content` parameter poisons the cache with stored XSS affecting all visitors.

### Scenario 4: CDN Cache Poisoning via Host Header
Multiple applications are behind the same CDN. Manipulating the Host header causes the CDN to cache a response from one application under another application's cache key.

## Output Format

```
## Web Cache Poisoning Finding

**Vulnerability**: Web Cache Poisoning via Unkeyed Header
**Severity**: High (CVSS 8.6)
**Location**: X-Forwarded-Host header on all pages
**OWASP Category**: A05:2021 - Security Misconfiguration

### Cache Configuration
| Property | Value |
|----------|-------|
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