<!-- Source: BACKEND_GUIDELINES(1).md, section DATA. Original rule numbers preserved, qualified with BE. -->

## DATA

- **BE.DATA1 M** Give every authoritative data set a named owner, lifecycle, security classification, integrity contract, retention policy, and supported read/write access paths.
- **BE.DATA2 M** Choose storage technology based on access patterns, transaction needs, query semantics, consistency, durability, scale, and operational competence—not novelty or benchmark marketing.
- **BE.DATA3 M** Enforce important identity/uniqueness/referential integrity with authoritative constraints or a verified equivalent; request-time checks alone are race-prone.
- **BE.DATA4 M** Distinguish source-of-truth records from derived indexes, search documents, materialized views, caches, and reporting projections; define rebuild and reconciliation behavior.
- **BE.DATA5 S** Minimize duplicate authoritative state and unclear ownership; accept intentional denormalization only with an update, staleness, and repair plan.
- **BE.DATA6 M** Scope queries, exports, tables, partitions, cache entries, and generated files by authenticated tenant/object permission; row filtering cannot rely on unverified caller fields.
- **BE.DATA7 M** Define deletion, archival, legal hold, soft delete, and retention semantics explicitly. A soft-delete flag does not satisfy erasure obligations without further analysis.
- **BE.DATA8 S** Prefer explicit domain-schema evolution and typed access over unbounded JSON catch-all columns when core invariants and useful queries require structure.
- **BE.DATA9 M** Validate and reconcile data after high-risk imports, replication changes, transformations, and migrations; counts alone may not prove semantic correctness.
- **BE.DATA10 M** Keep sensitive values out of production fixtures, seed data, logs, analytics, unencrypted dumps, and lower-trust environments unless properly approved and protected.
- **BE.DATA11 S** Record known constraints on freshness and accuracy for derived/reporting data; do not expose eventually consistent projections as transactionally current without a contract.
