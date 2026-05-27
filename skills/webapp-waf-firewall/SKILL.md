---
name: webapp-waf-firewall
description: - When confirmed vulnerabilities are blocked by WAF signature-based detection - During penetration testing where WAF prevents exploitation of known issues - When evaluating WAF rule effectiveness against evasion techniques - During red team engagements requiring bypass of perimeter security controls - When testing custom WAF rules for completeness 
domain: cybersecurity
---
------|-------------|
| Signature Evasion | Obfuscating payloads to avoid matching WAF regex patterns |
| Encoding Bypass | Using URL, Unicode, or HTML encoding to disguise malicious characters |
| Protocol-Level Bypass | Exploiting HTTP protocol features (chunked encoding, method override) |
| Tamper Scripts | SQLMap modules that transform payloads to evade specific WAF rules |
| Content-Type Confusion | Sending payloads in unexpected content types the WAF does not inspect |
| Parameter Pollution | Splitting payloads across duplicate parameters to evade per-parameter inspection |
| Behavioral vs Signature | WAF detection modes: pattern matching (bypassable) vs. anomaly detection (harder) |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| wafw00f | WAF fingerprinting and identification |
| SQLMap | Automated SQL injection with WAF bypass tamper scripts |
| waf-bypass.com | Community-maintained WAF bypass payload database |
| Awesome-WAF | Curated GitHub repository of WAF bypass techniques |
| Burp Suite | HTTP proxy for manual payload crafting and WAF response analysis |
| XSStrike | XSS scanner with WAF detection and bypass capabilities |

## Common Scenarios

1. **SQLi Through JSON** — Bypass WAF by sending SQL injection payloads inside JSON request bodies that are not inspected by the WAF rules
2. **XSS via Event Handlers** — Use alternative HTML event handlers (onpageshow, onanimationstart) not covered by WAF signature rules
3. **Encoding Chain Bypass** — Apply multiple layers of encoding (URL + Unicode + HTML entity) to evade each decoding layer of the WAF
4. **Chunked Transfer Bypass** — Split malicious payload across HTTP chunked transfer encoding segments to avoid pattern matching
5. **Method Override** — Send attack payloads via PUT/PATCH methods or custom headers that WAF does not inspect

## Output Format

```
## WAF Bypass Assessment Report
- **Target**: http://target.com
- **WAF Identified**: Cloudflare (via cf-ray header)
- **Bypass Achieved**: Yes

### WAF Detection Results
| Payload Type | Blocked | Bypass Found |
|-------------|---------|-------------|
| Basic SQLi | Yes | Yes (JSON encoding) |
| UNION SELECT | Yes | Yes (inline comments) |
| XSS <script> | Yes | Yes (SVG onload) |
| Path Traversal | No | N/A (not blocked) |

### Successful Bypass Payloads
| # | Original (Blocked) | Bypass Payload | Technique |
|---|-------------------|---------------|-----------|
| 1 | 1' OR 1=1-- | {"id":"1' OR 1=1--"} | JSON content-type |
| 2 | UNION SELECT | /*!50000UNION*/ /*!50000SELECT*/ | MySQL version comments |
| 3 | <script>alert(1)</script> | <svg/onload=alert(1)> | Alternative tag+event |

### Remediation
- Enable JSON body inspection in WAF rules
- Implement behavioral analysis alongside signature detection
- Add rules for uncommon HTML tags and event handlers
- Enable deep content inspection for all HTTP methods
- Implement request normalization before rule evaluation
```