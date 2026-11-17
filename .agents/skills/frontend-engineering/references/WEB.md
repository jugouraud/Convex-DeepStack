<!-- Source: FRONTEND_GUIDELINES(2).md, section WEB. Original rule numbers preserved, qualified with FE. -->

## WEB

- **FE.WEB1 M** Treat the browser and web standards as the foundation; use native elements, URLs, events, constraints, forms and platform APIs before custom replacements when they meet requirements.
- **FE.WEB2 M** Establish supported browser/OS/device/input policy. Check feature support and test meaningful fallbacks; `Baseline` labels inform compatibility but do not override project audience data.
- **FE.WEB3 S** Prefer progressive enhancement: meaningful initial HTML/content and core paths should work through reasonable failures of optional JavaScript or enhancements when feasible for the product.
- **FE.WEB4 M** Understand execution environment before using DOM, `window`, storage, timers, network or navigation APIs (SSR, static generation, workers, edge, browser); guard environment-dependent code appropriately.
- **FE.WEB5 M** Do not rely on user-agent sniffing when feature detection suffices; avoid assuming touch implies mobile, hover implies desktop, or viewport width maps to a device class.
- **FE.WEB6 S** Use built-in browser navigation/history semantics and interoperable APIs; require a specific reason for custom scroll, focus, form, dialog or routing behavior.
- **FE.WEB7 M** Test new or experimental platform features against the supported matrix and provide an accessible functional alternative or scoped progressive enhancement when needed.
- **FE.WEB8 S** Prefer HTTPS and robust web defaults; avoid depending on browser quirks, undocumented event ordering or implicit platform coercions.
