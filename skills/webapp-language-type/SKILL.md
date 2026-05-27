---
name: webapp-language-type
description: - When testing PHP web applications for authentication bypass vulnerabilities - During assessment of password comparison and hash verification logic - When testing applications using loose comparison (== instead of ===) - During code review of PHP applications handling JSON or deserialized input - When evaluating input validation that relies on typ
domain: cybersecurity
---
------|-------------|
| Loose Comparison (==) | PHP comparison that performs type coercion before comparing values |
| Strict Comparison (===) | PHP comparison requiring both value and type to match |
| Magic Hash | String whose hash starts with "0e" followed by digits, evaluating to 0 in loose comparison |
| Type Coercion | Automatic conversion between types (string to int, null to 0) during comparison |
| strcmp Bypass | Passing array to strcmp() returns NULL, which equals 0 in loose comparison |
| JSON Type Control | Using JSON input to send specific types (boolean, integer, null) to PHP endpoints |
| Scientific Notation | PHP interprets "0eN" strings as 0 in exponential notation during numeric comparison |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy for changing parameter types in requests |
| PHP interactive shell | Local testing of type juggling behavior |
| PayloadsAllTheThings | Curated magic hash and type juggling payload lists |
| phpggc | PHP generic gadget chains for deserialization exploitation |
| Custom Python scripts | Automated type juggling payload testing |
| PHPStan/Psalm | Static analysis tools detecting loose comparisons in code |

## Common Scenarios

1. **Authentication Bypass via Boolean** — Send `"password": true` as JSON to bypass loose comparison password verification
2. **Magic Hash Collision** — Use known magic hash input ("240610708") whose MD5 starts with "0e" to match against stored hashes
3. **strcmp Array Bypass** — Send `password[]=anything` to make strcmp() return NULL, bypassing password comparison
4. **PIN/OTP Bypass** — Send integer 0 as verification code to match against "0e..." hash of the actual code
5. **Role Escalation** — Send `"role": true` to match any non-empty role string in loose comparison access checks

## Output Format

```
## Type Juggling Vulnerability Report
- **Target**: http://target.com
- **Language**: PHP 8.1
- **Framework**: Laravel

### Findings
| # | Endpoint | Parameter | Payload | Type | Impact |
|---|----------|-----------|---------|------|--------|
| 1 | POST /login | password | true (boolean) | Loose comparison | Auth bypass |
| 2 | POST /login | password | 240610708 (magic hash) | MD5 0e collision | Auth bypass |
| 3 | POST /login | password[] | array | strcmp NULL return | Auth bypass |
| 4 | POST /verify | code | 0 (integer) | Numeric comparison | OTP bypass |

### PHP Comparison Table (Relevant)
| Expression | Result | Reason |
|-----------|--------|--------|
| 0 == "password" | TRUE | String cast to 0 |
| true == "password" | TRUE | Non-empty string is truthy |
| "0e123" == "0e456" | TRUE | Both are scientific notation = 0 |
| NULL == 0 | TRUE | NULL cast to 0 |

### Remediation
- Replace all == with === (strict comparison) in security-critical code
- Use password_verify() for password comparison instead of direct comparison
- Use hash_equals() for timing-safe hash comparison
- Validate input types before comparison operations
- Enable PHP strict_types declaration in all files
```