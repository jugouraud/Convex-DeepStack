<!-- Source: BACKEND_GUIDELINES(1).md, section TEST. Original rule numbers preserved, qualified with BE. -->

## TEST

- **BE.TEST1 M** Test externally observable behavior and domain invariants at the cheapest reliable level; unit-test nontrivial pure logic, but validate real DB/protocol/runtime behavior at the actual boundary.
- **BE.TEST2 M** Do not mock the integration under test: use representative database, broker, HTTP, auth, and serialization behavior for contract-critical checks rather than fake success returns.
- **BE.TEST3 M** Cover relevant success, invalid, unauthorized, cross-tenant, not-found, conflict, timeout, cancellation, partial-failure, and unknown-outcome states for consequential paths.
- **BE.TEST4 M** Test concurrent attempts, duplicate retries, stale versions, uniqueness conflicts, and lost-update/write-skew risks when changing authoritative shared state.
- **BE.TEST5 M** Keep tests isolated and repeatable: deterministic clocks/randomness where appropriate, separate test identities/data, cleanup, controlled external effects, and no production secrets.
- **BE.TEST6 S** Prefer small explicit fixtures and real fast collaborators; mock expensive/nondeterministic external boundaries, not every internal function call or implementation step.
- **BE.TEST7 M** Use behavior-based names, clear arrange/act/assert, and meaningful outcomes; avoid brittle assertions of query count, private helper calls, or incidental log order unless those are contractual/performance requirements.
- **BE.TEST8 S** Use decision tables, property-based tests, fuzzing, and mutation-style checks for parsers, permission matrices, financial calculations, and state transitions where they expose edge cases better than long duplicated examples.
- **BE.TEST9 M** For API/serialization changes, verify actual wire payloads, statuses, error cases, content types, backward compatibility, and representative consumer versions where risk warrants.
- **BE.TEST10 M** Test high-risk schema migrations on nonempty representative data, mixed app versions, long-running jobs, backfill replay, and failure/resume behavior; a fresh-schema test is insufficient.
- **BE.TEST11 M** Verify authorization with permitted and forbidden actor/object/tenant combinations and the real policy boundary; checking that UI hides a button or middleware simply runs is not enough.
- **BE.TEST12 S** Reproduce confirmed bugs before fixing when practical and retain high-value regressions; do not add snapshots/harness complexity that merely replicates implementation internals.
- **BE.TEST13 M** Use bounded retries and readiness assertions in integration tests; avoid arbitrary sleeps, timing-sensitive schedules, uncontrolled parallel state, and flakiness disguised as random reruns.
- **BE.TEST14 M** Verify durable job/queue behavior around crash/restart/duplicate delivery, acknowledgement, idempotency, ordering, retry exhaustion, and dead-letter handling when affected.
- **BE.TEST15 S** Use targeted fault-injection or property/model-based concurrent tests for significant distributed invariants; do not demand a cluster test for routine pure logic.
- **BE.TEST16 M** Before claiming performance or scale improvements, test relevant real workloads and resource/latency distributions with comparable settings; microbenchmarks cannot stand in for production-path proof.
- **BE.TEST17 S** Include load, stress, soak, and burst tests only where change risk/traffic justifies them, and do not pollute production services or consume uncontrolled cost during test runs.
- **BE.TEST18 M** Run and report actual repository checks; do not weaken assertions, disable failing gates, delete useful regressions, or relabel blocked tests as passing.
- **BE.TEST19 M** Distinguish pre-existing failures, environment flakiness, unexecuted tests, and patch regressions; quarantine needs ownership, tracking, and a removal trigger.
- **BE.TEST20 M** Use synthetic or governed deidentified test data; never embed live credentials, sensitive personal records, or production tokens in test fixtures/logs.
- **BE.TEST21 S** Consider contract tests for provider/consumer independence and executable state-machine tests for complex workflows, but avoid creating a new test platform for trivial endpoints.
- **BE.TEST22 M** When recovery guarantees matter, test restore/readability, checksums/invariants, RPO/RTO where claimed, and at least one realistic failed-deploy/partial-migration scenario.
