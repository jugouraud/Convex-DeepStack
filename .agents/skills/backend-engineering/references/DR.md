<!-- Source: BACKEND_GUIDELINES(1).md, section DR. Original rule numbers preserved, qualified with BE. -->

## DR

- **BE.DR1 M** Classify critical datasets and specify owner, backup frequency, retention, offsite/isolation protection, acceptable data-loss objective (RPO), and recovery-time objective (RTO) where necessary.
- **BE.DR2 M** Back up data and metadata needed for a coherent restore—schema, configuration, keys where legitimately recoverable, object-store pointers, and relevant transaction logs—not merely table rows.
- **BE.DR3 M** Test restoration and verification on an isolated representative environment; backup-job success alone does not prove recoverability or meet a claimed RPO/RTO.
- **BE.DR4 M** Guard backups/snapshots against unauthorized read/delete, encryption-key loss, ransomware, and irreversible retention policy errors according to the threat model.
- **BE.DR5 M** Define recovery sequence across database, broker, search, cache, application versions, secrets, identity, and external provider state; inconsistent multi-store restoration needs reconciliation.
- **BE.DR6 S** Prefer rebuilding derived indexes/caches from authoritative state rather than complicating backups when their recovery time meets requirements.
- **BE.DR7 M** Define point-in-time recovery and data-corruption detection for high-integrity stores where needed; replication alone is not a backup because corruption/deletion may replicate.
- **BE.DR8 M** Document which actions remain safe during regional outage/restore and which must be paused to avoid divergent writes, double execution, or stale authorization.
- **BE.DR9 S** Use tested recovery drills proportionate to criticality; do not require expensive cross-region active-active deployments when simpler restore capability meets product requirements.
- **BE.DR10 M** Treat destructive migrations, encryption-key changes, and datastore replacement as recovery-sensitive; establish a verified restoration checkpoint and approved escape route before acting.
