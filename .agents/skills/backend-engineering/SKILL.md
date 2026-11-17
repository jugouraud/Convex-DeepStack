---
name: backend-engineering
description: Use on backend services, APIs, databases, transactions, queues, workers, security, storage, infrastructure and SRE; not for UI-only tasks.
---

# Backend Engineering

This skill adds domain-specific constraints to the repository `AGENTS.md` and shared `docs/agent-policy/core/` policy; it does **not** override safety, user intent or higher-priority instructions. The source's M/MUST, S/SHOULD and O/MAY levels are preserved. Conditional rules apply only to used technologies and actual affected boundaries.

## How to use (progressive disclosure)

1. Inspect actual files and code paths, then classify affected concerns. Read the shared core policy for relevant cross-cutting topics.
2. Read `references/WORK-addendum.md` for consequential code changes in this domain and `references/CODE-addendum.md` for domain-specific code conventions.
3. Read **only** the relevant topic references below, plus direct dependencies of the change; do not load all references or the literature by default.
4. Include applicable qualified rule IDs (e.g., `BE.A11Y3` / `BE.TXN3`) in the change plan. Original numeric suffixes and MUST/SHOULD strength are maintained.
5. If a policy conflicts with adopted repository contracts or another applicable rule, surface the conflict rather than silently overriding it.

## Reference router

- `WORK-addendum.md`: domain-specific risk, six-pass additions and impact-to-check matrix.
- `CODE-addendum.md`: unique domain-level coding rules beyond `CORE.CODE`.

### Application architecture

- `ARCH` → `references/ARCH.md` — modular monoliths/services, boundaries, ports/adapters, coupling, migrations.
- `DOMAIN` → `references/DOMAIN.md` — business invariants, aggregates, ownership, state transitions, money.
- `TYPE` → `references/TYPE.md` — type systems, runtime schemas, nullability, serialization, contract boundaries.
- `RUNTIME` → `references/RUNTIME.md` — process model, concurrency, cancellation, lifecycle, memory, resource ownership.
- `API` → `references/API.md` — HTTP contracts, request/response semantics, versioning, pagination, webhooks.
- `RPC` → `references/RPC.md` — gRPC/GraphQL/internal APIs, interface definitions, propagation, compatibility (when used).
- `NET` → `references/NET.md` — DNS, TLS, HTTP connections, proxies, timeouts, network trust boundaries.

### Data, durability and distribution

- `DATA` → `references/DATA.md` — data models, lifecycle, ownership, integrity, classification, retention.
- `SQL` → `references/SQL.md` — relational schemas, queries, indexes, isolation, connection use, query plans.
- `TXN` → `references/TXN.md` — atomicity, concurrency control, idempotency, transactional side effects.
- `MIG` → `references/MIG.md` — schema/data migrations, compatibility windows, backfills, rollback.
- `DIST` → `references/DIST.md` — distributed consistency, clocks, ordering, consensus, partitions, split-brain.
- `CACHE` → `references/CACHE.md` — caching, freshness, key isolation, invalidation, stampede/eviction.
- `MSG` → `references/MSG.md` — queues, event streams, consumer behavior, delivery semantics, schema evolution.
- `JOB` → `references/JOB.md` — asynchronous jobs, schedulers, retries, leases, workflows, reconciliation.

### Trust and resilience

- `FAIL` → `references/FAIL.md` — failure modes, timeouts, overload, degradation, retry and recovery budgets.
- `AUTH` → `references/AUTH.md` — identity, sessions, authorization, tenancy, service credentials.
- `SEC` → `references/SEC.md` — threat models, injection, SSRF, validation, safe defaults, abuse resistance.
- `CRYPTO` → `references/CRYPTO.md` — encryption, password hashing, key management, tokens, randomness.
- `PRIV` → `references/PRIV.md` — personal-data minimization, redaction, retention, deletion, access.

### Operations and delivery

- `PERF` → `references/PERF.md` — baselines, latency, throughput, profiling, memory, allocation, query efficiency.
- `CAP` → `references/CAP.md` — capacity, quotas, queueing, load shedding, scaling, efficiency/cost.
- `OBS` → `references/OBS.md` — structured logs, metrics, traces, audits, alerting, cardinality.
- `TEST` → `references/TEST.md` — unit, contract, integration, migration, concurrency, load, fault testing.
- `BUILD` → `references/BUILD.md` — dependencies, CI, locked builds, artifacts, provenance, supply chain.
- `CONFIG` → `references/CONFIG.md` — environment, secrets, feature flags, validation, runtime configuration.
- `DEPLOY` → `references/DEPLOY.md` — release safety, schema compatibility, rollouts, readiness, rollback.
- `INFRA` → `references/INFRA.md` — containers, cloud, IAM, IaC, networking, platform limits (when used).
- `SRE` → `references/SRE.md` — SLOs, error budgets, incidents, on-call, runbooks, postmortems.
- `DR` → `references/DR.md` — backups, restores, disaster recovery, data reconstruction, integrity drills.
- `FILE` → `references/FILE.md` — uploads, object storage, exports, streaming, content safety (when used).
- `I18N` → `references/I18N.md` — time zones, Unicode, locale-aware data, business calendars and units.
- `AI` → `references/AI.md` — agent-generated code and model/tool-backed backend features (when used).
- `DOC` → `references/DOC.md` — ADRs, contracts, operational documentation, rule maintenance, traceability.

### Maintenance-only

- `references/maintenance-literature.md`: bibliographies, standards and literature-extraction notes; consult for policy updates or standards research, **not** routine code changes.

If both frontend and backend boundaries change, load both skills, but keep one scoped patch plan and one verification record.
