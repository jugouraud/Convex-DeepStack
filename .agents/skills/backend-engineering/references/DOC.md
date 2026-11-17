<!-- Source: BACKEND_GUIDELINES(1).md, section DOC. Original rule numbers preserved, qualified with BE. -->

## DOC

- **BE.DOC1 S** Record consequential architecture decisions as ADRs with context, forces, alternatives including a simpler approach, decision, constraints, owner, and revisit trigger; routine helper edits do not need ADRs.
- **BE.DOC2 M** Document public API/event contracts, data ownership, non-obvious transactions, idempotency, deployment compatibility, and recovery assumptions when maintainers/operators depend on them.
- **BE.DOC3 M** Maintain stable rule IDs, M/S levels, applicability, version, and source anchors. When changing a rule, explain the rationale, migration impact, and any exception policy.
- **BE.DOC4 M** If a human companion is adopted, synchronize IDs, conditions, strengths, and exceptions. Do not claim synchronization with a document that does not exist.
- **BE.DOC5 S** Automate repeatable high-risk checks with existing CI, lint, type, contract, migration, security, and integration tooling; avoid an unnecessary custom governance engine.
- **BE.DOC6 M** Keep commands, test results, threat assumptions, performance measurements, and operational recovery claims accurate and reproducible. Clearly label unsupported claims.
- **BE.DOC7 S** Review the rulebook when normative standards, identity/security guidance, DB/runtime versions, cloud behavior, privacy obligations, and architecture/operating requirements materially change.
- **BE.DOC8 M** Books, pattern catalogues, vendor posts, benchmarks, and examples are informative, not stronger than numbered rules, real repository contracts, or mandatory obligations.
- **BE.DOC9 S** Keep a concise service README/runbook describing owners, startup/test commands, critical dependencies, important invariants, deploy/rollback, SLOs, and recovery links where applicable.

### Suggested agent delivery format (DOC6; concise, not a mandatory report template)

1. **Outcome:** requested behavior, changed files/entrypoints, and why the chosen module/data boundary owns it.
2. **Verification:** exact commands and observed pass/fail/blocked status; include DB/migration, concurrency, load, and deployment checks **only if run**.
3. **Risk:** compatibility, security/data integrity, failure/retry behavior, migrations/ops obligations, remaining unknowns, and justified exceptions.
4. **Patch review:** actual unified diff by hunk, or the compact PDF review for delivered code patches when available under WORK8.

### Change-classification examples (informative; WORK10)

- **Pure function or error-message fix:** test relevant edge/input cases, run fast project checks; no universal load test.
- **New/changed endpoint:** verify input validation, statuses, auth/tenant denial, serialization, consumer contracts, limits, and error behavior.
- **Query/index optimization:** inspect query plan on representative data, query correctness, transaction behavior, latency/load difference, and index/write cost.
- **New table/column/backfill:** check expand–migrate–contract, mixed versions, real old data, locks, resume/idempotency, and irreversible steps.
- **Payment/inventory/idempotency flow:** test concurrent attempts, duplicate calls, crash/timeout unknown outcomes, commit/side effect ordering, and reconciliation.
- **Queue/worker change:** check ack/retry/duplicate/replay, ordering scope, stale worker/lease, shutdown, backlog, and monitoring.
- **Auth/session/tenant policy:** verify denied actors and cross-tenant objects, expiry/revocation, token validation, secret redaction, and actual boundary enforcement.
- **Hot-path optimization:** compare production-equivalent latency distribution, errors, resource saturation, and data correctness before/after.
- **Deploy/platform change:** inspect built artifact and IaC/config diff, rollout/migration order, readiness, IAM/network policy, smoke checks, and rollback constraints.
- **Backup/recovery change:** perform an isolated restore/verification, check encryption and access, reconciliation, and RPO/RTO claims against actual results.
