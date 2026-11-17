<!-- Source: BACKEND_GUIDELINES(1).md, section RUNTIME. Original rule numbers preserved, qualified with BE. -->

## RUNTIME

- **BE.RUNTIME1 M** Know the actual execution model: process/thread/async task/event loop, request context, shared state, runtime limits, and signal semantics before adding concurrency.
- **BE.RUNTIME2 M** Bound concurrency, active requests, buffers, streams, in-memory queues, connection pools, worker counts, and task fan-out according to product needs.
- **BE.RUNTIME3 M** Propagate cancellation and deadlines through owned operations where supported; never assume that cancelling an HTTP request rolls back committed database work or external side effects.
- **BE.RUNTIME4 M** Shut down gracefully: stop admission, mark unready where applicable, drain/cancel bounded inflight work, release leases, close pools, and respect termination budgets.
- **BE.RUNTIME5 S** Prefer structured concurrency and explicit task ownership; avoid fire-and-forget tasks that can disappear on crash or leak exceptions, unless the operation is intentionally disposable.
- **BE.RUNTIME6 M** Guard shared mutable state with appropriate synchronization or ownership; verify data races, reentrancy, and memory visibility on supported runtimes.
- **BE.RUNTIME7 M** Close file handles, cursors, transactions, sockets, response bodies, threads, and timers along success, error, cancellation, and timeout paths.
- **BE.RUNTIME8 S** Distinguish CPU-bound, blocking I/O, and async work; do not block an event loop with heavy synchronous tasks or spawn unbounded threads as a shortcut.
- **BE.RUNTIME9 M** Treat process restarts, scale-out, and duplicate task execution as expected; process-local memory cannot be the sole authority for critical durable state.
- **BE.RUNTIME10 S** Profile allocation, garbage collection, object retention, and event-loop/worker saturation before adding pools or reusing mutable objects that complicate correctness.
