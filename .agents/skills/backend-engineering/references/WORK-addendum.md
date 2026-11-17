# backend-engineering: workflow addendum

> Applies together with [CORE.WORK](../../../../docs/agent-policy/core/WORK.md), never instead of it. All shared WORK1–WORK8 source IDs are aliases to CORE.WORK1–CORE.WORK8. The original specialized wording is retained in docs/agent-policy/sources/original-rulebooks.zip.

- **BE.WORK9 M** Preserve external contracts, persisted-data interpretation, intended ordering/consistency, authorization boundaries, error semantics, deployment compatibility, and recovery behavior unless explicitly changed.
- **BE.WORK10 S** Choose a proportional risk class (pure local logic, API, persistence, concurrency, auth/security, infrastructure/release, recovery) and grow test depth accordingly; a typo needs no failover drill and an idempotency change needs more than a unit happy-path.
- **BE.WORK11 M** Never claim an endpoint is safe, a migration reversible, a race eliminated, a backup restorable, or latency improved without actual relevant evidence. Distinguish reasoning from execution.
- **BE.WORK12 S** Deliver a concise report: behavior/files changed, why this boundary, checks run and results, migrations or operational impacts, unverified risks, and necessary follow-up only.
- **BE.WORK13 M** Before destructive or externally effective operations (data deletion, bulk mutation, migrations, key rotation, production changes, payments), determine authorization, scope, irreversibility, expected effects, and approved execution path; do not take such action implicitly as part of a patch.

### Backend-specific gated-pass focus (additive to CORE.WORK)

- **Scope:** entrypoints, clients, consumers, data readers/writers, transaction boundaries, authorization, external effects, deployment versions, and failure/recovery modes.
- **Implementation:** prefer the existing owner, authoritative transaction, schema and transport contracts; avoid new deployables, queues or layers without a demonstrated need.
- **Subtraction:** challenge new queries, indexes, caches, jobs, services, DTOs, flags, config, schema columns and I/O.
- **Efficiency:** inspect query count/plans, serialization, round trips, allocations, connection pools, lock duration, queues, timeouts and throughput budgets; measure consequential claims.
- **Failure/tests:** cover relevant denied/duplicate/concurrent/timeout/crash/migration/restart paths at the actual boundary, not with a mock of the subject.
- **Verification:** report actual checks, unexecuted checks, migration/release effects and uncertainty without overstated recovery or performance claims.

### Backend impact-to-check matrix (WORK5/WORK9/WORK10)

| Changed surface | Minimum relevant inspection/checks | Expand when |
| --- | --- | --- |
| Pure logic/types | Edge cases, invariants, targeted unit/type/lint | Money, dates, parsers, numeric precision, security predicates |
| API/serialization | Request/response contract, status/error behavior, auth failure, consumer compatibility | Public clients, webhooks, pagination, large bodies, old consumers |
| DB query/index | Real query shape, plan on representative data, transaction semantics, targeted integration | Locks, hot tables, scans, indexes, migrations, replicas |
| Schema/backfill | Expand/contract compatibility, dry run, rollback/recovery path, data validation | Large tables, long locks, dual-writes, non-null backfills |
| Concurrency/idempotency | Concurrent attempts, duplicates, retries, timeout-unknown outcomes | Money, inventory, multiple workers, external side effects |
| Queue/worker | Delivery, duplicates, poison messages, ordering, retries, shutdown | Multi-consumer scaling, DLQ, replay, scheduler ownership |
| Auth/security/privacy | Threat boundary, tenant/object denial, secret/PII handling, audit | Permissions, credential storage, exports, signing, deletion |
| Performance/capacity | Production-like baseline, latency percentiles, query/resource profile | Shared hot path, load spikes, autoscaling, tail behavior |
| Infrastructure/release | Build/image/config, readiness, rollout/rollback, smoke and observability | Traffic shifts, regional recovery, IAM/network policy, secrets |
| Backup/DR | Restore integrity, RPO/RTO evidence, failure and access controls | Destructive migration, new datastore, retention, region change |
