# frontend-engineering: workflow addendum

> Applies together with [CORE.WORK](../../../../docs/agent-policy/core/WORK.md), never instead of it. All shared WORK1–WORK8 source IDs are aliases to CORE.WORK1–CORE.WORK8. The original specialized wording is retained in docs/agent-policy/sources/original-rulebooks.zip.

- **FE.WORK9 M** Preserve intended visual, keyboard, focus, URL, state, and responsive behavior unless the request changes it. Treat a screenshot-only implementation as unverified until real DOM and interactions are checked.
- **FE.WORK10 S** Choose a proportionate change-risk class (text/style, interaction, state/data, security/auth, build/release) and tailor tests; do not require full-site E2E for a typo or rely on typecheck alone for an auth-flow change.
- **FE.WORK11 M** Do not claim design parity, cross-browser support, accessibility conformance, or performance improvements without the corresponding actual inspection/test/measurement.
- **FE.WORK12 S** Deliver a concise report: files/behavior changed, reason, checks run/results, changed performance if measured, material risks, and concrete follow-up only where needed. Avoid process theater.

### Frontend-specific gated-pass focus (additive to CORE.WORK)

- **Scope:** routes/components, supported browsers and devices, visual/interaction states, focus/keyboard flow, network and API contracts, CSS influence, and SSR/hydration boundaries.
- **Implementation:** prefer existing semantic HTML, accessible components, styling tokens, and local state. Do not rewrite the application for a local change.
- **Subtraction:** challenge new components/hooks/effects/selectors/state/props/assets and CSS overrides, without reducing accessibility.
- **Efficiency:** inspect bundle and asset bytes, request waterfalls, re-renders, layout/paint, hydration, listeners and memory; measure performance claims in representative production builds.
- **Experience/tests:** cover changed loading/empty/error states, keyboard/focus, viewport reflow, routing, API races, and representative browser behavior.
- **Verification:** report only browser, accessibility, visual, build and performance checks actually performed.

### Frontend impact-to-check matrix (WORK5/WORK9/WORK10)

| Changed surface | Minimum relevant inspection/checks | Expand when |
| --- | --- | --- |
| Text/markup | Semantic structure, labels, lint; targeted visual inspection | Copy changes navigation, legal meaning, truncation, language or announcements |
| CSS/layout/tokens | Target viewport(s), overflow, zoom, focus, reduced motion when relevant | Shared styles, breakpoints, themes, RTL, sticky/overlay behavior |
| Component interaction | Keyboard, focus, pointer/touch, disabled/loading/error, unit/component test | Dialogs, composite widgets, screen-reader behavior, cross-component state |
| State/fetch/API | Race/cancel paths, error/retry behavior, URL/cache consistency, contract test | Mutations, optimistic updates, auth/tenant data, offline or realtime |
| Security/auth/privacy | Threat boundary, safe sinks, permission failure, storage/cookie/consent checks | Credentials, private content, uploads, third-party scripts, session transitions |
| Rendering/build/release | Production build, SSR/hydration, route loading and bundle/output review | Changed cache policy, bundler, dependency, edge/server split, broad rollout |
| Performance-sensitive | Representative before/after lab measurement; field data if available | Shared critical path, Core Web Vitals target, high-traffic rollout |
