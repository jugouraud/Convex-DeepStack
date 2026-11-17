<!-- Source: FRONTEND_GUIDELINES(2).md, section ARCH. Original rule numbers preserved, qualified with FE. -->

## ARCH

- **FE.ARCH1 M** For significant design changes, define routes, rendering mode, data freshness, auth boundaries, user flows, reliability, scale, team ownership, browser targets and quality goals; record the simplest credible alternative.
- **FE.ARCH2 S** Prefer a cohesive modular frontend with feature-aligned ownership. Split deployables, microfrontends, packages or runtime plugins only for demonstrated team, isolation or deployment needs and their integration costs.
- **FE.ARCH3 M** Establish explicit public module APIs and dependency direction; avoid cyclic imports, reaching into another feature's private files/state, and accidental server-to-client secret leakage.
- **FE.ARCH4 S** Separate route assembly, feature logic, shared design primitives and external adapters without creating multiple redundant abstraction tiers. Organize by reason to change rather than rigid file-name ideology.
- **FE.ARCH5 M** Select static, server-rendered, streamed, client-rendered, or hybrid rendering per route using content, interactivity, SEO, latency, auth, deployment and hydration requirements; do not force one strategy across all routes.
- **FE.ARCH6 S** Keep orchestration at route or feature boundaries, isolate reusable pure behavior, and keep substantial configurable infrastructure at a clear composition boundary.
- **FE.ARCH7 M** Mark server-only, client-only and edge/runtime boundaries; prevent importing privileged code, secret environment values, filesystem APIs or server dependencies into browser bundles.
- **FE.ARCH8 S** Adopt architectural changes incrementally, preserve route/API compatibility and rollback where practical; do not combine migrations with unrelated redesigns.
- **FE.ARCH9 M** Define ownership for cross-tab/session state, shared caches, fetch coordination and concurrent writes; do not disguise distributed consistency problems as local UI state.
- **FE.ARCH10 S** Document 3–5 prioritized quality scenarios for large frontend systems (e.g. slow mobile first load, authenticated navigation, degraded network, high-content-density page, partial rollout).
