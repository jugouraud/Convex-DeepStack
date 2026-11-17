<!-- Source: FRONTEND_GUIDELINES(2).md, section DOC. Original rule numbers preserved, qualified with FE. -->

## DOC

- **FE.DOC1 S** Record consequential architecture decisions with context, alternatives, choice, implications, owner and revisit trigger; avoid ADRs for routine styling or local helper choices.
- **FE.DOC2 S** Document public components, route contracts, async states, design tokens, accessibility interaction and cross-feature interfaces where future maintainers need explicit knowledge.
- **FE.DOC3 M** Maintain stable rule IDs, levels and applicability. When updating a rule, describe the reason, impacted themes, migration/exception policy and authoritative source if it governs external behavior.
- **FE.DOC4 M** If a human companion is adopted, keep human and agent editions synchronized. Do not falsely claim synchronization with a document that does not exist.
- **FE.DOC5 S** Automate recurring high-risk checks using existing lint, type, build, test and CI tools; avoid introducing mandatory custom architecture scanners for conventions that can be reviewed cheaply.
- **FE.DOC6 M** Keep documented commands and review evidence accurate; distinguish required checks from suggestions and do not publish fabricated test results, measurements or unsupported conformance claims.
- **FE.DOC7 S** Review frontend guidance when supported browsers, WCAG, security practices, Core Web Vitals, framework/toolchain versions or product requirements materially change; supersede outdated decisions instead of silently rewriting history.
- **FE.DOC8 M** Source examples, reference patterns and anti-pattern catalogs are informative, not stronger than numbered rules or project-specific legal/security/correctness constraints.

### Suggested agent delivery format (DOC6; concise, not a mandatory report template)

1. **Outcome:** the user-visible change and files touched; describe why the implementation boundary is appropriate.
2. **Verification:** exact commands/observations and pass/fail/blocked status; include browser, accessibility and production-build checks **only if run**.
3. **Risk:** any unverified behavior, security/accessibility/performance concerns, assumptions or justified exceptions.
4. **Patch review:** actual unified diff by hunk, or the compact PDF review for delivered code changes when available under WORK8.

### Change-classification examples (informative; WORK10)

- **Single copy change:** inspect affected text/semantics; run a relevant fast check; no universal visual baseline rebuild.
- **New button or dialog:** verify semantics, keyboard/focus, pending/disabled states and a representative behavior test.
- **New data-fetching view:** verify empty/loading/error, stale result/cancel behavior, auth/data contract, navigation and one representative integration path.
- **Global CSS token update:** sample affected components/themes/viewport sizes, visible focus/contrast and relevant visual regressions.
- **New login/session flow:** check server enforcement, CSRF/redirects, storage/cookie scope, account switching, denial/expiry, E2E and environment headers.
- **Bundle/render optimization:** compare representative production builds, field metrics where available, correctness, hydration, caches and long-tail interactions.
