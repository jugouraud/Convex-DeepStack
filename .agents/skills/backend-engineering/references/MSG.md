<!-- Source: BACKEND_GUIDELINES(1).md, section MSG. Original rule numbers preserved, qualified with BE. -->

## MSG

- **BE.MSG1 M** Define producer/consumer ownership, topic/queue meaning, message schema/version, ordering key, retention, acknowledgement, retry and replay semantics before adding messaging.
- **BE.MSG2 M** Assume at-least-once delivery, duplicate callbacks, and reordered events unless the actual end-to-end contract proves otherwise; make effects idempotent or detect duplicates durably.
- **BE.MSG3 M** Acknowledge a message only when its required durable effects are committed or safely recoverable; on exceptions distinguish retryable from permanent poison-message cases.
- **BE.MSG4 M** Bound consumer concurrency, in-flight messages, retry attempts, memory, and backlog growth. Apply backpressure and dead-letter/escalation ownership where needed.
- **BE.MSG5 M** Design event schema evolution for old consumers, retained events, replay, and rolling deployments; field removal/reinterpretation is a contract change.
- **BE.MSG6 S** Prefer a single event with clear business meaning rather than a chain of fine-grained notifications that couple services through incidental steps.
- **BE.MSG7 M** Keep publish/DB consistency explicit. Use transactional outbox or comparable durable coordination when lost or duplicate publication would violate required behavior.
- **BE.MSG8 M** Specify whether order is local to a partition/key, a producer, a consumer, or global; do not assume total order across workers or topics.
- **BE.MSG9 S** Use a schema registry or contract tests only where cross-team/schema drift warrants it; avoid unnecessary infrastructure for a single internal queue.
- **BE.MSG10 M** On consumer replay/rebuild, preserve effect-once semantics where promised and avoid re-sending irreversible external side effects without explicit replay policy.
- **BE.MSG11 M** Monitor consumer lag, age of oldest work, failure rates, DLQ growth, and throughput where messaging is production-critical; alert on user impact rather than arbitrary queue counts alone.
- **BE.MSG12 S** Prefer well-understood broker primitives over custom polling/protocols, but do not migrate a working application to event-driven architecture solely for conceptual purity.
- **BE.MSG13 M** Authenticate/authorize publishers and consumers, classify event data, and limit retention/access; a topic name or private network is not a security boundary.
