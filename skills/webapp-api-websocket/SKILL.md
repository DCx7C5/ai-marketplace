---
name: webapp-api-websocket
description: - During authorized penetration tests when the application uses WebSocket connections for real-time features - When assessing chat applications, live notifications, trading platforms, or collaborative editing tools - For testing WebSocket API endpoints for authentication and authorization flaws - When evaluating real-time data streams for injection
domain: cybersecurity
---
------|-------------|
| **WebSocket Handshake** | HTTP upgrade request that transitions the connection from HTTP to WebSocket protocol |
| **CSWSH** | Cross-Site WebSocket Hijacking - exploiting missing Origin validation to hijack sessions |
| **Origin Validation** | Server-side check that the WebSocket upgrade request comes from a trusted origin |
| **Message-level Authorization** | Verifying permissions for each WebSocket message, not just at connection time |
| **WSS** | WebSocket Secure - encrypted WebSocket connection over TLS (equivalent to HTTPS) |
| **Socket.IO** | Popular WebSocket library with automatic fallback to HTTP long-polling |
| **Ping/Pong Frames** | WebSocket keepalive mechanism; can be abused for timing attacks |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | WebSocket interception, modification, and history analysis |
| **wscat** | Command-line WebSocket client for manual testing |
| **websocat** | Versatile command-line WebSocket client written in Rust |
| **Browser DevTools** | Network tab WS filter for inspecting WebSocket frames |
| **Socket.IO Client** | Testing Socket.IO-based WebSocket implementations |
| **Python websockets** | Scripting automated WebSocket attack sequences |

## Common Scenarios

### Scenario 1: Chat Application CSWSH
A real-time chat application validates the user's cookie during the WebSocket handshake but does not check the Origin header. An attacker hosts a page that opens a WebSocket to the chat server, stealing the victim's private messages.

### Scenario 2: Trading Platform Message Injection
A trading platform processes WebSocket messages containing order parameters. SQL injection in the `symbol` field of an order message allows extracting the entire order database through error-based SQLi.

### Scenario 3: Missing Message Authorization
A collaboration tool checks user authentication at WebSocket connection time but does not verify authorization for individual messages. After connecting, a regular user sends admin-level commands to delete workspaces and export user data.

### Scenario 4: Notification Channel IDOR
A notification system subscribes users to channels via WebSocket messages containing channel IDs. Changing the channel ID allows any user to subscribe to any other user's private notification channel.

## Output Format

```
## WebSocket Security Assessment Report

**Vulnerability**: Cross-Site WebSocket Hijacking (CSWSH)
**Severity**: High (CVSS 8.1)
**Location**: wss://target.example.com/ws
**OWASP Category**: A01:2021 - Broken Access Control

### WebSocket Configuration
| Property | Value |
|----------|-------|
| Protocol | WSS (encrypted) |
| Library | Socket.IO 4.x |
| Authentication | Cookie-based session |
| Origin Validation | NOT ENFORCED |
| Message Authorization | NOT ENFORCED |
| Rate Limiting | NOT IMPLEMENTED |

### Findings
| Finding | Severity |
|---------|----------|
| CSWSH - No Origin validation | High |
| Missing message-level authorization | High |
| XSS via chat message injection | Medium |
| No rate limiting on messages | Medium |
| Channel IDOR (subscribe to any channel) | High |
| WebSocket open after logout | Medium |

### Impact
- Private message exfiltration via CSWSH
- Account impersonation through unauthorized message sending
- Cross-channel data access affecting all users
- DoS via message flooding (no rate limits)

### Recommendation
1. Validate the Origin header during WebSocket handshake
2. Implement CSRF tokens in the WebSocket upgrade request
3. Enforce authorization checks on every WebSocket message
4. Sanitize all user input in WebSocket messages (prevent XSS/SQLi)
5. Implement message rate limiting per connection
6. Invalidate WebSocket connections on logout or session expiration
7. Use per-message authentication tokens rather than relying solely on the initial handshake
```