---
name: webapp-api-websocket-wssecurity
description: "Webapp Api Websocket Wssecurity."
domain: cybersecurity
---

|
| **WebSocket** | Full-duplex communication protocol over a single TCP connection, established via HTTP upgrade handshake |
| **CSWSH** | Cross-Site WebSocket Hijacking - an attack where a malicious website initiates a WebSocket connection to a legitimate server using the victim's browser credentials |
| **Origin Validation** | Server-side check of the Origin header during WebSocket handshake to prevent CSWSH by rejecting connections from unauthorized domains |
| **WebSocket Frame** | The basic unit of data in WebSocket communication, containing opcode, masking, payload length, and payload data |
| **Upgrade Handshake** | HTTP request with `Upgrade: websocket` and `Connection: Upgrade` headers that establishes the WebSocket connection |
| **Message Flooding** | Sending a large volume of WebSocket messages to exhaust server resources (memory, CPU, bandwidth) |

## Tools & Systems

- **Burp Suite Professional**: Intercepts WebSocket handshakes and messages, allows message modification and replay
- **OWASP ZAP**: WebSocket testing with message fuzzing, interception, and breakpoint capabilities
- **wscat**: Command-line WebSocket client for manual testing: `wscat -c wss://target.com/ws -H "Authorization: Bearer token"`
- **websocat**: Advanced CLI WebSocket tool with proxy, broadcast, and scripting capabilities
- **Autobahn TestSuite**: Comprehensive WebSocket protocol compliance and security testing framework

## Common Scenarios

### Scenario: Chat Application WebSocket Security Assessment

**Context**: A messaging application uses WebSocket for real-time chat. The WebSocket endpoint handles message delivery, typing indicators, read receipts, and user presence. Authentication is cookie-based.

**Approach**:
1. Analyze the WebSocket handshake: connection established at `wss://chat.example.com/ws` with session cookie authentication
2. Test CSWSH: WebSocket server does not validate the Origin header - an attacker's page can connect and receive the victim's messages
3. Test authentication: WebSocket accepts connections with expired session cookies (session validation only at handshake, not for subsequent messages)
4. Test authorization: User A can send messages to private channels they are not a member of by crafting the channel ID
5. Test injection: Message content is stored without sanitization; XSS payload in message body executes in other users' browsers
6. Test message flooding: Server accepts 5000 messages per second without rate limiting, causing CPU spike
7. Find that WebSocket messages include the sender's internal user ID, email, and IP address (information leakage)

**Pitfalls**:
- Not testing CSWSH because the application uses token-based authentication (cookies are automatically sent with WebSocket)
- Only testing the initial handshake authentication without verifying ongoing message authorization
- Missing injection vulnerabilities because payloads are in JSON WebSocket frames instead of HTTP parameters
- Not testing reconnection behavior (does the server re-validate authentication on reconnect?)
- Ignoring that WebSocket connections may bypass HTTP-level rate limiting and WAF rules

## Output Format

```
## Finding: Cross-Site WebSocket Hijacking Enables Real-Time Data Theft

**ID**: API-WS-001
**Severity**: High (CVSS 8.1)
**Affected Endpoint**: wss://chat.example.com/ws

**Description**:
The WebSocket server does not validate the Origin header during the
handshake. An attacker can host a malicious web page that opens a
WebSocket connection to the chat server using the victim's session
cookie. All messages, typing indicators, and presence data are
forwarded to the attacker in real time.

**Proof of Concept**:
Host the CSWSH PoC page on attacker.com. When a logged-in user
visits the page, the JavaScript establishes a WebSocket connection
to the chat server. The server authenticates the connection using
the victim's cookie and delivers all real-time chat data to the
attacker's connection.

**Impact**:
Real-time interception of all private messages, presence data,
and typing indicators for any user who visits the attacker's page.

**Remediation**:
1. Validate the Origin header against an allowlist of legitimate domains
2. Implement CSRF tokens in the WebSocket handshake URL
3. Use token-based authentication (Authorization header) instead of cookies for WebSocket
4. Implement per-message authorization checks, not just connection-level authentication
5. Add rate limiting on WebSocket message volume per connection
```
