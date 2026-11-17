<!-- Source: FRONTEND_GUIDELINES(2).md, section FAIL. Original rule numbers preserved, qualified with FE. -->

## FAIL

- **FE.FAIL1 M** Define visible and safe loading, empty, denied, offline, slow, timed-out, invalid-data and retry states where they can occur; never silently replace failure with a misleading successful UI.
- **FE.FAIL2 M** Bound request retries, polling, prefetching, listeners, memory, event queues and large content rendering; prevent overload amplification and duplicate effects.
- **FE.FAIL3 M** Provide retry/undo/recovery only when the action is actually safe; clearly distinguish pending, failed, cancelled and outcome-unknown mutations.
- **FE.FAIL4 S** Use error boundaries or route isolation to contain unexpected component failures without masking security or data-integrity errors; identify recovery ownership.
- **FE.FAIL5 M** Ensure thrown errors and rejected promises reach a handler that can act, report or surface appropriate feedback; do not swallow exceptions or leak technical details into user-facing errors.
- **FE.FAIL6 S** Degrade noncritical enhancements deliberately under poor networks, reduced capability or third-party outages; never weaken authentication, authorization or privacy controls as a fallback.
- **FE.FAIL7 M** Release timers, subscriptions, pending tasks and retained resources on cancellation/navigation; avoid leaked background work and updating disposed UI.
- **FE.FAIL8 S** Avoid elaborate retry/circuit-breaker/fallback frameworks for ordinary frontend flows; add resilience machinery only for observed fault modes and bounded operational needs.
