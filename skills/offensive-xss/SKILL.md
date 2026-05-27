---
name: offensive-xss
description: - Look for user input opportunities on the application. When user input is stored and used to construct a web page later, test the input field for stored XSS. if user input in a URL gets reflected back on the resulting web page, test for reflected and DOM XSS.
domain: cybersecurity
---
----------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **React 19**   | `dangerouslySetInnerHTML`, `use()` hook with unsanitized data, concurrent rendering races    | Hydration mismatch bugs, `useFormStatus` edge cases                 |
| **Vue 3.4+**   | `v-html`, dynamic component names (`:<is="...">`)`, `v-html` with Composition API refs       | Server-side rendering XSS in `renderToString`                       |
| **Svelte 5**   | `{@html ...}`, runes (`$state`, `$derived`) with HTML content, event directives              | Fine-grained reactivity can bypass sanitization                     |
| **Next.js 15** | `next/script strategy="beforeInteractive"`, Server Actions with unvalidated input, edge gaps | Turbopack dev server XSS (CVE-2024-XXXXX), RSC serialization issues |
| **Solid 2.0**  | `innerHTML` in reactive statements, `<Dynamic>` component with user props                    | Signal-based XSS when reactivity wraps unsafe HTML                  |
| **Astro 4.x**  | `set:html` in `.astro` components, framework islands with unescaped props                    | Server-side XSS in content collections                              |
| **Qwik**       | `dangerouslySetInnerHTML` equivalent, resumability serialization issues                      | Hydration boundary XSS                                              |
| **Remix 2.x**  | Loader data XSS, `<Scripts/>` with inline data, Form action injection                        | Deferred loader data without sanitization                           |
| **Angular 17** | `bypassSecurityTrust*` methods, `[innerHTML]` binding, custom element XSS                    | SSR hydration mismatch, signal-based XSS                            |

### Detection & Monitoring (AI‑assisted)

| Tool                   | Notes                             |
| ---------------------- | --------------------------------- |
| **Acunetix 15**        | LLM‑powered mutation engine       |
| **Burp Suite 2024.8**  | “DAST+AI” context‑aware scan mode |
| **XSSInspector AI/ML** | RL‑based payload generator        |
| **ParamSpider 3**      | LLM‑enhanced parameter discovery  |