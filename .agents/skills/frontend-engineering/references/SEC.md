<!-- Source: FRONTEND_GUIDELINES(2).md, section SEC. Original rule numbers preserved, qualified with FE. -->

## SEC

- **FE.SEC1 M** Render untrusted content as text by default. For allowed rich HTML, use a maintained sanitizer with suitable configuration and safe insertion; untrusted strings must never reach executable HTML/JS/CSS contexts unescaped.
- **FE.SEC2 M** Avoid `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, dangerous framework HTML escape hatches and active URL schemes with untrusted data; require explicit reviewed justification for any such sink.
- **FE.SEC3 M** Prevent DOM XSS in URLs, attributes, templates, SVG, Markdown, SSR serialization and third-party widgets; validate protocol/destination for navigations or embeds influenced by users.
- **FE.SEC4 M** Use a context-appropriate CSP as defense in depth for production surfaces when deployment supports it; prefer nonce/hash-based strict policies and test them before enforcement. CSP does not replace safe output handling.
- **FE.SEC5 S** Consider Trusted Types enforcement when supported and suitable for the stack; its policy must actually sanitize/validate and unsupported browsers still require safe code paths.
- **FE.SEC6 M** Treat `postMessage` and cross-frame/window communication as trust boundaries: verify sender origin/source and message schema; never send credentials/private data to arbitrary origins.
- **FE.SEC7 M** Use HTTPS for production authenticated/sensitive pages and resources; avoid mixed content and apply security headers, iframe restrictions, referrer policy and embedding controls appropriate to the product.
- **FE.SEC8 M** Isolate and review third-party scripts, analytics, embedded content and browser SDKs for data access, injection, performance, CSP and outage risk; minimize privileges and load them only when necessary.
- **FE.SEC9 M** Never ship server secrets or privileged keys in `public`/browser-exposed environment variables, sourcemaps, static assets, HTML or bundled modules. Assume every client-delivered byte is inspectable.
- **FE.SEC10 M** Treat dependency upgrades, transitive packages and build plugins as supply-chain changes; verify provenance and security impact, preserve lockfile integrity and resolve relevant advisories.
- **FE.SEC11 M** For file uploads, enforce authoritative server file/size/content rules. Browser previews or MIME hints do not make a file safe; avoid rendering untrusted SVG/HTML in privileged origins.
- **FE.SEC12 M** Validate external URLs and redirect targets; use `rel="noopener noreferrer"` or platform-equivalent isolation where needed for external windows, and do not trust user-controlled navigation schemes.
- **FE.SEC13 M** Do not expose unauthorized data in initial HTML, preloaded route payloads, service-worker caches, client stores or hidden DOM, even if the visible UI conceals it.
- **FE.SEC14 S** Review security-sensitive error and loading states for account enumeration and data leakage; keep diagnostics separate from displayed messages.
- **FE.SEC15 M** Keep credentialed requests explicit and intentional; distinguish same-site and same-origin, cookie sending, CSRF defense, CORS policy and navigation behavior.
