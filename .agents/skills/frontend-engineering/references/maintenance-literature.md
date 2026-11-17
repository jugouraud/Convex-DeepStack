# frontend-engineering references, bibliography and maintenance only

### Authoritative reference anchors (maintenance only; not required reading for routine edits)

These sources inform rule construction but do not supersede the project's documented obligations or the current versions of adopted standards. Specific technical advice from older books must be reconciled with modern browser and protocol behavior.

- **Web platform:** [WHATWG HTML Standard](https://html.spec.whatwg.org/); [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web); [ECMAScript](https://tc39.es/ecma262/); [Web Platform Baseline](https://web.dev/baseline/).
- **Accessibility:** [WCAG 2.2](https://www.w3.org/TR/WCAG22/); [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/); [W3C Internationalization](https://www.w3.org/International/quicktips/index.en).
- **Security/privacy:** [OWASP ASVS](https://asvs.owasp.org/); [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html); [MDN CSP Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP); [MDN Trusted Types](https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API).
- **Performance:** [Web Vitals](https://web.dev/articles/vitals); [Learn Performance](https://web.dev/learn/performance); [Rendering on the Web](https://web.dev/articles/rendering-on-the-web); [HTTP Semantics (RFC 9110)](https://www.rfc-editor.org/rfc/rfc9110.html); [HTTP Caching (RFC 9111)](https://www.rfc-editor.org/rfc/rfc9111.html).
- **Framework/testing:** [React — You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) (framework-specific example, not a universal framework rule); [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/); [Playwright Best Practices](https://playwright.dev/docs/best-practices).
- **Discoverability/operations:** [Google Search Central — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide); [Google SRE — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/).
- **Foundational perspectives, not normative standards:** Martin Fowler, *Refactoring*; John Ousterhout, *A Philosophy of Software Design*; *Software Engineering at Google*; Jeremy Keith, *Resilient Web Design*; Ethan Marcotte, *Responsive Web Design*; Brad Frost, *Atomic Design*; Alla Kholmatova, *Design Systems*; Addy Osmani, *Learning JavaScript Design Patterns*; Steve Souders, *High Performance Web Sites*; Ilya Grigorik, *High Performance Browser Networking*; Steve Krug, *Don't Make Me Think*; Jakob Nielsen, *10 Usability Heuristics*.

### Scope and maintenance note

This document specifies **what an agent must preserve and verify**, not a universal mandated framework, package list, folder tree or architecture. Team-specific profiles may add precise runtime versions, browser matrices, accessibility acceptance policies, budgets, naming conventions, test commands and release procedures. Such profiles may strengthen these rules but cannot quietly waive applicable safety, security, privacy, accessibility or behavioral obligations. Review the rulebook periodically; preserve meaningful exception records and historical decisions.
