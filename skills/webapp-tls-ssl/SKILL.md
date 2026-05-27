---
name: webapp-tls-ssl
description: - Testing whether web applications properly enforce HTTPS through HSTS headers and redirect chains - Validating that HSTS preloading is correctly configured and registered in browser preload lists - Demonstrating the risk of cleartext HTTP to stakeholders during authorized security assessments - Assessing whether internal applications and thick cli
domain: cybersecurity
---
---|------------|
| **SSL Stripping** | Downgrade attack that intercepts HTTP-to-HTTPS redirects, maintaining encrypted connection to the server while serving cleartext HTTP to the victim |
| **HSTS (HTTP Strict Transport Security)** | HTTP response header that instructs browsers to only connect via HTTPS for a specified duration, preventing SSL stripping in subsequent visits |
| **HSTS Preloading** | Submission of domains to browser-maintained lists that enforce HTTPS from the very first connection, closing the first-visit vulnerability window |
| **Certificate Transparency** | Public logging framework for TLS certificates that enables detection of misissued certificates but does not prevent SSL stripping |
| **Mixed Content** | Web pages served over HTTPS that load resources (scripts, images) over HTTP, creating partial downgrade vulnerability |
| **Upgrade-Insecure-Requests** | CSP directive that instructs browsers to upgrade HTTP requests to HTTPS, complementing HSTS for mixed content prevention |

## Tools & Systems

- **Bettercap 2.x**: Network attack framework with integrated SSL stripping, HTTP/HTTPS proxying, and credential sniffing
- **sslstrip2**: Dedicated SSL stripping tool that transparently downgrades HTTPS to HTTP with URL rewriting
- **mitmproxy**: TLS-intercepting proxy that can modify response headers to remove HSTS and other security headers
- **curl**: Command-line tool for testing HSTS headers, redirect chains, and certificate validation
- **hstspreload.org**: Public HSTS preload list checker for verifying domain inclusion in browser preload databases

## Common Scenarios

### Scenario: Testing HSTS Implementation on a Banking Web Application

**Context**: A bank deployed HSTS on their online banking portal (banking.example.com) six months ago and wants to verify it effectively prevents SSL stripping. The assessment is authorized to test from a workstation on the same VLAN as the test environment using dedicated test accounts.

**Approach**:
1. Verify HSTS header presence and values: `curl -sI https://banking.example.com | grep -i strict` reveals `max-age=31536000; includeSubDomains; preload`
2. Check HSTS preload status: confirmed the domain is on Chrome and Firefox preload lists
3. Set up Bettercap with ARP spoofing and SSL stripping against a test workstation
4. Attempt to access banking.example.com from the test workstation -- Chrome refuses connection with NET::ERR_CERT_AUTHORITY_INVALID (HSTS prevents downgrade)
5. Test with a fresh browser profile (no HSTS cache) -- still blocked because domain is preloaded
6. Test the bank's mobile app -- app successfully connects over HTTP (does not enforce HSTS), exposing credentials in cleartext
7. Test subdomain api.banking.example.com -- not on preload list, SSL stripping succeeds on first visit before HSTS header is cached

**Pitfalls**:
- Testing with a browser that already has HSTS cached for the target domain and concluding HSTS works, when a first-time visitor might be vulnerable
- Not testing subdomains separately -- `includeSubDomains` only works after the parent domain's HSTS header is received
- Forgetting to test mobile applications which may not respect HSTS headers at all
- Not checking for mixed content that could leak session tokens even with HSTS enabled

## Output Format

```
## SSL Stripping Assessment Report

**Test ID**: SSL-STRIP-2024-001
**Target Application**: banking.example.com
**Test Date**: 2024-03-15

### HSTS Configuration

| Property | Value | Status |
|----------|-------|--------|
| HSTS Header Present | Yes | PASS |
| max-age | 31536000 (1 year) | PASS |
| includeSubDomains | Yes | PASS |
| preload | Yes | PASS |
| In Chrome Preload List | Yes | PASS |

### SSL Stripping Test Results

| Target | Client | HSTS Status | Strip Result |
|--------|--------|-------------|--------------|
| banking.example.com | Chrome (cached) | Active | BLOCKED |
| banking.example.com | Chrome (fresh) | Preloaded | BLOCKED |
| banking.example.com | Mobile App | Not Enforced | VULNERABLE |
| api.banking.example.com | Chrome (fresh) | Not Preloaded | VULNERABLE (first visit) |

### Recommendations
1. Implement TLS certificate pinning in the mobile banking app (Critical)
2. Submit api.banking.example.com to HSTS preload list separately
3. Add Content-Security-Policy: upgrade-insecure-requests header
4. Implement certificate transparency monitoring for the domain
```