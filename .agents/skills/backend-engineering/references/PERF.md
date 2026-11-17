<!-- Source: BACKEND_GUIDELINES(1).md, section PERF. Original rule numbers preserved, qualified with BE. -->

## PERF

### Objectives, measurement, and workload realism

- **BE.PERF1 M** Establish target workloads, real endpoint/query/job mix, latency distribution (including p95/p99 where applicable), throughput, error rates, resource cost, and production-equivalent baseline before consequential optimization.
- **BE.PERF2 M** Optimize for a specified user/business SLO and limiting resource, not an attractive microbenchmark; measure end-to-end impact and correctness under representative concurrency.
- **BE.PERF3 S** Prioritize removal of unnecessary I/O, round trips, repeated queries, payloads, serialization, and idle waits before adding a new caching or concurrency layer.
- **BE.PERF4 M** Use flame graphs/profiles, DB plans, traces, lock and pool metrics, or equivalent evidence to identify dominant cost; do not ascribe a latency gain to a change without comparison.

### Latency, throughput, resources

- **BE.PERF5 S** Avoid N+1 database and HTTP calls; use joins, batching, prefetch or tailored endpoints where that reduces measured total work without violating isolation/authorization.
- **BE.PERF6 M** Bound memory, open connections, request bodies, streaming buffers, worker fan-out, allocations, and processing time on all externally influenced hot paths.
- **BE.PERF7 S** Keep useful CPU- or I/O-intensive work off latency-critical request paths when durability and product response semantics permit; do not hide essential work in unreliable fire-and-forget tasks.
- **BE.PERF8 M** Treat added concurrency, parallelism, and batching as correctness/capacity changes: examine contention, external rate limits, ordering, deadlines, backpressure, and partial results.
- **BE.PERF9 S** Reduce lock hold duration and transaction scope before introducing aggressive parallel writes; review deadlocks and replica/connection-pool pressure.
- **BE.PERF10 M** Evaluate indexes against production-like cardinality, selectivity, write costs, and actual plans; do not equate 'index added' with verified speedup.
- **BE.PERF11 S** Profile runtime-specific allocation/GC/event-loop/thread behavior where affected; avoid preemptive object pools, custom allocators, or lower-level rewrites without sustained evidence.
- **BE.PERF12 M** Check response tail latency and error rates under expected load, not only mean latency or single-client throughput, when changes touch shared critical paths.
- **BE.PERF13 S** Prefer streaming for large content and bounded batches for bulk jobs when useful; test cancellation, partial data, limits, and consumer behavior.

### Optimization restraint and rollout evidence

- **BE.PERF14 M** For material optimization, record before/after environment, workload, result distribution, correctness checks, and trade-offs; disclose noisy or incomparable tests.
- **BE.PERF15 M** Test cache/fan-out/async performance changes for data freshness, authorization, timeout, retries, resource exhaustion, and rollback behavior.
- **BE.PERF16 S** Distinguish warm/cold cache, startup, steady state, and burst/soak conditions; choose tests reflecting real traffic rather than a universal benchmark.
- **BE.PERF17 S** Track cost per unit of useful work (request/job/tenant) where material; avoid optimizing only peak throughput while sharply increasing idle infrastructure or operational complexity.
