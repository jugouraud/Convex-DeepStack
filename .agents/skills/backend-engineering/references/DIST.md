<!-- Source: BACKEND_GUIDELINES(1).md, section DIST. Original rule numbers preserved, qualified with BE. -->

## DIST

- **BE.DIST1 M** State the consistency guarantees that matter: linearizability, serializability, read-your-writes, monotonic reads, causal ordering, bounded staleness, or best-effort eventual convergence; do not use 'strong' or 'eventual' without specifying observable behavior.
- **BE.DIST2 M** Assume network partitions, delayed/lost/duplicated messages, reordered responses, and independent process failure when designing multi-node workflows.
- **BE.DIST3 M** Do not use wall-clock timestamps alone for causality or mutually exclusive ownership. Account for skew, drift, leap/calendar behavior, and monotonic versus real time.
- **BE.DIST4 M** Where leader election/lease ownership controls correctness, define fencing or equivalent stale-owner protection; an expired lease does not stop a paused former owner from writing.
- **BE.DIST5 S** Keep cross-service invariants rare and explicit; prefer a single authoritative owner and transaction boundary where one exists.
- **BE.DIST6 M** Specify duplicate, out-of-order, missing, and replayed event behavior, including how state converges and how irreconcilable conflicts surface.
- **BE.DIST7 M** Do not implement a homegrown consensus protocol, distributed lock algorithm, or leader election when a vetted managed/established mechanism fits; understand its failure guarantees before relying on it.
- **BE.DIST8 S** Separate request/command acknowledgement from durable completion; expose pending/unknown states for asynchronous multi-step operations.
- **BE.DIST9 M** When using replicas, document replication mode, lag, failover promotion, conflict handling, and the potential for stale or lost acknowledged writes under the chosen guarantee.
- **BE.DIST10 M** Test correctness under induced faults and concurrency when a distributed invariant is consequential; unit tests with a single successful timeline cannot prove it.
- **BE.DIST11 S** Prefer deterministic replay, event versioning, and reconciliation for derived state; avoid demanding synchronized clocks or total ordering across independent domains without justification.
- **BE.DIST12 M** Do not assert exactly-once delivery or global order merely because a broker, transport, or vendor markets it; specify scope and verify downstream side effects.
- **BE.DIST13 S** Distinguish availability goals under partition from integrity goals; deliberately reject writes when necessary to preserve non-negotiable invariants.
