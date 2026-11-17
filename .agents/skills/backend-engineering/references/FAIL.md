<!-- Source: BACKEND_GUIDELINES(1).md, section FAIL. Original rule numbers preserved, qualified with BE. -->

## FAIL

- **BE.FAIL1 M** Enumerate realistic failures across the touched boundary: invalid input, denied access, dependency timeout, partial outage, stale data, conflict, crash, disk/queue exhaustion, and overload; preserve correct outcomes for consequential operations.
- **BE.FAIL2 M** Bound all potentially unbounded work (retries, request fan-out, queues, polling, memory, file processing, recursion, batch loops, and concurrency).
- **BE.FAIL3 M** Give remote calls and multi-step workflows end-to-end deadlines with a defined budget allocation; layered timeouts must not accidentally exceed or undermine the caller's deadline.
- **BE.FAIL4 M** Retry only safe operations and identifiable transient failures; limit attempts, exponential backoff with jitter where appropriate, and total retry amplification across layers.
- **BE.FAIL5 M** Treat a timeout, broken connection, or cancelled request as possibly successful remotely; do not retry non-idempotent mutations blindly or assert that an external side effect did not occur.
- **BE.FAIL6 M** Apply overload controls at admission/resource boundaries—bounded queues, concurrency limits, quotas, fair scheduling or shedding—rather than letting the service fail by memory/thread exhaustion.
- **BE.FAIL7 S** Use circuit breakers, bulkheads, fallback paths, or hedging only for demonstrated dependency/failure patterns and with explicit correctness and blast-radius analysis.
- **BE.FAIL8 M** A fallback must not weaken authorization, privacy, encryption, data-integrity, or business rules or present stale/unverified state as current when that matters.
- **BE.FAIL9 M** Define safe error propagation and user-facing responses; log enough sanitized context for diagnosis, avoid leaked internals, and preserve typed domain rejection versus technical failure.
- **BE.FAIL10 M** Prevent cascading failure: avoid retry storms, synchronous fan-out to weak dependencies, hot-key concentration, unbounded waiting, and heavy diagnostic work during outage.
- **BE.FAIL11 S** Prefer graceful degradation for genuinely optional integrations and fail closed for security/integrity-sensitive authorization decisions; choose per capability, not a universal fallback rule.
- **BE.FAIL12 M** Test interrupted workflows at meaningful boundaries (before/after commit, before/after acknowledgement, after timeout) when side effects or recoverability are consequential.
- **BE.FAIL13 M** Provide a reconciliation path when transient failure leaves an uncertain financial, legal, data-integrity, or customer-visible outcome; don't substitute repeated blind retries for state inspection.
