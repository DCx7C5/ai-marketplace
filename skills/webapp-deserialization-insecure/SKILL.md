---
name: webapp-deserialization-insecure
description: - During authorized penetration tests when applications process serialized data (cookies, API parameters, message queues) - When identifying Java serialization markers (`ac ed 00 05` / `rO0AB`) in HTTP traffic - For testing PHP applications that use `unserialize()` on user-controlled input - When evaluating .NET applications using `BinaryFormatter`
domain: cybersecurity
---
------|-------------|
| **Serialization** | Converting an object into a byte stream for storage or transmission |
| **Deserialization** | Reconstructing an object from a byte stream, potentially executing code |
| **Gadget Chain** | A sequence of existing class methods chained together to achieve arbitrary code execution |
| **Magic Methods** | Special methods called automatically during deserialization (`__wakeup`, `__destruct` in PHP, `readObject` in Java) |
| **ViewState** | ASP.NET mechanism for persisting page state, often containing serialized objects |
| **Pickle** | Python's native serialization format, inherently unsafe for untrusted data |
| **URLDNS Gadget** | A Java gadget that triggers DNS lookup, useful for safe deserialization detection |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **ysoserial** | Java deserialization payload generator with multiple gadget chains |
| **ysoserial.net** | .NET deserialization payload generator |
| **PHPGGC** | PHP Generic Gadget Chains for multiple frameworks |
| **Burp Java Deserialization Scanner** | Automated detection of Java deserialization vulnerabilities |
| **marshalsec** | Java unmarshaller exploitation for various libraries |
| **Freddy (Burp Extension)** | Detects deserialization issues in multiple languages |

## Common Scenarios

### Scenario 1: Java Session Cookie RCE
A Java application stores session data as serialized objects in cookies. The `rO0AB` prefix reveals Java serialization. Using ysoserial with CommonsCollections gadget chain achieves remote code execution.

### Scenario 2: PHP Laravel Unserialize
A Laravel application passes serialized data through a hidden form field. Using PHPGGC to generate a Laravel RCE gadget chain achieves command execution when the form is submitted.

### Scenario 3: .NET ViewState Without MAC
An ASP.NET application has ViewState MAC validation disabled. Using ysoserial.net to generate a malicious ViewState payload achieves code execution when the page processes the modified ViewState.

### Scenario 4: Python Pickle in Redis Cache
A Python web application stores pickled objects in Redis for caching. By poisoning the cache with a malicious pickle payload, code execution is triggered when the application deserializes the cached object.

## Output Format

```
## Insecure Deserialization Finding

**Vulnerability**: Insecure Deserialization - Remote Code Execution
**Severity**: Critical (CVSS 9.8)
**Location**: Cookie `user_session` (Java serialized object)
**OWASP Category**: A08:2021 - Software and Data Integrity Failures

### Reproduction Steps
1. Capture the `user_session` cookie value (starts with rO0AB)
2. Generate payload: java -jar ysoserial.jar CommonsCollections5 "id"
3. Base64 encode and replace the cookie value
4. Send request; command executes on the server

### Vulnerable Library
- commons-collections 3.2.1 (CVE-2015-7501)
- Java Runtime: OpenJDK 11.0.15

### Confirmed Impact
- Remote Code Execution as `tomcat` user
- Server OS: Ubuntu 22.04 LTS
- Internal network access confirmed via reverse shell
- Database credentials accessible from application config

### Recommendation
1. Avoid deserializing untrusted data; use JSON or Protocol Buffers instead
2. Upgrade commons-collections to 4.1+ (patched version)
3. Implement deserialization filters (JEP 290 for Java 9+)
4. Use allowlists for permitted classes during deserialization
5. Implement integrity checks (HMAC) on serialized data before deserialization
```