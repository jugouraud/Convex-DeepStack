<!-- Source: AGENTS_v1.6(1).md / SCALE; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## SCALE


### Capacity and project growth

- CORE.SCALE1 M For scaling decisions define demand/data growth envelope, SLOs, time horizon, bottlenecks, resource/cost limits, and measured capacity/headroom including required failure scenarios.
- CORE.SCALE2 S Scale project delivery through owned cohesive modules, stable contracts, dependency-aware CI/builds and bounded change scope; split services/repos only for demonstrated ownership/deployment/operational benefit.

### Horizontal scaling and overload

- CORE.SCALE3 M For horizontal replicas define state/session/job ownership and routing; balance to ready capacity, drain removal, preserve in-flight effects; identify shared bottlenecks and required failure-domain independence.
- CORE.SCALE4 M When autoscaling, define workload signals, min/max/cost bounds, warmup/readiness, stabilization and safe scale-in; cap aggregate pools/connections/fan-out against downstream capacity.
- CORE.SCALE5 M Apply FAIL/DATA limits across tiers and tenants; define backlog age/recovery, admission/fairness, retry amplification and optional-feature degradation without weakening auth or data invariants.

### Databases and distributed caches

- CORE.SCALE6 S Before database distribution, examine query plans/indexes, N+1 access, bounded pagination/batching, pool size, retention and I/O; add replicas/partitions only for measured bottlenecks.
- CORE.SCALE7 M For replicas/regions define per-operation consistency, lag/freshness, read-after-write and failover/recovery behavior; route decisions needing current authority to a source that guarantees it.
- CORE.SCALE8 M If partitioning/sharding, choose keys from cardinality/access/skew/locality; define hot-key relief, routing/rebalance, cross-shard queries/transactions/uniqueness, migration and recovery.
- CORE.SCALE9 M For distributed caches define source of truth, freshness/invalidation, expiry/eviction, concurrent fills and miss/outage load; preserve tenant scope/deletion and protect origin from refill storms.

### Distributed CPU/GPU work

- CORE.SCALE10 S For multi-node CPU/GPU work measure useful scaling versus network/collectives/I/O; partition inputs once, bound per-rank CPU/RAM/VRAM, preserve collective/seed/global-batch/checkpoint semantics.

### Verification and safe rollout

- CORE.SCALE11 M Validate scale claims with representative ramp/burst/soak, cold-cache and relevant failure/scale-in tests; record offered/admitted/completed work, tails/errors/backlog, bottlenecks, recovery and cost; check generator capacity.
- CORE.SCALE12 M For scaling rollouts/resharding define mixed-version schema/event compatibility, bounded backfill/dual-write reconciliation, staged exposure, stop/rollback criteria and post-change capacity verification.
