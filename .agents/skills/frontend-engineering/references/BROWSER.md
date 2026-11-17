<!-- Source: FRONTEND_GUIDELINES(2).md, section BROWSER. Original rule numbers preserved, qualified with FE. -->

## BROWSER

- **FE.BROWSER1 M** Define the target browser/OS/device matrix from audience and obligations, not only the developer's primary browser. Review compatibility for newly introduced APIs/CSS features.
- **FE.BROWSER2 M** Check server-rendered and hydrated output for mismatches, hydration warnings and altered behavior; do not conceal hydration issues by disabling warnings or broadly turning off SSR.
- **FE.BROWSER3 S** Prefer responsive testing across meaningful content breakpoints and input modes, including coarse pointer/keyboard, rather than assuming common device pixel dimensions cover all cases.
- **FE.BROWSER4 M** Test route reloads, deep links, history/back-forward and refresh paths for any routing change; account for direct server navigation as well as client-side transitions.
- **FE.BROWSER5 M** Consider autofill, browser password managers, zoom, text scaling, virtual keyboards and browser-native form behaviors when changing critical forms/navigation.
- **FE.BROWSER6 S** Prefer progressive fallback when modern APIs are unavailable; use polyfills only when the project audience and functional need justify their complexity/bytes.
- **FE.BROWSER7 M** Preserve consistent server/client locale, time, random values and initial state during SSR; delay browser-only personalization until hydration where unavoidable.
- **FE.BROWSER8 S** Verify mobile browser chrome, safe areas, fixed/sticky overlays and scroll behavior on actual target devices for complex viewport-sensitive experiences.
