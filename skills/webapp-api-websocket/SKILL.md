---
name: webapp-api-websocket
description: "Webapp Api Websocket."
domain: cybersecurity
---

-|
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
