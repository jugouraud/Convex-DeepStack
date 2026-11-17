<!-- Source: BACKEND_GUIDELINES(1).md, section DOMAIN. Original rule numbers preserved, qualified with BE. -->

## DOMAIN

- **BE.DOMAIN1 M** Identify authoritative business invariants (money, inventory, ownership, eligibility, quotas, state transitions) and enforce them at a boundary a concurrent client cannot bypass.
- **BE.DOMAIN2 S** Use ubiquitous domain language and small cohesive business capabilities; an aggregate/DDD pattern is useful only when it clarifies real consistency and ownership boundaries.
- **BE.DOMAIN3 M** Treat authorization, input validity, business admissibility, and persistence integrity as separate checks; passing one does not imply the others.
- **BE.DOMAIN4 M** Specify state transitions, allowed actors, retries, reversals, and terminal states for consequential workflows; reject invalid transitions rather than repairing them silently.
- **BE.DOMAIN5 M** Use domain-appropriate exact numeric representations, units, currencies, rounding rules, and precision. Avoid binary floating-point for exact money/accounting balances.
- **BE.DOMAIN6 S** Model events as facts that happened and commands as requested actions; keep names, timestamps, causal meaning, and versioning clear without mandating event sourcing.
- **BE.DOMAIN7 M** Preserve uniqueness and conservation invariants under concurrency (e.g. no duplicate charge, oversold allocation, or cross-tenant transfer) using authoritative transactions/constraints or a documented equivalent.
- **BE.DOMAIN8 S** Keep policy/decision logic testable with explicit inputs; avoid reading ambient clocks, environment variables, network data, and persistence deep inside deterministic rules.
- **BE.DOMAIN9 M** Define whether an external side effect is reversible, compensatable, or irrevocable; do not treat compensation as a true database rollback or promise atomicity across unrelated providers.
- **BE.DOMAIN10 S** Record domain terms that appear ambiguous across teams/services; resolve meaning at contracts rather than multiplying translation layers without need.
