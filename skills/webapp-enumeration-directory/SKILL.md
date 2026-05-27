---
name: webapp-enumeration-directory
description: - During authorized penetration tests when the application handles file paths in URL parameters or request bodies - When testing file download, file view, or file include functionality - For assessing Local File Inclusion (LFI) and Remote File Inclusion (RFI) vulnerabilities - When evaluating template engines, logging systems, or report generators 
domain: cybersecurity
---
------|-------------|
| **Directory Traversal** | Using `../` sequences to navigate to parent directories and access files outside the intended path |
| **Local File Inclusion (LFI)** | Server-side inclusion of local files, potentially leading to code execution |
| **Remote File Inclusion (RFI)** | Including files from external URLs (requires `allow_url_include=On` in PHP) |
| **Null Byte Injection** | Using `%00` to truncate file paths, bypassing extension checks in older PHP versions |
| **PHP Wrappers** | Protocols like `php://filter`, `php://input`, `data://` for reading and executing files |
| **Log Poisoning** | Injecting code into log files and then including them via LFI for code execution |
| **Path Canonicalization** | The process of resolving relative paths to absolute paths, which can be exploited |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | Request interception and Intruder for automated payload testing |
| **ffuf** | Fast fuzzing with LFI/traversal wordlists |
| **dotdotpwn** | Dedicated directory traversal fuzzer with multiple traversal patterns |
| **LFISuite** | Automated LFI exploitation tool with multiple techniques |
| **SecLists** | Comprehensive wordlists including LFI payloads and traversal patterns |
| **Kadimus** | LFI scanning and exploitation tool |

## Common Scenarios

### Scenario 1: File Download Traversal
A document download endpoint at `/download?file=report.pdf` does not validate the file parameter. Replacing the value with `../../../etc/passwd` returns the server's password file.

### Scenario 2: Template LFI to RCE
A PHP application includes templates via `?page=home`. By poisoning the Apache access log with PHP code in the User-Agent header, then including the log file, the attacker achieves remote code execution.

### Scenario 3: Image Path Traversal
An image resizing service accepts `?src=images/photo.jpg`. The application strips `../` once but does not recurse, so `....//....//etc/passwd` bypasses the filter.

### Scenario 4: Windows IIS Configuration Leak
A .NET application serves files via `?path=docs\manual.pdf`. Traversing to `..\..\web.config` exposes the IIS configuration file containing database connection strings.

## Output Format

```
## Directory Traversal Finding

**Vulnerability**: Path Traversal / Local File Inclusion
**Severity**: High (CVSS 8.6)
**Location**: GET /download?file=../../../etc/passwd
**OWASP Category**: A01:2021 - Broken Access Control

### Reproduction Steps
1. Navigate to https://target.example.com/download?file=report.pdf
2. Replace file parameter: ?file=../../../etc/passwd
3. Server returns contents of /etc/passwd

### Files Retrieved
| File | Impact |
|------|--------|
| /etc/passwd | User enumeration (42 accounts) |
| /var/www/html/.env | Database credentials exposed |
| /home/deploy/.ssh/id_rsa | SSH private key recovered |
| /proc/self/environ | Environment variables with API keys |

### Filter Bypass Required
Original `../` stripped by filter. Successful bypass: `....//....//....//etc/passwd`

### Recommendation
1. Use an allowlist of permitted file names rather than accepting arbitrary paths
2. Resolve the canonical path and verify it stays within the intended directory
3. Run the web server with minimal file system permissions
4. Remove sensitive files from web-accessible directories
5. Disable PHP wrappers (allow_url_include, allow_url_fopen) if not required
```