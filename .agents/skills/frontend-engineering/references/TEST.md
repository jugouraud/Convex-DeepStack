<!-- Source: FRONTEND_GUIDELINES(2).md, section TEST. Original rule numbers preserved, qualified with FE. -->

## TEST

- **FE.TEST1 M** Test user-observable behavior and contracts at the cheapest reliable level; unit-test nontrivial pure logic and component behavior where useful. Do not test trivial wrappers, private implementation order or trusted framework internals.
- **FE.TEST2 M** Verify real API/serialization/auth contracts at the boundary; do not mock the integration under test. Keep network doubles faithful to actual statuses, timing and payloads.
- **FE.TEST3 M** Cover relevant happy, invalid, empty, loading, failure, cancellation, permission-denied and repeated-action states; test race/rollback invariants for consequential async flows.
- **FE.TEST4 S** Use decision tables, boundary cases and parameterization for equivalent scenarios; avoid redundant tests and meaningless coverage inflation.
- **FE.TEST5 M** Use behavior-based names, clear arrange/act/assert, independent expectations, and observable DOM/navigation/state assertions; avoid brittle exact markup snapshots for every variant.
- **FE.TEST6 M** Keep tests isolated and deterministic: controlled clock/network where needed, independent accounts/storage, no arbitrary sleeps, no production secrets or personal data.
- **FE.TEST7 S** Favor real fast collaborators and small explicit fixtures; stub costly/nondeterministic boundaries and avoid elaborate fake servers or deep mock chains without need.
- **FE.TEST8 S** Reproduce confirmed bugs before fixing when practical, keep valuable regressions and characterize current behavior before risky refactoring.
- **FE.TEST9 M** Exercise critical flows in a real browser with resilient semantic locators and readiness/web-first assertions; do not make screenshot-only tests stand in for behavior tests.
- **FE.TEST10 M** Test changed keyboard, focus and accessible structure where relevant; add manual assistive-technology evaluation for complex widgets or claims automation cannot support.
- **FE.TEST11 S** Use visual regression only for stable high-value surfaces; control fonts, viewport, time, animations and test data, and review intentional differences rather than blindly updating baselines.
- **FE.TEST12 M** Verify responsive/mobile behavior on applicable viewports; expand to real devices/browsers where touch, viewport, scrolling, virtual keyboard or rendering engines matter.
- **FE.TEST13 M** Run and report relevant repo checks (lint, types, tests, build); never weaken assertions, disable checks, silently bless snapshots or drop regressions to make CI green.
- **FE.TEST14 S** Treat coverage diagnostically; do not chase 100% metrics or introduce a custom test harness for a simple component.
- **FE.TEST15 M** Investigate reproducible flakes and distinguish environment failure from product regression. Temporary quarantine needs explicit tracking and removal criteria.
- **FE.TEST16 M** Validate security-critical behavior with denied actor/object/tenant cases and trusted server responses; verifying that a button is hidden is not an authorization test.
- **FE.TEST17 S** Test long copy, RTL/localized text, contrast/theme, large text, slow network and error banners for shared UI components where affected.
- **FE.TEST18 M** Never report unexecuted visual, accessibility, browser or performance checks as passing; explicitly name the remaining verification gap.
