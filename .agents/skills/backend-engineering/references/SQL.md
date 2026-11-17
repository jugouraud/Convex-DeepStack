<!-- Source: BACKEND_GUIDELINES(1).md, section SQL. Original rule numbers preserved, qualified with BE. -->

## SQL

- **BE.SQL1 M** Use parameterized statements or trusted query builders; never concatenate untrusted values into SQL expressions, identifiers, predicates, or raw query fragments.
- **BE.SQL2 M** Set database constraints for true invariants: keys, uniqueness, foreign keys where appropriate, checks, nullability, and cascade semantics; validate at boundaries as a complementary UX layer.
- **BE.SQL3 M** Review transaction isolation, concurrent writers, phantom/write-skew/lost-update risks, and lock behavior for operations depending on current state; test against the actual database engine.
- **BE.SQL4 S** Keep queries straightforward and inspect real plans/statistics when performance matters. Avoid indiscriminate indexes, `SELECT *` on costly paths, and N+1 query patterns.
- **BE.SQL5 M** Bound result sizes and query time, avoid unindexed full-table scans on hot endpoints unless deliberately acceptable, and cancel/release slow queries where supported.
- **BE.SQL6 S** Index for representative predicates, joins, sorting, cardinality, and write costs; validate with realistic data and inspect index bloat/maintenance overhead.
- **BE.SQL7 M** Handle uniqueness conflicts, deadlocks, serialization failures, and stale writes explicitly; retries must operate on a safe transaction boundary and respect a bounded budget.
- **BE.SQL8 M** Keep transactions short and free from avoidable network calls, slow user interaction, or large streaming work; prolonged locks cause latency, contention, and availability failures.
- **BE.SQL9 S** Use a pool sized for DB capacity, concurrency, and deployment replica count; more connections do not necessarily increase throughput.
- **BE.SQL10 M** Know how ORM flush, lazy loading, cascades, identity maps, and automatic retries affect real SQL and transaction boundaries; ORM syntax is not proof of atomicity or efficiency.
- **BE.SQL11 M** Do not use read replicas for read-after-write/authorization/inventory paths that require stronger freshness than observed replication lag can provide.
- **BE.SQL12 S** Use set-oriented operations/bulk writes for large updates when safe, with bounded batches and correctness checks instead of millions of individual round trips.
- **BE.SQL13 M** Define collation, case handling, uniqueness, normalization, decimal scale, and time-zone types deliberately; do not rely on environment-specific defaults for business keys.
- **BE.SQL14 M** Preserve correctness across pagination and concurrent inserts/deletes: define stable sort keys/cursors or explicitly document snapshot and drift semantics.
- **BE.SQL15 S** Review the actual database's documented isolation guarantees and known anomalies; labels such as `REPEATABLE READ` need not mean identical behavior across engines.
