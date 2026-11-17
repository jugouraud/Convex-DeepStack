---
name: frontend-engineering
description: Use on changes to browser/UI, HTML/CSS/JS, UX, accessibility, client data, frontend APIs, web performance, builds or deployments; not for backend-only or CPU/GPU kernel work.
---

# Frontend Engineering

This skill adds domain-specific constraints to the repository `AGENTS.md` and shared `docs/agent-policy/core/` policy; it does **not** override safety, user intent or higher-priority instructions. The source's M/MUST, S/SHOULD and O/MAY levels are preserved. Conditional rules apply only to used technologies and actual affected boundaries.

## How to use (progressive disclosure)

1. Inspect actual files and code paths, then classify affected concerns. Read the shared core policy for relevant cross-cutting topics.
2. Read `references/WORK-addendum.md` for consequential code changes in this domain and `references/CODE-addendum.md` for domain-specific code conventions.
3. Read **only** the relevant topic references below, plus direct dependencies of the change; do not load all references or the literature by default.
4. Include applicable qualified rule IDs (e.g., `FE.A11Y3` / `FE.TXN3`) in the change plan. Original numeric suffixes and MUST/SHOULD strength are maintained.
5. If a policy conflicts with adopted repository contracts or another applicable rule, surface the conflict rather than silently overriding it.

## Reference router

- `WORK-addendum.md`: domain-specific risk, six-pass additions and impact-to-check matrix.
- `CODE-addendum.md`: unique domain-level coding rules beyond `CORE.CODE`.

### Application and platform

- `ARCH` → `references/ARCH.md` — app shape, routing boundaries, dependency graph, rendering strategy, ownership, migrations.
- `WEB` → `references/WEB.md` — HTML/CSS/JS platform behavior, browser APIs, compatibility, progressive enhancement.
- `HTML` → `references/HTML.md` — semantic documents, metadata, forms, links, media semantics, DOM structure.
- `CSS` → `references/CSS.md` — cascade, layout, responsive behavior, motion, theming, containment and layering.
- `JS` → `references/JS.md` — browser execution, events, concurrency, memory, cleanup, deterministic behavior.
- `TYPE` → `references/TYPE.md` — TypeScript, schemas, narrowing, public contracts, runtime boundary validation.
- `COMP` → `references/COMP.md` — components, composition, state ownership, reuse, lifecycle, rendering.
- `DS` → `references/DS.md` — design systems, tokens, visual consistency, component APIs, governance.
- `UX` → `references/UX.md` — interaction flows, feedback, content, usability, error prevention, visual states.

### Accessibility and interaction

- `A11Y` → `references/A11Y.md` — WCAG, keyboard, focus, names/roles/states, screen readers, motion, contrast.
- `FORM` → `references/FORM.md` — forms, inputs, validation, submission, errors, drafts, sensitive values.
- `STATE` → `references/STATE.md` — UI/server/URL state, async work, cache, synchronization, concurrency.
- `API` → `references/API.md` — HTTP contracts, requests, streaming, errors, auth, retries, pagination, upload.
- `DATA` → `references/DATA.md` — browser storage, caching, offline data, versioning, consistency, ownership.
- `FAIL` → `references/FAIL.md` — network failures, cancellation, timeouts, degradation, recovery, resource limits.
- `AUTH` → `references/AUTH.md` — authentication UX, session/browser credentials, client-side authorization boundaries.

### Security and delivery

- `SEC` → `references/SEC.md` — injection, CSP, URLs, navigation, embedding, third parties, dependencies.
- `PRIV` → `references/PRIV.md` — consent, analytics, data minimization, storage, exports, telemetry.
- `PERF` → `references/PERF.md` — Core Web Vitals, budgets, main thread, loading, render efficiency, measurement.
- `MEDIA` → `references/MEDIA.md` — images, fonts, icons, audio/video, responsive delivery, layout stability.
- `TEST` → `references/TEST.md` — behavior, component/integration/E2E, a11y, visual, network, regressions.
- `BROWSER` → `references/BROWSER.md` — cross-browser/device/input validation, progressive enhancement, hydration.
- `SEO` → `references/SEO.md` — public-page discoverability, crawlability, metadata, structured data, canonical URLs.
- `I18N` → `references/I18N.md` — localization, internationalization, Unicode, RTL, formats, language negotiation.
- `BUILD` → `references/BUILD.md` — packages, bundling, environment variables, CI, supply chain, reproducibility.
- `RELEASE` → `references/RELEASE.md` — deployments, flags, compatibility, caching rollout/rollback, monitoring.
- `OBS` → `references/OBS.md` — client errors, field measurements, observability, privacy-safe diagnostics.
- `PWA` → `references/PWA.md` — service workers, offline/install/update behavior, notifications (when used).
- `AI` → `references/AI.md` — AI/agent-generated code, untrusted content, AI UI/tool integrations.
- `DOC` → `references/DOC.md` — ADRs, rule maintenance, design/contract documentation, auditability.

### Maintenance-only

- `references/maintenance-literature.md`: bibliographies, standards and literature-extraction notes; consult for policy updates or standards research, **not** routine code changes.

If both frontend and backend boundaries change, load both skills, but keep one scoped patch plan and one verification record.
