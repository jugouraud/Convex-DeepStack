<!-- Source: FRONTEND_GUIDELINES(2).md, section JS. Original rule numbers preserved, qualified with FE. -->

## JS

- **FE.JS1 M** Keep render/computation functions free of externally visible side effects where the framework expects purity; never depend on a particular number of renders or effect calls.
- **FE.JS2 M** Register and clean up listeners, observers, subscriptions, intervals, workers and other resources according to ownership; prevent listeners/timers from outliving their route/component.
- **FE.JS3 S** Prefer declarative DOM/framework bindings over manual DOM mutation; use imperative APIs only for integration, focus, measurements or other specific browser capabilities.
- **FE.JS4 M** Handle promise rejection and cancellation where ownership demands it; avoid stale responses overwriting newer results and updates after disposal/unmount.
- **FE.JS5 M** Avoid unbounded synchronous work on the main thread and unbounded queue/microtask loops. Partition or offload demonstrably heavy tasks without compromising state consistency.
- **FE.JS6 S** Keep event handlers short and tied to intent; avoid broad document-level delegation when native propagation/framework handlers suffice. Account for event phase, passive listeners and cleanup where relevant.
- **FE.JS7 M** Do not use `eval`, dynamic `Function`, string-based timers, unsafe template execution or arbitrary code loading for application logic.
- **FE.JS8 S** Use feature detection and well-supported modern JS constructs; avoid polyfills or legacy transpilation targets unsupported by project requirements.
- **FE.JS9 M** Define behavior for async interactions that can be repeated, interrupted or completed out of order; do not assume a user's rapid clicks or navigation cannot race requests.
- **FE.JS10 S** Be deliberate about references, closures, object lifetimes and memory retention; avoid premature micro-optimization without profiling.
