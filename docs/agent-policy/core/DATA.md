<!-- Source: AGENTS_v1.6(1).md / DATA; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## DATA

- CORE.DATA1 M Own each entity/artifact and transaction boundary; define persistent/API/event schema evolution and producer–consumer compatibility.
- CORE.DATA2 M Enforce mutable invariants atomically using authoritative state, transactions/constraints/conditional writes; prevent check/use races and unintended partial state.
- CORE.DATA3 M For consequential retries/delivery, scope durable idempotency/deduplication to actor+operation with a retention window; reject conflicting reuse; prevent duplicate effects.
- CORE.DATA4 S Publish artifacts atomically; prefer immutable/versioned results and safe checkpoints; scope caches by permissions plus relevant input/config/model/schema revisions.
- CORE.DATA5 M For async jobs/events define identity/version, producer, states, timestamps, ordering/delivery, retention, cancellation, result access/replay; failed/cancelled work cannot expose partial results as success.
- CORE.DATA6 S Use outbox/equivalent for atomic DB+publish needs; track lag/dead letters/replay; avoid distributed transactions without genuine distributed ownership needs.
- CORE.DATA7 M For cross-service effects define compensable/retryable/irreversible steps and recovery when compensation fails; sagas do not provide global rollback.
