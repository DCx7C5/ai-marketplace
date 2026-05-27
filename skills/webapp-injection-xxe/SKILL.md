---
name: webapp-injection-xxe
description: - During authorized penetration tests when the application processes XML input (SOAP APIs, file uploads, RSS feeds) - When testing APIs that accept `Content-Type: application/xml` or `text/xml` - For assessing XML parsers in file upload functionality (DOCX, XLSX, SVG, PDF) - When evaluating SOAP-based web services for entity injection - During secu
domain: cybersecurity
---
------|-------------|
| **XML External Entity** | An entity defined in a DTD that references external resources via SYSTEM or PUBLIC keywords |
| **DTD (Document Type Definition)** | Defines the structure and legal elements of an XML document, including entity declarations |
| **Internal Entity** | Entity defined with a value directly in the DTD (`<!ENTITY name "value">`) |
| **External Entity** | Entity that loads content from a URI (`<!ENTITY name SYSTEM "uri">`) |
| **Parameter Entity** | Entity used within the DTD itself, prefixed with `%` (`<!ENTITY % name SYSTEM "uri">`) |
| **Blind XXE** | XXE where entity values are not reflected in the response, requiring out-of-band exfiltration |
| **Billion Laughs (DoS)** | Recursive entity expansion attack causing exponential memory consumption |
| **XXE to SSRF** | Using XXE to make the server send HTTP requests to internal or external services |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Request interception, modification, and Collaborator for OOB detection |
| **XXEinjector** | Automated XXE exploitation with file exfiltration and SSRF capabilities |
| **interactsh** | Out-of-band interaction server for detecting blind XXE callbacks |
| **xxeserv** | Dedicated FTP/HTTP server for XXE data exfiltration |
| **OWASP ZAP** | Automated XXE scanning in active scan mode |
| **DTD-Finder** | Discovers DTD files on the server for entity injection |

## Common Scenarios

### Scenario 1: SOAP API File Read
A SOAP web service processes XML input without disabling external entities. Injecting a DTD with a SYSTEM entity in the SOAP body reads `/etc/passwd` and returns it in the SOAP response.

### Scenario 2: SVG Upload Blind XXE
An image upload feature accepts SVG files. The SVG is parsed server-side for thumbnail generation. Using a blind XXE payload in the SVG, server files are exfiltrated via out-of-band HTTP requests.

### Scenario 3: JSON to XML Content-Type Switch
A REST API primarily uses JSON but the XML parser is also enabled. Switching `Content-Type` to `application/xml` and sending an XXE payload exposes server files through the API response.

### Scenario 4: DOCX Processing XXE
A resume upload feature processes DOCX files. Injecting XXE into the `[Content_Types].xml` file within the DOCX archive triggers file read when the document is parsed server-side.

## Output Format

```
## XXE Injection Finding

**Vulnerability**: XML External Entity (XXE) Injection
**Severity**: Critical (CVSS 9.1)
**Location**: POST /api/search (Content-Type: application/xml)
**OWASP Category**: A05:2021 - Security Misconfiguration

### Reproduction Steps
1. Send POST request to /api/search with Content-Type: application/xml
2. Include DTD with external entity: <!ENTITY xxe SYSTEM "file:///etc/passwd">
3. Reference entity in XML body: <search>&xxe;</search>
4. Server returns file contents in the response

### Confirmed Impact
- Local file read: /etc/passwd, /etc/hostname, application config files
- SSRF: Accessed AWS metadata at 169.254.169.254
- Internal network scanning: Identified internal services on ports 3306, 6379, 8080

### Files Retrieved
| File | Contents Summary |
|------|-----------------|
| /etc/passwd | 42 user accounts, service accounts identified |
| /var/www/html/config.php | Database credentials in plaintext |
| /etc/hostname | Internal hostname: prod-web-01 |

### Recommendation
1. Disable external entity processing in the XML parser
2. Disable DTD processing entirely if not required
3. Use JSON instead of XML where possible
4. Implement input validation to reject DTD declarations in XML input
5. Apply least-privilege file system permissions for the web server user
```