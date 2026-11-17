<!-- Source: BACKEND_GUIDELINES(1).md, section MIG. Original rule numbers preserved, qualified with BE. -->

## MIG

- **BE.MIG1 M** Treat schema/data migrations as production operations with affected readers/writers, deployment order, lock duration, rollback/roll-forward, observability, and data-recovery requirements.
- **BE.MIG2 M** Use expand–migrate–contract for changes requiring mixed application versions: add compatible shape, transition reads/writes/backfill, verify, then remove old shape only after the compatibility window.
- **BE.MIG3 M** Do not deploy destructive drops, incompatible renames, tightened constraints, or changed enum semantics while old clients/jobs/replicas still depend on them.
- **BE.MIG4 M** Make data backfills restartable, bounded, observable, resumable, and idempotent, with progress checkpoints and sampled/aggregate postconditions appropriate to the risk.
- **BE.MIG5 S** Prefer online/index-concurrent/low-lock approaches supported by the real engine for hot large tables; verify actual database capabilities, replication lag, and DDL lock behavior.
- **BE.MIG6 M** Define how writes occurring during a backfill are captured and reconciled; a one-time copy cannot silently lose concurrent updates.
- **BE.MIG7 M** Test migration from representative existing state, not only an empty database; verify old-version/new-version overlap and downgrades where claimed.
- **BE.MIG8 M** A reverse schema migration is not automatically a safe data rollback. Record irreversibility, backup/snapshot checkpoints, and forward-fix procedure before execution.
- **BE.MIG9 S** Keep migrations scoped and reviewable; avoid combining unrelated table redesigns, bulk cleanup, and application feature work in one opaque change.
- **BE.MIG10 M** Coordinate storage, cache, search index, event schema, and API consumers during renames/deletions; database migration success alone does not prove system compatibility.
- **BE.MIG11 M** Make destructive migration execution an explicitly authorized operational action with a verified target environment and limited credentials, not an accidental application startup side effect.
