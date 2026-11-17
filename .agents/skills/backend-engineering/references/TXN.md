<!-- Source: BACKEND_GUIDELINES(1).md, section TXN. Original rule numbers preserved, qualified with BE. -->

## TXN

- **BE.TXN1 M** Identify the atomic commit boundary for every consequential mutation and the invariants it protects. Use a real transaction or verified atomic operation, not a sequence of unguarded reads/writes.
- **BE.TXN2 M** Resolve races with database constraints, compare-and-swap/version checks, predicate locking, serializable isolation, or equivalent design appropriate to the invariant; do not treat `if not exists` as concurrency-safe.
- **BE.TXN3 M** Define idempotency keys/uniqueness scope, actor/tenant ownership, retention window, request fingerprint, response replay, and concurrent duplicate behavior where mutations are retried.
- **BE.TXN4 M** Do not equate HTTP retries, client cancellation, transaction rollback, and external-provider effects. Record and reconcile **unknown outcome** states after timeouts.
- **BE.TXN5 M** Do not claim atomicity across a database and external network service without an actual protocol/guarantee. Consider transactional outbox or a reconciled workflow for durable cross-boundary effects where needed.
- **BE.TXN6 S** Prefer one authoritative local transaction over distributed two-phase commit when the business does not require global atomicity; document partial states and compensation where chosen.
- **BE.TXN7 M** Ensure transaction retries rerun all dependent reads/decisions correctly, have a bounded attempt budget, and cannot duplicate nontransactional effects.
- **BE.TXN8 M** On optimistic concurrency conflict, specify whether to reject, merge, retry, or request new user intent; do not silently overwrite more recent valid state.
- **BE.TXN9 S** Record causal workflow identifiers and durable status where external operations can outlive the request; make reconciliation possible without guessing from logs.
- **BE.TXN10 M** Apply uniqueness and idempotency controls before externally visible irreversible actions wherever supported; protect the whole operation, not just an HTTP handler's first execution.
- **BE.TXN11 M** Distinguish at-most-once attempt, at-least-once delivery, effect-once handling, and exactly-once claims; verify end-to-end semantics including failures and replays.
- **BE.TXN12 S** Prefer a simple single-resource transaction when adequate; do not introduce sagas, distributed locks, and event-sourced compensations as boilerplate.
