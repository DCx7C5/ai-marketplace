---
name: webapp-design-prototype-review
description: - When testing Node.js or JavaScript-heavy web applications - During assessment of APIs accepting deep-merged JSON objects - When testing client-side JavaScript frameworks for DOM XSS via prototype pollution - During code review of object merge/clone/extend operations - When evaluating npm packages for prototype pollution gadgets
domain: cybersecurity
---
------|-------------|
| Prototype Chain | JavaScript inheritance mechanism where objects inherit from Object.prototype |
| __proto__ | Accessor property that exposes the prototype of an object |
| Pollution Source | Input point that allows setting properties on Object.prototype |
| Pollution Sink | Code that reads a polluted property and performs a dangerous operation |
| Gadget | A property that flows from prototype to a dangerous sink (source-to-sink chain) |
| Deep Merge | Recursive object merge functions that may process __proto__ as a regular key |
| constructor.prototype | Alternative path to access and pollute the prototype object |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| DOM Invader | Burp Suite built-in tool for detecting client-side prototype pollution |
| Prototype Pollution Gadgets Scanner | Burp extension for server-side gadget detection |
| ppfuzz | Automated prototype pollution fuzzer |
| Nuclei | Template-based scanner with prototype pollution templates |
| server-side-prototype-pollution | Burp Scanner check for server-side detection |
| ESLint security plugin | Static analysis for prototype pollution patterns in code |

## Common Scenarios

1. **DOM XSS via Analytics** — Pollute transport_url property to inject JavaScript through analytics tracking scripts that read URL from prototype
2. **RCE via Template Engine** — Exploit EJS/Pug/Handlebars gadgets to execute arbitrary commands through polluted template rendering properties
3. **Admin Privilege Escalation** — Pollute isAdmin or role properties to bypass authorization checks in Node.js applications
4. **JSON Schema Bypass** — Pollute schema validation properties to bypass input validation and inject malicious data
5. **Denial of Service** — Pollute toString or valueOf to crash the application when objects are coerced to primitives

## Output Format

```
## Prototype Pollution Assessment Report
- **Target**: http://target.com
- **Type**: Server-Side Prototype Pollution
- **Impact**: Remote Code Execution via EJS template gadget

### Findings
| # | Source | Gadget | Sink | Impact |
|---|--------|--------|------|--------|
| 1 | POST /api/merge __proto__ | EJS escapeFunction | Template render | RCE |
| 2 | POST /api/profile __proto__ | isAdmin property | Auth middleware | Privilege Escalation |
| 3 | URL ?__proto__[innerHTML] | innerHTML property | DOM write | Client-Side XSS |

### Remediation
- Use Object.create(null) for configuration objects instead of {}
- Freeze Object.prototype with Object.freeze(Object.prototype)
- Sanitize __proto__ and constructor keys in user input
- Use Map instead of plain objects for user-controlled data
- Update vulnerable npm packages (lodash, merge-deep, etc.)
```