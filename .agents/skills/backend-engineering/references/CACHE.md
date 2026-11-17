<!-- Source: BACKEND_GUIDELINES(1).md, section CACHE. Original rule numbers preserved, qualified with BE. -->

## CACHE

- **BE.CACHE1 M** Identify source of truth, key namespace, tenant/permission scope, data sensitivity, TTL, invalidation events, maximum staleness, and failure behavior before adding a cache.
- **BE.CACHE2 S** Default to no new cache until profiling shows a meaningful repeated-cost bottleneck or an explicit operational need; optimize queries and request shape first.
- **BE.CACHE3 M** Never allow shared cache keys to mix users/tenants/authorization scopes. Account for permission changes, logout/revocation, and sensitive response controls.
- **BE.CACHE4 M** Define stale-read consequences for balances, access control, inventory, quotas, and other invariants; do not use cache state as sole authority for protected mutations.
- **BE.CACHE5 S** Prefer explicit invalidation or versioned keys when coherent with domain updates; do not stack multiple cache layers with unknown ownership and unpredictable expiry.
- **BE.CACHE6 M** Bound cache size, per-key payload, TTL/eviction, batch fill, and memory use; ensure eviction does not violate correctness.
- **BE.CACHE7 M** Plan for cache misses, restart/flush, degraded cache service, thundering herds, synchronized expiry, and cold start; use single-flight/jitter where they solve observed risks.
- **BE.CACHE8 S** Distinguish negative caching of truly absent resources from temporary permission denial, transient upstream failure, and stale replication results.
- **BE.CACHE9 M** Confirm invalidation and data versioning across deployments, backfills, schema migrations, and asynchronous updates; a compatible application rollback may still encounter newer cached values.
- **BE.CACHE10 S** Measure hit rate and end-to-end latency/DB load in representative traffic; a high hit rate alone does not prove positive system impact.
- **BE.CACHE11 M** Do not cache secrets or highly sensitive payloads outside approved storage/access/retention controls; cache encryption and network isolation do not substitute for authorization.
