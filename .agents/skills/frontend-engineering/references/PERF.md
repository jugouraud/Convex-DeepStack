<!-- Source: FRONTEND_GUIDELINES(2).md, section PERF. Original rule numbers preserved, qualified with FE. -->

## PERF

### Objectives, measurement and budgets

- **FE.PERF1 M** Before consequential optimization, define target user journeys, relevant devices/networks, budget and representative baseline. Compare production-equivalent builds and record actual before/after results.
- **FE.PERF2 S** Use Core Web Vitals field targets as default guidance: 75th-percentile **LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1**, segmented mobile/desktop where data permits. Actual contractual/project SLOs take precedence; revisit metric definitions as they evolve.
- **FE.PERF3 M** Measure both lab and real-user performance where available; do not mistake Lighthouse scores, dev builds or a fast desktop run for the distribution of field experience.
- **FE.PERF4 M** Check regressions on affected critical routes and interactions, including cold load and meaningful warm navigation, without inventing thresholds or gains that have not been measured.

### Network and loading

- **FE.PERF5 S** Remove unnecessary requests, chained dependencies and blocking resources before adding complex caches or resource hints. Prioritize critical HTML, CSS, image and font discovery.
- **FE.PERF6 S** Choose route/feature-level code splitting based on measured initial cost and interaction latency; avoid overly fragmented chunks and waterfalls caused by excessive splitting.
- **FE.PERF7 M** Keep secrets out of preloaded data and public build outputs; make prefetching permission-aware and cancel or limit speculative network activity where expensive.
- **FE.PERF8 S** Set correct cache semantics for versioned static assets versus private or rapidly changing responses; account for CDN layers, invalidation and deployment compatibility.

### Rendering and interaction

- **FE.PERF9 S** Avoid unnecessary render work, broad subscriptions, expensive calculations during interaction, layout thrashing and repeated style measurement; profile before adding memoization or virtualization.
- **FE.PERF10 M** Avoid unbounded long main-thread tasks on latency-critical interactions. Chunk, defer, offload or simplify demonstrated heavy work, preserving cancellation and correctness.
- **FE.PERF11 S** Prevent layout instability using dimensions/aspect ratios, stable placeholders and delayed-content strategies; do not hide large layout shifts behind fixed-height hacks that clip content.
- **FE.PERF12 S** Use server/static rendering for meaningful first content where justified; minimize hydration cost and client bundle work but do not degrade correctness or interactivity solely to improve one metric.
- **FE.PERF13 M** Treat performance changes to data fetching, concurrent tasks and caches as correctness changes: verify freshness, order, authorization, memory limits, cleanup and failure behavior.
- **FE.PERF14 S** Profile memory leaks and repeated mount/navigation cycles when relevant; remove listeners, subscriptions, retained DOM references and large unnecessary cache entries.
- **FE.PERF15 S** Use real user journey instrumentation for important interactions, not synthetic click timing alone; investigate long-tail INP and task contention if affected.

### Evidence and restraint

- **FE.PERF16 M** Record measured cost/benefit for consequential caches, virtual lists, workers, speculative preloads, render-mode switches and new performance dependencies; retain simpler alternatives if evidence is inconclusive.
- **FE.PERF17 S** Make budgets route/class-specific where product needs differ (landing page, authenticated workspace, visualization) instead of mandating arbitrary site-wide byte ceilings.
