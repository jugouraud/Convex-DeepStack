<!-- Source: BACKEND_GUIDELINES(1).md, section JOB. Original rule numbers preserved, qualified with BE. -->

## JOB

- **BE.JOB1 M** Define job durability, actor/tenant context, start/finish semantics, idempotency, retries, cancellation, progress, deadline, and terminal failure behavior for consequential background work.
- **BE.JOB2 M** Assume workers can crash between a side effect and checkpoint; make restart and duplicate execution safe, or expose/reconcile the uncertain state.
- **BE.JOB3 M** Bound per-job resource use, queue concurrency, memory, runtime, and batch size; avoid one large job monopolizing worker pools or database locks.
- **BE.JOB4 M** For scheduled work, account for missed and repeated triggers, DST/time-zone transitions, simultaneous schedulers, and deployment restarts; do not infer exactly-once scheduling.
- **BE.JOB5 S** Store progress/checkpoints for long resumable operations; prefer small restartable units over giant opaque jobs when recovery or backpressure warrants it.
- **BE.JOB6 M** Leases/locks for singleton work must guard against stale workers and expiry; use fencing or authoritative checks when overlapping execution is harmful.
- **BE.JOB7 S** Expose durable status and retry/reconciliation controls where user-facing work extends beyond request time; distinguish queued, running, completed, failed, cancelled, and unknown.
- **BE.JOB8 M** Make retries conditional on error type and idempotency; use bounded backoff/jitter and dedicated handling for permanent validation failures/poison payloads.
- **BE.JOB9 M** Ensure shutdown/redeployment does not silently discard accepted durable jobs; define visibility-timeout and acknowledgement ownership for the actual queue.
- **BE.JOB10 S** Keep workflows in a simple queue + transaction if sufficient; introduce a durable workflow engine only for demonstrated long-running coordination/recovery needs.
