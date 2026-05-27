---
name: webapp-cache-cachedeception
description: - When testing applications behind CDNs or reverse proxies (Cloudflare, Akamai, Varnish, Nginx) - During assessment of authenticated page caching behavior - When evaluating path normalization differences between caching and origin layers - During bug bounty hunting on applications with aggressive caching policies - When testing for sensitive data e
domain: cybersecurity
---
------|-------------|
| Cache Deception | Tricking CDN into caching authenticated dynamic content as static resource |
| Path Normalization | How CDN and origin differently resolve path segments (../, ;, encoded chars) |
| Cache Key | The identifier CDN uses to store/retrieve cached responses (typically URL path) |
| Static Extension Trick | Appending .css/.js/.png to dynamic URLs to trigger caching behavior |
| Delimiter Discrepancy | Characters (;, ?, #) interpreted differently by cache vs. origin server |
| Cache Poisoning vs Deception | Poisoning modifies cache for all users; deception caches specific victim data |
| Vary Header | HTTP header controlling which request attributes affect cache key |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy for crafting cache deception requests |
| curl | Command-line testing of cache behavior and response headers |
| Web Cache Vulnerability Scanner | Automated tool for detecting cache deception/poisoning |
| Param Miner | Burp extension for discovering unkeyed cache parameters |
| Cloudflare Diagnostics | Analyzing CF-Cache-Status and cf-ray headers |
| Varnish CLI | Direct cache inspection for Varnish-based setups |

## Common Scenarios

1. **Profile Data Theft** — Cache authenticated user profile pages containing PII (email, address, phone) by appending .css extension to profile URLs
2. **API Token Exposure** — Cache API dashboard pages showing tokens and secrets through path manipulation on CDN
3. **Account Takeover** — Cache pages containing session tokens or CSRF tokens, then use stolen tokens for account takeover
4. **Financial Data Exposure** — Cache banking or payment pages showing account balances and transaction history
5. **Admin Panel Caching** — Cache admin pages accessible through delimiter-based path confusion on CDN

## Output Format

```
## Web Cache Deception Report
- **Target**: http://target.com
- **CDN**: Cloudflare
- **Vulnerability**: Path-based cache deception via static extension appending

### Cache Behavior Analysis
| Extension | Cached | Cache-Control | TTL |
|-----------|--------|---------------|-----|
| .css | Yes | public, max-age=86400 | 24h |
| .js | Yes | public, max-age=86400 | 24h |
| .png | Yes | public, max-age=604800 | 7d |

### Exploitation Results
| Victim URL | Cached Data | Sensitive Fields |
|-----------|-------------|-----------------|
| /account/profile/x.css | Full profile page | Email, Name, API Key |
| /account/settings/x.js | Settings page | 2FA backup codes |

### Remediation
- Configure CDN to respect Cache-Control: no-store on dynamic pages
- Implement Vary: Cookie header on authenticated endpoints
- Use path-based routing rules that reject unexpected extensions
- Enable consistent path normalization between CDN and origin
```