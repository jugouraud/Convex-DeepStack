<!-- Source: FRONTEND_GUIDELINES(2).md, section DATA. Original rule numbers preserved, qualified with FE. -->

## DATA

- **FE.DATA1 M** Choose browser storage intentionally: memory, URL, cookies, sessionStorage, localStorage, IndexedDB and Cache Storage have different security, lifetime and sharing properties.
- **FE.DATA2 M** Do not store credentials or sensitive personal data in script-readable storage by default; where unavoidable, document risk, retention, access and clearing behavior.
- **FE.DATA3 M** Version persisted client schemas and define migration/invalid-data handling; never assume long-lived storage will always match the current build.
- **FE.DATA4 M** Define authority, TTL, invalidation, logout behavior and permission scope for caches; respect no-store/private responses and do not cache another user's data under a shared key.
- **FE.DATA5 S** Use atomic or recoverable update patterns for consequential local data; test quota denial, private mode, storage unavailability and corrupt records when product depends on persistence.
- **FE.DATA6 M** For offline queues or deferred mutations, define actor, ordering, idempotency, conflict resolution, cancellation and what happens after account changes or logout.
- **FE.DATA7 S** Prefer server-owned authoritative persistence to ad hoc browser stores; keep local persistence limited to UX requirements and supported offline functions.
- **FE.DATA8 M** Treat cross-tab synchronization and BroadcastChannel/storage events as coordination, not a reliable transactional authority; protect against duplicate effects.
