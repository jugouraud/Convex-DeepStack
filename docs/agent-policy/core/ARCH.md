<!-- Source: AGENTS_v1.6(1).md / ARCH; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## ARCH

- CORE.ARCH1 M Define capabilities, workload, state, reliability, change drivers, security, ownership, and measurable success before major design; record trade-offs and simpler alternatives.
- CORE.ARCH2 S Prioritize 3–5 quality scenarios; prefer a cohesive/modular monolith. Choose deployment, dependency shape, module boundaries, execution, and state independently.
- CORE.ARCH3 M Expose deliberate module APIs; keep private methods/tables/caches private; prevent dependency cycles and unauthorized cross-module state mutation.
- CORE.ARCH4 S Organize by capability/reason to change; share stable primitives narrowly; use one architecture vocabulary without duplicate conceptual layers.
- CORE.ARCH5 S Construct substantial configured infrastructure at the composition root; pass concrete/callable dependencies first; add ports/DI only for meaningful volatility or substitution.
- CORE.ARCH6 M Justify services/queues/plugins with present operational needs; specify extension lifecycle/contracts and isolate untrusted plugins. Treat remote calls as failure boundaries.
- CORE.ARCH7 S Migrate incrementally through stable seams and behavior checks; retain rollback, retire proven replacements, and avoid combining migrations with unrelated rewrites.
- CORE.ARCH8 M Honor adopted dependency boundaries; in clean/hexagonal designs source dependencies point toward stable policy, independent of volatile concrete infrastructure.
