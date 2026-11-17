<!-- Source: BACKEND_GUIDELINES(1).md, section ARCH. Original rule numbers preserved, qualified with BE. -->

## ARCH

- **BE.ARCH1 M** For consequential architecture, define bounded domain responsibilities, ownership, trust boundaries, consistency/availability needs, traffic, latency, failure tolerance, deployment constraints, and operational cost; compare with the simplest credible alternative.
- **BE.ARCH2 S** Prefer a cohesive modular monolith until independent deployment, isolation, scaling, organizational autonomy, or other demonstrated needs justify more services. Microservices are not a correctness or maturity requirement.
- **BE.ARCH3 M** Define stable public module/service contracts and dependency direction; forbid cyclic dependencies, cross-module private-table writes, and backdoor access to another owner's invariants without agreement.
- **BE.ARCH4 S** Place domain decisions and invariant enforcement outside transport/database framework details where helpful; do not require artificial hexagonal/clean-architecture layers for every handler.
- **BE.ARCH5 M** Assign one authoritative owner for mutable domain data and operations; document intentional replication, materialized views, and exception paths. Multiple writers need an explicit consistency design.
- **BE.ARCH6 S** Organize by business capability and reason to change; isolate adapters for external dependencies with meaningful replacement/test seams, not boilerplate for every library call.
- **BE.ARCH7 M** Identify trust and runtime boundaries: public edge, service-to-service, internal admin, worker, database, object store, third-party, and control-plane access; deployment location does not imply trust.
- **BE.ARCH8 S** Evolve boundaries incrementally with strangler/adapter patterns and compatible overlap where needed; avoid simultaneous rewrites, reorganizations, and schema/platform migrations.
- **BE.ARCH9 M** Explicitly model failure propagation, ownership of retries, side-effect ordering, data reconstruction, and rollback/roll-forward capabilities for distributed operations.
- **BE.ARCH10 S** For large systems, record 3–5 quality scenarios (e.g. 10x traffic burst, replica lag, partial region outage, failed payment callback, tenant boundary, zero-downtime schema upgrade).
- **BE.ARCH11 M** Do not introduce orchestration, a queue, service mesh, distributed transactions, or new database merely to align with a reference architecture; require a concrete problem and operating plan.
- **BE.ARCH12 S** Keep synchronous request paths short; move genuinely long or nonessential work to an existing asynchronous mechanism with explicit progress, durability, and recovery semantics.
- **BE.ARCH13 M** Document and test compatibility when extracting a service or moving ownership: authentication, API, schema, events, idempotency, old-client behavior, observability, and operations must remain coherent.
